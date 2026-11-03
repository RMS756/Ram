"""Local Ollama transport. The check command needs only the Python standard library."""

import argparse
import json
import re
import secrets
from http.client import HTTPConnection

MODEL = "qwen3:4b"
HOST = "127.0.0.1"
PORT = 11434


class OllamaLocal:
    def __init__(self, model=MODEL):
        self.model = model
        self.responses = 0

    def request(self, path, payload=None):
        # A literal loopback target, no proxies, redirects, credentials, or cloud fallback.
        connection = HTTPConnection(HOST, PORT, timeout=600)
        try:
            body = json.dumps(payload).encode() if payload is not None else None
            connection.request("POST" if body else "GET", path, body, {"Content-Type": "application/json"})
            response = connection.getresponse()
            data = response.read()
            if response.status != 200:
                raise RuntimeError(f"Ollama returned HTTP {response.status} for {path}: {data[:300]!r}")
            return json.loads(data)
        except (ConnectionError, TimeoutError, OSError) as exc:
            raise RuntimeError("Cannot reach local Ollama. Open Ollama on this computer and retry.") from exc
        finally:
            connection.close()

    def identity(self):
        model = next((m for m in self.request("/api/tags")["models"] if m["name"] == self.model), None)
        if model is None:
            raise ValueError(f"Download the local model first: ollama pull {self.model}")
        details = self.request("/api/show", {"model": self.model})
        if (":cloud" in self.model or any(d.get(k) for d in (model, details) for k in ("remote_host", "remote_model"))
                or details.get("details", {}).get("format") != "gguf"):
            raise ValueError("This pilot requires locally stored GGUF weights.")
        digest = model.get("digest", "").removeprefix("sha256:")
        if not re.fullmatch(r"[0-9a-f]{64}", digest) or "tools" not in details.get("capabilities", []):
            raise ValueError("The installed model must report a SHA-256 digest and tool support.")
        return {"model": self.model, "sha256": digest, "ollama_version": self.request("/api/version")["version"]}

    def complete(self, messages, tools):
        answer = self.request("/v1/chat/completions", {
            "model": self.model, "messages": messages, "tools": tools, "stream": False,
            "temperature": 0, "max_tokens": 2048,
        })
        result = answer["choices"][0]
        if result.get("finish_reason") == "length":
            raise ValueError("The model reached its output token limit before completing its turn.")
        message = result["message"]
        if message.get("role") != "assistant":
            raise ValueError("Ollama returned no assistant message.")
        self.responses += 1
        return message

    def check(self):
        identity = self.identity()
        # A fresh result forces the second response to use the tool message.
        nonce = secrets.token_hex(4)
        tools = [{"type": "function", "function": {
            "name": "get_demo_receipt", "description": "Return the receipt code from a fake bank.",
            "parameters": {"type": "object", "properties": {}, "required": []}}}]
        turns = [{"role": "user", "content":
                  "Use get_demo_receipt now. Then tell me the exact receipt code it returned."}]
        reply = self.complete(turns, tools)
        calls = reply.get("tool_calls") or []
        if len(calls) != 1 or calls[0]["function"]["name"] != "get_demo_receipt" or not calls[0].get("id"):
            raise ValueError("No matching structured tool call. Keep Ollama open and check the model tag.")
        if json.loads(calls[0]["function"]["arguments"]) != {}:
            raise ValueError("The demo tool expects no arguments.")
        turns.append({"role": "assistant", "content": reply.get("content"), "tool_calls": calls})
        turns.append({"role": "tool", "name": "get_demo_receipt", "tool_call_id": calls[0]["id"], "content": nonce})
        final = self.complete(turns, tools)
        if final.get("tool_calls") or nonce not in (final.get("content") or ""):
            raise ValueError("The model did not read back the simulated tool result.")
        return identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=MODEL)
    args = parser.parse_args()
    try:
        info = OllamaLocal(args.model).check()
    except (RuntimeError, ValueError, KeyError, IndexError, TypeError) as exc:
        parser.exit(2, f"Check failed: {exc}\n")
    print(f"PASS: {info['model']} called get_demo_receipt and read back the matching reply.")
    print("Model SHA-256:", info["sha256"], "| Ollama:", info["ollama_version"])
    print("This was a setup check. No REM banking episode was run.")


if __name__ == "__main__":
    main()
