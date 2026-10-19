#!/usr/bin/env python3
"""Read-only OMP design setup check; never prints MCP URLs or credentials."""
import argparse
import json
import re
import stat
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError("Redirect refused")


class Client:
    def __init__(self, config, max_response_bytes=2_000_000, timeout=20):
        self.max_response_bytes = max_response_bytes
        self.timeout = timeout
        self.url = config["url"]
        parsed = urllib.parse.urlsplit(self.url)
        if parsed.hostname not in ("localhost", "127.0.0.1", "::1") or parsed.scheme not in ("http", "https"):
            raise ValueError("Doctor only supports the configured local Penpot service")
        self.headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        self.opener = urllib.request.build_opener(NoRedirect())
        self.index = 0

    def call(self, method, params=None, notification=False):
        self.index += 1
        body = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            body["params"] = params
        if not notification:
            body["id"] = self.index
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), headers=self.headers)
        with self.opener.open(req, timeout=self.timeout) as response:
            if response.headers.get("Mcp-Session-Id"):
                self.headers["Mcp-Session-Id"] = response.headers["Mcp-Session-Id"]
            if "text/event-stream" in response.headers.get("Content-Type", ""):
                size = 0
                for line in response:
                    size += len(line)
                    if size > self.max_response_bytes:
                        raise ValueError("Response limit exceeded")
                    if line.startswith(b"data:"):
                        result = json.loads(line[5:])
                        if result.get("id") == body.get("id"):
                            return result
                return {}
            data = response.read(self.max_response_bytes + 1)
            if len(data) > self.max_response_bytes:
                raise ValueError("Response limit exceeded")
            return json.loads(data) if data else {}


def canvas_status(result):
    """Require positive evidence; some MCP failures arrive as ordinary text."""
    value = result.get("result", {})
    text = "\n".join(b.get("text", "") for b in value.get("content", []) if b.get("type") == "text")
    if value.get("isError") or "error" in result:
        return {"state": "unavailable"}, True
    marker = "OMP_DESIGN_CANVAS "
    if marker in text:
        candidate = text.split(marker, 1)[1]
        # Tool responses can wrap returned strings in JSON or a result label.
        candidate = candidate.replace('\\"', '"')
        try:
            data, _ = json.JSONDecoder().raw_decode(candidate)
            ids = {key: data.get(key) for key in ("fileId", "pageId")}
            uuid = re.compile(r"^[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")
            if all(isinstance(v, str) and uuid.fullmatch(v) for v in ids.values()):
                return {"state": "connected", **ids}, False
            return {"state": "no active file/page"}, True
        except (ValueError, TypeError, AttributeError):
            pass
    if "frozen" in text.lower() or "suspended" in text.lower():
        return {"state": "browser tab frozen; focus the connected Penpot tab"}, True
    return {"state": "unverified; no valid file/page IDs returned"}, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--connect", action="store_true", help="Initialize local MCP and list tools")
    parser.add_argument("--canvas", action="store_true", help="Also read active file/page IDs; no writes")
    args = parser.parse_args()
    root = Path.home() / ".omp/agent"
    status = {"skills": {name: (root / "skills" / name / "SKILL.md").is_file()
                        for name in ("penpot-design-studio", "penpot-uiux-design", "impeccable", "ui-ux-pro-max")}}
    path = root / "mcp.json"
    failed = not all(status["skills"].values())
    try:
        config = json.loads(path.read_text())
        server = config.get("mcpServers", {}).get("penpot")
        status["penpot_configured"] = bool(server)
        status["config_private"] = stat.S_IMODE(path.stat().st_mode) & 0o077 == 0
        failed = failed or not status["penpot_configured"] or not status["config_private"]
        status["canvas"] = "not checked"
        if args.connect or args.canvas:
            if not server:
                raise ValueError("No Penpot configuration")
            client = Client(server)
            init = client.call("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                             "clientInfo": {"name": "omp-design-doctor", "version": "1.0"}})
            if "result" not in init:
                raise RuntimeError("Initialization failed")
            version = init["result"].get("protocolVersion")
            if version:
                client.headers["MCP-Protocol-Version"] = version
            client.call("notifications/initialized", notification=True)
            result = client.call("tools/list", {})
            status["mcp_tools"] = sorted(t["name"] for t in result.get("result", {}).get("tools", []))
            if not status["mcp_tools"]:
                failed = True
            if args.canvas:
                result = client.call("tools/call", {"name": "execute_code", "arguments": {
                    "code": "return 'OMP_DESIGN_CANVAS ' + JSON.stringify({ fileId: penpot.currentFile?.id ?? null, pageId: penpot.currentPage?.id ?? null });"}})
                status["canvas"], canvas_failed = canvas_status(result)
                failed = failed or canvas_failed
    except Exception as exc:
        # Exception messages can contain full request URLs. Report only type/status.
        status["error_type"] = type(exc).__name__
        status["http_status"] = getattr(exc, "code", None)
        failed = True
    print(json.dumps(status, indent=2))
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
