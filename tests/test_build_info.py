from __future__ import annotations

from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
import json
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from camera_timelapse.build_info import build_info_document
from camera_timelapse.cli import main


class BuildInfoTests(unittest.TestCase):
    def test_source_build_info_is_complete(self) -> None:
        document = build_info_document()

        self.assertEqual(document["version"], "0.2.0")
        self.assertTrue(document["branch"])
        self.assertTrue(document["commit"])
        assert isinstance(document["build_time"], str)
        datetime.fromisoformat(document["build_time"].replace("Z", "+00:00"))

    def test_cli_prints_build_info_json(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["--build-info"]), 0)

        self.assertEqual(json.loads(output.getvalue()), build_info_document())


if __name__ == "__main__":
    unittest.main()
