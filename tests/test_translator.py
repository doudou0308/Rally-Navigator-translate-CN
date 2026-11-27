import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.translator import translate_json


class TranslatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "input.json"
        self.output = self.root / "output"

    def write_input(self, records):
        self.source.write_text(json.dumps(records), encoding="utf-8")

    def test_preserves_metadata_order_and_untranslated_records(self):
        records = [
            {"id": 1, "content": "Hello", "context": "menu", "flags": [1]},
            {"id": 2, "content": "Unknown", "extra": {"enabled": True}},
            {"id": 3, "content": "PDF"},
        ]
        self.write_input(records)
        with patch("src.translator.trans_map", {"Hello": "你好", "PDF": "PDF"}):
            result = translate_json(self.source, self.output)
        actual = json.loads(Path(result["output"]).read_text(encoding="utf-8"))
        expected = [dict(records[0], content="你好"), records[1], records[2]]
        self.assertEqual(actual, expected)
        self.assertEqual(result["total"], 3)
        self.assertEqual(result["translated"], 1)
        self.assertEqual(result["kept"], 2)
        self.assertEqual(result["untranslated"], [records[1]])

    def test_invalid_input_leaves_existing_output_unchanged(self):
        self.output.mkdir()
        target = self.output / "translation.json"
        target.write_text("original", encoding="utf-8")
        self.write_input([{"id": 1, "content": None}])
        with self.assertRaises(ValueError):
            translate_json(self.source, self.output)
        self.assertEqual(target.read_text(encoding="utf-8"), "original")

    def test_failed_write_leaves_existing_output_unchanged(self):
        self.output.mkdir()
        target = self.output / "translation.json"
        target.write_text("original", encoding="utf-8")
        self.write_input([{"id": 1, "content": "Hello"}])

        def interrupted_write(data, stream, **kwargs):
            stream.write("[")
            raise OSError("simulated write failure")

        with patch("src.translator.json.dump", side_effect=interrupted_write):
            with self.assertRaises(OSError):
                translate_json(self.source, self.output)
        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertEqual(list(self.output.iterdir()), [target])

    def test_success_replaces_existing_output(self):
        self.output.mkdir()
        target = self.output / "translation.json"
        target.write_text("original", encoding="utf-8")
        self.write_input([])
        result = translate_json(self.source, self.output)
        self.assertEqual(json.loads(target.read_text(encoding="utf-8")), [])
        self.assertEqual(result["total"], 0)
        self.assertEqual(list(self.output.iterdir()), [target])


if __name__ == "__main__":
    unittest.main()
