"""REM deployment gateway: an HTTP service at the tool-execution boundary.

A deployed agent framework does not execute tool calls itself; it sends each assistant turn's proposed
calls to this gateway. For every call, in order, the gateway runs REM (``RemGuard.evaluate``: evidence,
frozen estimator and calibration, consequence tier, predicates, expected-loss verdict, mitigation,
audit record) and forwards only RELEASED calls to the tool backend (here: a simulated banking API).
Withheld calls never reach the backend; the agent receives a refusal carrying the call's id.

Fail-closed rules:
  * any exception while REM evaluates a call  -> the call is withheld ("REM: internal error ...");
  * unknown episode or malformed request      -> HTTP 4xx, nothing is executed;
  * backend failure on a released call         -> error result, classified as infrastructure error
                                                  (never as a security decision).

The REM components are injected by ``provider(meta) -> (RemGuard, tool_names)`` at episode opening;
the gateway itself contains no design value. One guard per episode (state isolated per episode);
one lock per episode (calls of one episode are serialised; episodes run concurrently).

Endpoints (JSON):
  GET  /health
  POST /v1/episodes                    {episode_id, configuration, user_task_id, injection_task_id,
                                         injections, system_prompt, user_prompt}
  POST /v1/episodes/<id>/calls         {calls: [{id, function, args}]}
       -> {results: [{tool_call_id, content, error, released, verdict, rem_ms, backend_ms}]}
  POST /v1/episodes/<id>/close         {model_output, function_calls}
       -> {utility, security, audit, backend_executed}
"""
from __future__ import annotations

import http.client
import json
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, Optional, Set, Tuple
from urllib.parse import quote, unquote, urlparse

FAIL_CLOSED_NOTICE = "REM: internal error while evaluating this action; the action was withheld (fail-closed)."


