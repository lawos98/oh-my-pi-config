#!/usr/bin/env python3
# Modified for safe loopback feedback and passive file previews; see ../NOTICE.txt.
"""Generate and serve a review page for eval results.

Reads the workspace directory, discovers runs (directories with outputs/),
embeds all output data into a self-contained HTML page, and serves it via
a tiny HTTP server. Feedback auto-saves to feedback.json in the workspace.

Usage:
    python generate_review.py <workspace-path> [--port PORT] [--skill-name NAME]
    python generate_review.py <workspace-path> --previous-feedback /path/to/old/feedback.json

No dependencies beyond the Python stdlib are required.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import tempfile
import sys
import webbrowser
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit

MAX_FEEDBACK_BYTES = 1024 * 1024
MAX_FEEDBACK_REVIEWS = 10_000

# Files to exclude from output listings
METADATA_FILES = {"transcript.md", "user_notes.md", "metrics.json"}

# Extensions we render as inline text
TEXT_EXTENSIONS = {
    ".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".yaml", ".yml", ".xml", ".html", ".css", ".sh", ".rb", ".go", ".rs",
    ".java", ".c", ".cpp", ".h", ".hpp", ".sql", ".r", ".toml",
}

# Extensions we render as inline images. SVG/PDF/XLSX remain downloads.
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}

# MIME type overrides for common types
MIME_OVERRIDES = {
    ".svg": "image/svg+xml",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


def get_mime_type(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in MIME_OVERRIDES:
        return MIME_OVERRIDES[ext]
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"


def _path_has_symlink(path: Path) -> bool:
    current = path.absolute()
    while True:
        if current.is_symlink():
            return True
        if current.parent == current:
            return False
        current = current.parent


def _safe_regular_file(path: Path, root: Path) -> bool:
    """Allow only regular files whose resolved path remains under root."""
    if path.is_symlink() or not path.is_file():
        return False
    try:
        path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        return False
    return True


def find_runs(workspace: Path) -> list[dict]:
    """Recursively find runs without following symbolic links."""
    runs: list[dict] = []
    _find_runs_recursive(workspace, workspace, runs)
    runs.sort(key=lambda r: (r.get("eval_id", float("inf")), r["id"]))
    return runs


def _find_runs_recursive(root: Path, current: Path, runs: list[dict]) -> None:
    if current.is_symlink() or not current.is_dir():
        return

    outputs_dir = current / "outputs"
    if outputs_dir.is_dir() and not outputs_dir.is_symlink():
        run = build_run(root, current)
        if run:
            runs.append(run)
        return

    skip = {"node_modules", ".git", "__pycache__", "skill", "inputs"}
    for child in sorted(current.iterdir()):
        if child.name not in skip and child.is_dir() and not child.is_symlink():
            _find_runs_recursive(root, child, runs)


def build_run(root: Path, run_dir: Path) -> dict | None:
    """Build a run dict with prompt, outputs, and grading data."""
    prompt = ""
    eval_id = None

    # Try eval_metadata.json
    for candidate in [run_dir / "eval_metadata.json", run_dir.parent / "eval_metadata.json"]:
        if _safe_regular_file(candidate, root):
            try:
                metadata = json.loads(candidate.read_text())
                prompt = metadata.get("prompt", "")
                eval_id = metadata.get("eval_id")
            except (json.JSONDecodeError, OSError):
                pass
            if prompt:
                break

    # Fall back to transcript.md
    if not prompt:
        for candidate in [run_dir / "transcript.md", run_dir / "outputs" / "transcript.md"]:
            if _safe_regular_file(candidate, root):
                try:
                    text = candidate.read_text()
                    match = re.search(r"## Eval Prompt\n\n([\s\S]*?)(?=\n##|$)", text)
                    if match:
                        prompt = match.group(1).strip()
                except OSError:
                    pass
                if prompt:
                    break

    if not prompt:
        prompt = "(No prompt found)"

    run_id = str(run_dir.relative_to(root)).replace("/", "-").replace("\\", "-")

    # Collect output files
    outputs_dir = run_dir / "outputs"
    output_files: list[dict] = []
    if outputs_dir.is_dir() and not outputs_dir.is_symlink():
        for f in sorted(outputs_dir.iterdir()):
            if f.name not in METADATA_FILES and _safe_regular_file(f, root):
                output_files.append(embed_file(f))

    # Load grading if present
    grading = None
    for candidate in [run_dir / "grading.json", run_dir.parent / "grading.json"]:
        if _safe_regular_file(candidate, root):
            try:
                grading = json.loads(candidate.read_text())
            except (json.JSONDecodeError, OSError):
                pass
            if grading:
                break

    return {
        "id": run_id,
        "prompt": prompt,
        "eval_id": eval_id,
        "outputs": output_files,
        "grading": grading,
    }


def embed_file(path: Path) -> dict:
    """Read a file and return an embedded representation."""
    ext = path.suffix.lower()
    mime = get_mime_type(path)

    if ext in TEXT_EXTENSIONS:
        try:
            content = path.read_text(errors="replace")
        except OSError:
            content = "(Error reading file)"
        return {
            "name": path.name,
            "type": "text",
            "content": content,
        }
    elif ext in IMAGE_EXTENSIONS:
        try:
            raw = path.read_bytes()
            b64 = base64.b64encode(raw).decode("ascii")
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        return {
            "name": path.name,
            "type": "image",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }
    else:
        # Binary / unknown — base64 download link
        try:
            raw = path.read_bytes()
            b64 = base64.b64encode(raw).decode("ascii")
        except OSError:
            return {"name": path.name, "type": "error", "content": "(Error reading file)"}
        return {
            "name": path.name,
            "type": "binary",
            "mime": mime,
            "data_uri": f"data:{mime};base64,{b64}",
        }


def load_previous_iteration(workspace: Path) -> dict[str, dict]:
    """Load previous iteration's feedback and outputs.

    Returns a map of run_id -> {"feedback": str, "outputs": list[dict]}.
    """
    result: dict[str, dict] = {}

    # Load feedback only from a regular file inside the previous workspace.
    feedback_map: dict[str, str] = {}
    feedback_path = workspace / "feedback.json"
    if _safe_regular_file(feedback_path, workspace):
        try:
            data = json.loads(feedback_path.read_text())
            feedback_map = {
                r["run_id"]: r["feedback"]
                for r in data.get("reviews", [])
                if isinstance(r, dict)
                and isinstance(r.get("run_id"), str)
                and isinstance(r.get("feedback"), str)
                and r["feedback"].strip()
            }
        except (json.JSONDecodeError, OSError, KeyError, AttributeError):
            pass

    # Load runs (to get outputs)
    prev_runs = find_runs(workspace)
    for run in prev_runs:
        result[run["id"]] = {
            "feedback": feedback_map.get(run["id"], ""),
            "outputs": run.get("outputs", []),
        }

    # Also add feedback for run_ids that had feedback but no matching run
    for run_id, fb in feedback_map.items():
        if run_id not in result:
            result[run_id] = {"feedback": fb, "outputs": []}

    return result


def generate_html(
    runs: list[dict],
    skill_name: str,
    previous: dict[str, dict] | None = None,
    benchmark: dict | None = None,
) -> str:
    """Generate the complete standalone HTML page with embedded data."""
    template_path = Path(__file__).parent / "viewer.html"
    template = template_path.read_text()

    # Build previous_feedback and previous_outputs maps for the template
    previous_feedback: dict[str, str] = {}
    previous_outputs: dict[str, list[dict]] = {}
    if previous:
        for run_id, data in previous.items():
            if data.get("feedback"):
                previous_feedback[run_id] = data["feedback"]
            if data.get("outputs"):
                previous_outputs[run_id] = data["outputs"]

    embedded = {
        "skill_name": skill_name,
        "runs": runs,
        "previous_feedback": previous_feedback,
        "previous_outputs": previous_outputs,
    }
    if benchmark:
        embedded["benchmark"] = benchmark

    # Escape characters that can terminate the surrounding script element.
    data_json = json.dumps(embedded).translate(str.maketrans({
        "<": "\\u003c", ">": "\\u003e", "&": "\\u0026",
    }))

    return template.replace("/*__EMBEDDED_DATA__*/", f"const EMBEDDED_DATA = {data_json};")


# ---------------------------------------------------------------------------
# HTTP server (stdlib only, zero dependencies)
# ---------------------------------------------------------------------------


def _valid_origin(origin: str | None, server_port: int) -> bool:
    """Allow browser writes only from this loopback server."""
    if origin is None:
        return False
    try:
        parsed = urlsplit(origin)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "http"
        and parsed.username is None
        and parsed.password is None
        and hostname in {"localhost", "127.0.0.1", "::1"}
        and port == server_port
        and not parsed.path
        and not parsed.query
        and not parsed.fragment
    )


def _validate_feedback(data: object) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("reviews"), list):
        raise ValueError("Expected JSON object with a reviews list")
    reviews = data["reviews"]
    if len(reviews) > MAX_FEEDBACK_REVIEWS:
        raise ValueError("Too many reviews")
    for review in reviews:
        if not isinstance(review, dict):
            raise ValueError("Each review must be an object")
        if not isinstance(review.get("run_id"), str) or len(review["run_id"]) > 500:
            raise ValueError("Invalid review run_id")
        if not isinstance(review.get("feedback"), str) or len(review["feedback"]) > 100_000:
            raise ValueError("Invalid review feedback")
        if "timestamp" in review and (
            not isinstance(review["timestamp"], str) or len(review["timestamp"]) > 100
        ):
            raise ValueError("Invalid review timestamp")
    if data.get("status") not in {None, "in_progress", "complete"}:
        raise ValueError("Invalid feedback status")
    return data


def _atomic_write_json(path: Path, data: dict) -> None:
    if path.is_symlink():
        raise OSError("Feedback path must not be a symbolic link")
    encoded = (json.dumps(data, indent=2) + "\n").encode("utf-8")
    if len(encoded) > MAX_FEEDBACK_BYTES:
        raise ValueError("Feedback payload is too large")
    fd, temporary_name = tempfile.mkstemp(prefix=".feedback-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as temporary:
            temporary.write(encoded)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, path)
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


class ReviewHandler(BaseHTTPRequestHandler):
    """Serves the review HTML and handles feedback saves.

    Regenerates the HTML on each page load so that refreshing the browser
    picks up new eval outputs without restarting the server.
    """

    def __init__(
        self,
        workspace: Path,
        skill_name: str,
        feedback_path: Path,
        previous: dict[str, dict],
        benchmark_path: Path | None,
        *args,
        **kwargs,
    ):
        self.workspace = workspace
        self.skill_name = skill_name
        self.feedback_path = feedback_path
        self.previous = previous
        self.benchmark_path = benchmark_path
        super().__init__(*args, **kwargs)

    def _send(self, status: int, content_type: str, body: bytes) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if content_type.startswith("text/html"):
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'unsafe-inline'; "
                "style-src 'unsafe-inline'; img-src 'self' data:; "
                "connect-src 'self'; font-src 'self'; frame-src 'none'; "
                "object-src 'none'; base-uri 'none'; form-action 'self'",
            )
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if not _valid_origin("http://" + self.headers.get("Host", ""), self.server.server_port):
            self.send_error(403, "Host is not allowed")
            return
        if self.path in {"/", "/index.html"}:
            runs = find_runs(self.workspace)
            benchmark = None
            if self.benchmark_path and _safe_regular_file(self.benchmark_path, self.workspace):
                try:
                    benchmark = json.loads(self.benchmark_path.read_text())
                except (json.JSONDecodeError, OSError):
                    pass
            content = generate_html(
                runs, self.skill_name, self.previous, benchmark
            ).encode("utf-8")
            self._send(200, "text/html; charset=utf-8", content)
        elif self.path == "/api/feedback":
            data = b"{}"
            if _safe_regular_file(self.feedback_path, self.workspace):
                data = self.feedback_path.read_bytes()
            self._send(200, "application/json", data)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        if not _valid_origin("http://" + self.headers.get("Host", ""), self.server.server_port):
            self.send_error(403, "Host is not allowed")
            return
        if self.path != "/api/feedback":
            self.send_error(404)
            return
        if not _valid_origin(self.headers.get("Origin"), self.server.server_port):
            self.send_error(403, "Origin is not allowed")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > MAX_FEEDBACK_BYTES:
                raise ValueError("Feedback payload is too large")
            data = _validate_feedback(json.loads(self.rfile.read(length)))
            _atomic_write_json(self.feedback_path, data)
            self._send(200, "application/json", b'{"ok":true}')
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            self._send(400, "application/json", json.dumps({"error": str(exc)}).encode())

    def log_message(self, format: str, *args: object) -> None:
        # Suppress request logging to keep terminal clean
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and serve eval review")
    parser.add_argument("workspace", type=Path, help="Path to workspace directory")
    parser.add_argument("--port", "-p", type=int, default=3117, help="Server port (default: 3117)")
    parser.add_argument("--skill-name", "-n", type=str, default=None, help="Skill name for header")
    parser.add_argument(
        "--previous-workspace", type=Path, default=None,
        help="Path to previous iteration's workspace (shows old outputs and feedback as context)",
    )
    parser.add_argument(
        "--benchmark", type=Path, default=None,
        help="Path to benchmark.json to show in the Benchmark tab",
    )
    parser.add_argument(
        "--static", "-s", type=Path, default=None,
        help="Write standalone HTML to this path instead of starting a server",
    )
    args = parser.parse_args()

    requested_workspace = args.workspace.expanduser()
    if _path_has_symlink(requested_workspace):
        print("Error: workspace path contains a symbolic link", file=sys.stderr)
        sys.exit(1)
    workspace = requested_workspace.resolve()
    if not workspace.is_dir():
        print(f"Error: {workspace} is not a directory", file=sys.stderr)
        sys.exit(1)

    runs = find_runs(workspace)
    if not runs:
        print(f"No runs found in {workspace}", file=sys.stderr)
        sys.exit(1)

    skill_name = args.skill_name or workspace.name.replace("-workspace", "")
    feedback_path = workspace / "feedback.json"

    previous: dict[str, dict] = {}
    if args.previous_workspace:
        requested_previous = args.previous_workspace.expanduser()
        if _path_has_symlink(requested_previous):
            print("Error: previous workspace path contains a symbolic link", file=sys.stderr)
            sys.exit(1)
        previous = load_previous_iteration(requested_previous.resolve())

    benchmark_path = None
    benchmark = None
    if args.benchmark:
        requested_benchmark = args.benchmark.expanduser()
        if _path_has_symlink(requested_benchmark):
            print("Error: benchmark path contains a symbolic link", file=sys.stderr)
            sys.exit(1)
        benchmark_path = requested_benchmark.resolve()
        if _safe_regular_file(benchmark_path, workspace):
            try:
                benchmark = json.loads(benchmark_path.read_text())
            except (json.JSONDecodeError, OSError):
                pass

    if args.static:
        static_path = args.static.expanduser().absolute()
        if _path_has_symlink(static_path) or os.path.lexists(static_path):
            print("Error: refusing unsafe or existing static output", file=sys.stderr)
            sys.exit(1)
        static_path.parent.mkdir(parents=True, exist_ok=True)
        static_path.write_text(generate_html(runs, skill_name, previous, benchmark))
        print(f"\n  Static viewer written to: {static_path}\n")
        sys.exit(0)

    handler = partial(ReviewHandler, workspace, skill_name, feedback_path, previous, benchmark_path)
    try:
        server = HTTPServer(("127.0.0.1", args.port), handler)
    except OSError as exc:
        print(f"Error: could not bind 127.0.0.1:{args.port}: {exc}", file=sys.stderr)
        sys.exit(1)
    port = server.server_address[1]

    url = f"http://localhost:{port}"
    print(f"\n  Eval Viewer")
    print(f"  ─────────────────────────────────")
    print(f"  URL:       {url}")
    print(f"  Workspace: {workspace}")
    print(f"  Feedback:  {feedback_path}")
    if previous:
        print(f"  Previous:  {args.previous_workspace} ({len(previous)} runs)")
    if benchmark_path:
        print(f"  Benchmark: {benchmark_path}")
    print(f"\n  Press Ctrl+C to stop.\n")

    webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
