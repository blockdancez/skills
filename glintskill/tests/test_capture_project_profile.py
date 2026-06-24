import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from unittest import mock


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "project-profile-capture"
    / "scripts"
    / "capture_project_profile.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("capture_project_profile", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CaptureProjectProfileTests(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_slug_prefers_product_title(self):
        data = {
            "product": {"title": "Launch Kit Pro"},
            "metadata": {"title": "Ignored Title", "ogSiteName": "Ignored Site"},
        }

        self.assertEqual(self.module.project_slug(data, "https://example.com"), "launch-kit-pro")

    def test_slug_falls_back_to_domain(self):
        self.assertEqual(
            self.module.project_slug({"metadata": {}}, "https://www.Example-Tool.com/pricing"),
            "example-tool-com",
        )

    def test_extracts_logo_and_screenshot_urls(self):
        data = {
            "branding": {
                "logo": "https://example.com/logo.svg",
                "images": {"logo": "https://example.com/other.svg"},
            },
            "screenshot": "https://example.com/screenshot.png",
        }

        self.assertEqual(self.module.logo_url(data), "https://example.com/logo.svg")
        self.assertEqual(self.module.screenshot_url(data), "https://example.com/screenshot.png")

    def test_logo_url_falls_back_to_branding_favicon_and_metadata(self):
        self.assertEqual(
            self.module.logo_url({"branding": {"images": {"favicon": "https://example.com/favicon.png"}}}),
            "https://example.com/favicon.png",
        )
        self.assertEqual(
            self.module.logo_url({"metadata": {"favicon": "https://example.com/meta-logo.png"}}),
            "https://example.com/meta-logo.png",
        )

    def test_resolves_api_key_from_cli_then_script_then_environment(self):
        with mock.patch.object(self.module, "HARDCODED_FIRECRAWL_API_KEY", "fc-script"):
            with mock.patch.dict("os.environ", {"FIRECRAWL_API_KEY": "fc-env"}):
                self.assertEqual(self.module.resolve_api_key("fc-cli"), "fc-cli")
                self.assertEqual(self.module.resolve_api_key(None), "fc-script")

        with mock.patch.object(self.module, "HARDCODED_FIRECRAWL_API_KEY", ""):
            with mock.patch.dict("os.environ", {"FIRECRAWL_API_KEY": "fc-env"}):
                self.assertEqual(self.module.resolve_api_key(None), "fc-env")

    def test_default_screenshot_format_captures_first_viewport_only(self):
        screenshot_formats = [
            item
            for item in self.module.DEFAULT_FORMATS
            if isinstance(item, dict) and item.get("type") == "screenshot"
        ]

        self.assertEqual(screenshot_formats, [{"type": "screenshot", "fullPage": False}])

    def test_writes_profile_outputs_and_records_missing_product_warning(self):
        data = {
            "markdown": "# Hero\n\nBody copy",
            "summary": "A short project summary.",
            "metadata": {
                "title": "Example Tool",
                "description": "Metadata description",
                "sourceURL": "https://example.com",
            },
            "branding": {
                "logo": "https://example.com/logo.svg",
                "colors": {"primary": "#111111"},
            },
            "screenshot": "https://example.com/screenshot.png",
        }

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "example-tool"
            result = self.module.write_outputs(
                data=data,
                source_url="https://example.com",
                output_dir=output_dir,
                raw_response={"success": True, "data": data},
                logo_path=None,
                screenshot_path=None,
                warnings=[],
            )

            profile = (output_dir / "profile.md").read_text()
            metadata = json.loads((output_dir / "metadata.json").read_text())

        self.assertEqual(result["project_name"], "Example Tool")
        self.assertIn("A short project summary.", profile)
        self.assertIn("Product data was not returned by Firecrawl.", metadata["warnings"])
        self.assertEqual(metadata["assets"]["logo_url"], "https://example.com/logo.svg")
        self.assertEqual(metadata["assets"]["screenshot_url"], "https://example.com/screenshot.png")

    def test_cli_reports_firecrawl_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            stderr = io.StringIO()
            with mock.patch.object(
                self.module,
                "call_firecrawl",
                side_effect=RuntimeError("Firecrawl request failed: HTTP 403: blocked"),
            ):
                with redirect_stderr(stderr):
                    code = self.module.cli(["https://example.com", "--project-root", tmp])

        self.assertEqual(code, 1)
        self.assertIn("Error: Firecrawl request failed: HTTP 403: blocked", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
