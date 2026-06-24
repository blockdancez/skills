import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "backlink-publisher"
    / "scripts"
    / "validate_backlinks_json.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("validate_backlinks_json", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def valid_document():
    return {
        "version": 1,
        "default_login_method": "google",
        "requires_logged_in_chrome": True,
        "submit_policy": "auto_submit_free_listings",
        "items": [
            {
                "id": "example-tool",
                "platform_name": "Example Tool",
                "url": "https://example.com/?ref=mkdollar.com",
                "free": True,
                "status": "pending",
                "login_method": "google",
                "notes": "",
                "last_attempt_at": None,
                "result_url": None,
                "error": None,
            }
        ],
    }


class ValidateBacklinksJsonTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_valid_document_passes(self):
        self.assertEqual(self.module.validate_document(valid_document()), [])

    def test_duplicate_url_fails(self):
        data = valid_document()
        second = dict(data["items"][0])
        second["id"] = "example-tool-two"
        data["items"].append(second)

        errors = self.module.validate_document(data)

        self.assertTrue(any("url duplicates" in error for error in errors))

    def test_invalid_status_fails(self):
        data = valid_document()
        data["items"][0]["status"] = "done"

        errors = self.module.validate_document(data)

        self.assertTrue(any("status must be one of" in error for error in errors))

    def test_missing_required_field_fails(self):
        data = valid_document()
        del data["items"][0]["result_url"]

        errors = self.module.validate_document(data)

        self.assertIn("items[0].result_url is required", errors)

    def test_cli_validates_file(self):
        data = valid_document()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "backlinks.json"
            path.write_text(json.dumps(data), encoding="utf-8")

            code = self.module.cli([str(path)])

        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
