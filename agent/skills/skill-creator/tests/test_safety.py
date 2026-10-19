"""Offline regression coverage for packaging, feedback and provider consent."""

import functools
import http.client
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import unittest
import zipfile
from http.server import HTTPServer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.package_skill import package_skill
from scripts.run_eval import ALLOW_ENV, run_single_query

spec = importlib.util.spec_from_file_location("skill_review", ROOT / "eval-viewer/generate_review.py")
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)


class SkillSafety(unittest.TestCase):
    def test_packaging_rejects_linked_and_special_files_without_creating_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "example"
            skill.mkdir()
            (skill / "SKILL.md").write_text("---\nname: example\ndescription: Example skill\n---\nBody\n")
            outside = root / "private.txt"
            outside.write_text("private data")
            link = skill / "resource.txt"
            for kind in ("symlink", "hardlink", "fifo"):
                with self.subTest(kind=kind):
                    if kind == "symlink":
                        link.symlink_to(outside)
                    elif kind == "hardlink":
                        os.link(outside, link)
                    else:
                        os.mkfifo(link)
                    self.assertIsNone(package_skill(skill, root / "output"))
                    self.assertFalse((root / "output/example.skill").exists())
                    self.assertEqual(outside.read_text(), "private data")
                    link.unlink()
            (skill / "resource.txt").write_text("approved resource")
            archive = package_skill(skill, root / "output")
            with zipfile.ZipFile(archive) as packaged:
                self.assertEqual(packaged.read("example/resource.txt"), b"approved resource")
            original = archive.read_bytes()
            self.assertIsNone(package_skill(skill, root / "output"))
            self.assertEqual(archive.read_bytes(), original)
            self.assertIsNone(package_skill(skill, skill / "output"))

    def test_feedback_requires_loopback_host_and_same_origin(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            feedback = workspace / "feedback.json"
            handler = functools.partial(review.ReviewHandler, workspace, "example", feedback, {}, None)
            server = HTTPServer(("127.0.0.1", 0), handler)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            port = server.server_port
            payload = {"reviews": [{"run_id": "one", "feedback": "Keep this result"}], "status": "complete"}
            try:
                for origin in (None, "https://untrusted.example", "http://[malformed"):
                    headers = {"Content-Type": "application/json"}
                    if origin is not None:
                        headers["Origin"] = origin
                    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
                    connection.request("POST", "/api/feedback", json.dumps(payload), headers)
                    response = connection.getresponse()
                    self.assertEqual(response.status, 403)
                    response.read()
                    connection.close()
                    self.assertFalse(feedback.exists())
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
                connection.request("GET", "/", headers={"Host": f"untrusted.example:{port}"})
                response = connection.getresponse()
                self.assertEqual(response.status, 403)
                response.read()
                connection.close()
                connection = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
                connection.request("POST", "/api/feedback", json.dumps(payload), {"Origin": f"http://127.0.0.1:{port}", "Content-Type": "application/json"})
                response = connection.getresponse()
                self.assertEqual(response.status, 200)
                response.read()
                connection.close()
                self.assertEqual(json.loads(feedback.read_text()), payload)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

    def test_evaluation_without_consent_creates_no_project_command_files(self):
        previous = os.environ.pop(ALLOW_ENV, None)
        try:
            with tempfile.TemporaryDirectory() as directory:
                with self.assertRaises(PermissionError):
                    run_single_query("example query", "example", "Example", 1, directory)
                self.assertFalse((Path(directory) / ".claude").exists())
        finally:
            if previous is not None:
                os.environ[ALLOW_ENV] = previous


if __name__ == "__main__":
    unittest.main()
