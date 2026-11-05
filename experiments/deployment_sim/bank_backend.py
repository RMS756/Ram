"""Simulated banking API (tool backend) for the REM deployment simulation.

A separate HTTP service holding one AgentDojo banking environment per episode (AgentDojo 0.1.35, suite
banking v1). It reproduces exactly what ``TaskSuite.run_task_with_pipeline`` does around the agent:
  open:    load_and_inject_default_environment(injections) -> user_task.init_environment -> deep copy (pre)
  execute: FunctionsRuntime(suite.tools).run_function(env, function, args) -> tool_result_to_str
  close:   AgentDojo's own utility / security checks (_check_task_result) on (model output, pre, post,
           function-call trace)
and logs every executed call, so withheld calls can be shown never to have reached it.
NO real bank, account, API or money is involved.

usage: python3 experiments/deployment_sim/bank_backend.py --port 8701
"""
from __future__ import annotations

import argparse
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

from agentdojo.agent_pipeline.tool_execution import tool_result_to_str
from agentdojo.functions_runtime import FunctionCall, FunctionsRuntime
from agentdojo.task_suite.load_suites import get_suites

SUITE = get_suites("v1")["banking"]


class Store:
    def __init__(self):
        self.eps, self.lock = {}, threading.Lock()

    def open(self, m):
        ut = SUITE.get_user_task_by_id(m["user_task_id"])
        env = SUITE.load_and_inject_default_environment(dict(m.get("injections") or {}))
        env = ut.init_environment(env)
        rec = {"meta": m, "env": env, "pre": env.model_copy(deep=True), "runtime": FunctionsRuntime(SUITE.tools),
               "executed": [], "lock": threading.Lock()}
        with self.lock:
            if m["episode_id"] in self.eps:
                raise ValueError("episode already open")
            self.eps[m["episode_id"]] = rec
        return {"episode_id": m["episode_id"]}

    def execute(self, eid, body):
        e = self.eps[eid]
        with e["lock"]:
            res, err = e["runtime"].run_function(e["env"], body["function"], dict(body.get("args") or {}))
            e["executed"].append({"function": body["function"], "args": body.get("args"), "error": err})
        return {"text": tool_result_to_str(res), "error": err}

    def close(self, eid, body):
        with self.lock:
            e = self.eps.pop(eid)
        m = e["meta"]
        trace = [FunctionCall(function=c["function"], args=dict(c.get("args") or {}), id=c.get("id"))
                 for c in body.get("function_calls", [])]
        out = body.get("model_output") or []
        ut = SUITE.get_user_task_by_id(m["user_task_id"])
        utility = SUITE._check_task_result(ut, out, e["pre"], e["env"], trace)
        if m.get("injection_task_id"):
            it = SUITE.get_injection_task_by_id(m["injection_task_id"])
            security = SUITE._check_task_result(it, out, e["pre"], e["env"], trace)
        else:
            security = True                                     # AgentDojo convention without injection
        return {"utility": bool(utility), "security": bool(security), "executed": e["executed"]}


def handler(store):
    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"
        disable_nagle_algorithm = True     # TCP_NODELAY: avoids the ~40 ms Nagle/delayed-ACK stall per response

        def log_message(self, *a):
            pass

        def _send(self, code, obj):
            data = json.dumps(obj, default=str).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            self._send(200, {"status": "ok", "open_episodes": len(store.eps)}) if self.path == "/health" \
                else self._send(404, {"error": "not found"})

        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
                p = [unquote(x) for x in self.path.strip("/").split("/")]
                if p == ["v1", "episodes"]:
                    return self._send(200, store.open(body))
                if len(p) == 4 and p[3] == "execute":
                    return self._send(200, store.execute(p[2], body))
                if len(p) == 4 and p[3] == "close":
                    return self._send(200, store.close(p[2], body))
                return self._send(404, {"error": "not found"})
            except KeyError as exc:
                return self._send(404, {"error": f"unknown episode {exc}"})
            except Exception as exc:
                return self._send(500, {"error": f"{type(exc).__name__}: {exc}"[:300]})
    return H


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, required=True)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), handler(Store()))
    srv.daemon_threads = True
    print(f"bank backend listening on {a.port}", flush=True)
    srv.serve_forever()
