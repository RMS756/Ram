"""Scripted protocol responses only. No model or experiment result is produced by these tests."""

import json
import sys
from pathlib import Path

import pytest

pytest.importorskip("agentdojo")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments" / "live"))
import ollama_local
import run_ollama_pilot as pilot
from rem.integration.agentdojo_live import adaptation_statistics


def call(name, args, call_id):
    return {"role": "assistant", "content": None, "tool_calls": [{"id": call_id, "type": "function",
            "function": {"name": name, "arguments": json.dumps(args)}}]}


class ScriptedTransport(ollama_local.OllamaLocal):
    """Stop after seeing a sandbox transfer result or refusal. No inference."""

    def request(self, path, payload=None):
        if path == "/api/tags":
            return {"models": [{"name": self.model, "digest": "f" * 64}]}
        if path == "/api/version":
            return {"version": "scripted-fixture"}
        if path == "/api/show":
            return {"capabilities": ["tools"], "details": {"format": "gguf"}}
        assert path == "/v1/chat/completions" and payload["temperature"] == 0
        last = payload["messages"][-1]
        names = {t["function"]["name"] for t in payload["tools"]}
        if names == {"get_demo_receipt"}:
            msg = (call("get_demo_receipt", {}, "probe") if last["role"] == "user"
                   else {"role": "assistant", "content": last["content"]})
        elif last["role"] == "user":
            assert payload["messages"][0]["role"] == "system"
            msg = call("read_file", {"file_path": "bill-december-2023.txt"}, "read")
        elif last["name"] == "read_file":
            assert last["tool_call_id"] == "read"
            msg = call("send_money", {"recipient": "UK12345678901234567890", "amount": 98.7,
                                      "subject": "Car rental", "date": "2022-01-01"}, "payment")
        else:
            assert last["tool_call_id"] == "payment"
            msg = {"role": "assistant", "content": "Finished."}
        return {"choices": [{"finish_reason": "tool_calls" if msg.get("tool_calls") else "stop", "message": msg}]}


def test_model_probe_requires_a_structured_call_and_readback(monkeypatch):
    s = ScriptedTransport()
    assert s.check()["sha256"] == "f" * 64
    assert s.responses == 2
    monkeypatch.setattr(s, "complete", lambda *a: {"role": "assistant", "content": "I will use a tool."})
    with pytest.raises(ValueError, match="structured tool call"):
        s.check()


def test_paired_bill_keeps_the_authorized_details():
    suite = pilot.common.make_setup().suite
    key = "injection_bill_text"
    user = suite.get_user_task_by_id(pilot.USER)
    injections = pilot.attacked_bill(suite, pilot.LocalAgent(ScriptedTransport()), user)
    clean = suite.load_and_inject_default_environment({}).filesystem.files["bill-december-2023.txt"]
    modified = suite.load_and_inject_default_environment(injections).filesystem.files["bill-december-2023.txt"]
    assert suite.get_injection_vector_defaults()[key] in injections[key]
    assert "98.70" in clean and "98.70" in modified
    assert "UK12345678901234567890" in clean and "UK12345678901234567890" in modified
    goal = suite.get_injection_task_by_id(pilot.FOLD).GOAL
    assert goal not in clean and goal in modified
    assert modified.replace("TODO: " + goal + "\n", "") == clean


def test_local_pilot_end_to_end_scripted_transport(tmp_path):
    p = tmp_path / "run"
    assert pilot.pilot(ScriptedTransport(), p, "TEST-ONLY", expected_digest="f" * 64) == "completed"
    rows = [json.loads(line) for line in (p / "episodes.jsonl").read_text().splitlines()]
    assert len({(r["repeat"], r["injection_task"], r["configuration"]) for r in rows}) == 18
    assert all(r["model_responses"] == 3 and r["error"] is None for r in rows)
    assert all(r["security"] is None for r in rows if r["injection_task"] is None)
    assert all(a["released"] for r in rows if r["configuration"] == "B0" for a in r["audit"])
    assert any(not a["released"] for r in rows if r["configuration"] == "REM" for a in r["audit"])
    assert all(any(t["saw_injection"] for t in r["feedback_turns"]) == bool(r["injection_task"]) for r in rows)
    assert any(t["refusal_ids"] for r in rows for t in r["feedback_turns"])
    assert all(r["chats"] and r["adaptation"]["proposals"] == 2 for r in rows)
    assert all(v["attack_success"]["denominator"] == 3 for v in pilot.read(p / "summary.json")["by_condition"].values())
    with pytest.raises(FileExistsError):
        pilot.pilot(ScriptedTransport(), p, "TEST-ONLY")


def test_missing_responses_and_digest_change(tmp_path, monkeypatch):
    p = tmp_path / "failed"
    s = ScriptedTransport()
    with pytest.raises(ValueError, match="SHA-256"):
        pilot.pilot(s, p, "TEST-ONLY", expected_digest="b" * 64)
    assert not p.exists()

    def unavailable(*args):
        raise RuntimeError("fixture offline")
    monkeypatch.setattr(s, "complete", unavailable)
    with pytest.raises(RuntimeError, match="No usable model reply"):
        pilot.pilot(s, p, "TEST-ONLY")
    manifest = pilot.read(p / "manifest.json")
    assert manifest["status"] == "interrupted" and manifest["model_responses"] == 0
    summary = pilot.read(p / "summary.json")["by_condition"]["B0"]
    assert summary["errors"] == 1 and summary["benign_task_success"]["denominator"] == 0


def test_adaptation_requires_later_turn_in_same_chat():
    def row(chat, turn, tool, released):
        return dict(chat_attempt=chat, decision_point=turn, tool=tool, arguments_digest=tool,
                    label=1, released=released)
    rows = [row(1, 1, "send", False), row(1, 1, "schedule", True), row(1, 2, "send", False),
            row(1, 3, "schedule", True), row(2, 4, "schedule", True)]
    stats = adaptation_statistics(rows, ["send", "schedule"])
    assert stats["retries"] == 1 and stats["replans"] == 1 and stats["y1_released_after_refusal"] == 1


def test_local_identity_rejects_cloud():
    server = ScriptedTransport("example:cloud")
    with pytest.raises(ValueError, match="locally stored"):
        server.identity()


def test_tool_roundtrip_through_loopback_http(monkeypatch):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from threading import Thread

    script = ScriptedTransport()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.reply(None)

        def do_POST(self):
            self.reply(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))

        def reply(self, body):
            data = json.dumps(script.request(self.path, body)).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def log_message(self, *args):
            pass

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        monkeypatch.setattr(ollama_local, "PORT", server.server_port)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            assert ollama_local.OllamaLocal().check()["ollama_version"] == "scripted-fixture"
        finally:
            server.shutdown()
            thread.join()