class BackendClient:
    """JSON over HTTP to the tool backend; one keep-alive connection per thread."""

    def __init__(self, url: str, timeout: float = 30.0) -> None:
        u = urlparse(url)
        self.host, self.port, self.timeout = u.hostname, u.port, timeout
        self._local = threading.local()

    def _conn(self) -> http.client.HTTPConnection:
        c = getattr(self._local, "conn", None)
        if c is None:
            c = http.client.HTTPConnection(self.host, self.port, timeout=self.timeout)
            self._local.conn = c
        return c

    def post(self, path: str, body: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(body).encode()
        for attempt in (0, 1):                                  # one reconnect on a stale keep-alive socket
            try:
                c = self._conn()
                c.request("POST", path, body=data, headers={"Content-Type": "application/json"})
                r = c.getresponse()
                payload = json.loads(r.read() or b"{}")
                if r.status >= 400:
                    raise RuntimeError(f"backend HTTP {r.status}: {payload.get('error')}")
                return payload
            except (ConnectionError, http.client.HTTPException, OSError):
                self._local.conn = None
                if attempt:
                    raise
        raise AssertionError("unreachable")


class _Episode:
    def __init__(self, guard, tool_names: Set[str]) -> None:
        self.guard, self.tool_names, self.lock = guard, set(tool_names), threading.Lock()


class RemGateway:
    def __init__(self, provider: Callable[[Dict[str, Any]], Tuple[Any, Set[str]]], backend_url: str) -> None:
        self.provider = provider
        self.backend = BackendClient(backend_url)
        self.episodes: Dict[str, _Episode] = {}
        self._lock = threading.Lock()
        self.counters = {"episodes_opened": 0, "calls": 0, "released": 0, "withheld": 0, "fail_closed": 0,
                         "backend_errors": 0}

    # -- lifecycle -------------------------------------------------------------------------------
    def open(self, meta: Dict[str, Any]) -> Dict[str, Any]:
        eid = str(meta["episode_id"])
        guard, tools = self.provider(meta)
        self.backend.post("/v1/episodes", meta)
        with self._lock:
            if eid in self.episodes:
                raise ValueError(f"episode {eid!r} already open")
            self.episodes[eid] = _Episode(guard, tools)
            self.counters["episodes_opened"] += 1
        return {"episode_id": eid}

    def calls(self, eid: str, calls) -> Dict[str, Any]:
        ep = self.episodes.get(eid)
        if ep is None:
            raise KeyError(eid)
        out = []
        with ep.lock:
            g = ep.guard
            g.begin_decision_point()
            for c in calls:
                cid, fn, args = c.get("id"), c["function"], dict(c.get("args") or {})
                self.counters["calls"] += 1
                if fn not in ep.tool_names:
                    g.ingest(fn, "", executed=False)
                    out.append({"tool_call_id": cid, "content": "", "error": f"Invalid tool {fn} provided.",
                                "released": False, "verdict": None, "rem_ms": 0.0, "backend_ms": 0.0})
                    continue
                t0 = time.perf_counter()
                try:
                    release, notice = g.evaluate(fn, args)
                    verdict = g.audit[-1]["verdict"] if g.audit else None
                except Exception:                                    # fail-closed
                    release, notice, verdict = False, FAIL_CLOSED_NOTICE, "fail_closed"
                    self.counters["fail_closed"] += 1
                    g.audit.append({"tool": fn, "verdict": "fail_closed", "released": False,
                                    "error": traceback.format_exc(limit=2)[-500:]})
                rem_ms = (time.perf_counter() - t0) * 1e3
                backend_ms, text, err, executed = 0.0, "", notice, False
                if release:
                    t1 = time.perf_counter()
                    try:
                        r = self.backend.post(f"/v1/episodes/{quote(eid, safe='')}/execute", {"function": fn, "args": args})
                        text, err = r.get("text", ""), r.get("error")
                        executed = err is None
                    except Exception as exc:
                        text, err = "", f"backend unavailable: {type(exc).__name__}"
                        self.counters["backend_errors"] += 1
                    backend_ms = (time.perf_counter() - t1) * 1e3
                    self.counters["released"] += 1
                else:
                    self.counters["withheld"] += 1
                g.ingest(fn, text if executed else (err or ""), executed=executed)
                out.append({"tool_call_id": cid, "content": text, "error": err, "released": bool(release),
                            "verdict": verdict, "rem_ms": rem_ms, "backend_ms": backend_ms})
        return {"results": out}

    def close(self, eid: str, body: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            ep = self.episodes.pop(eid, None)
        if ep is None:
            raise KeyError(eid)
        res = self.backend.post(f"/v1/episodes/{quote(eid, safe='')}/close", body)
        audit = [{k: v for k, v in a.items() if k not in ("features", "available", "phi", "details", "risk_table")}
                 for a in ep.guard.audit]
        return {"utility": res["utility"], "security": res["security"], "audit": audit,
                "backend_executed": res.get("executed", [])}


def make_handler(gw: RemGateway):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *a):          # quiet
            pass

        def _send(self, code: int, obj: Dict[str, Any]) -> None:
            data = json.dumps(obj, default=str).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/health":
                self._send(200, {"status": "ok", "open_episodes": len(gw.episodes), "counters": gw.counters})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            try:
                n = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(n) or b"{}")
            except Exception:
                return self._send(400, {"error": "malformed JSON"})
            parts = [unquote(x) for x in self.path.strip("/").split("/")]
            try:
                if parts == ["v1", "episodes"]:
                    return self._send(200, gw.open(body))
                if len(parts) == 4 and parts[:2] == ["v1", "episodes"] and parts[3] == "calls":
                    return self._send(200, gw.calls(parts[2], body["calls"]))
                if len(parts) == 4 and parts[:2] == ["v1", "episodes"] and parts[3] == "close":
                    return self._send(200, gw.close(parts[2], body))
                return self._send(404, {"error": "not found"})
            except KeyError as exc:
                return self._send(404, {"error": f"unknown episode or field {exc}"})
            except (ValueError, TypeError) as exc:
                return self._send(400, {"error": str(exc)})
            except Exception as exc:
                return self._send(500, {"error": f"{type(exc).__name__}: {exc}"[:300]})
    return Handler


def serve(gw: RemGateway, host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    srv = ThreadingHTTPServer((host, port), make_handler(gw))
    srv.daemon_threads = True
    return srv
