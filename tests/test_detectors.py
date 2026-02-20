import unittest
from detectors.failed_login import FailedLoginDetector
from detectors.error_detector import ErrorKeywordDetector
class TestFailedLoginDetector(unittest.TestCase):
    def test_triggers_critical_at_threshold(self):
        det=FailedLoginDetector(threshold=2, window_seconds=300, cooldown_seconds=0)
        self.assertIsNone(det.process_line("WARNING Failed login attempt from 10.0.0.5"))
        out = det.process_line("WARNING Failed login attempt from 10.0.0.5")
        self.assertIsNotNone(out)
        severity, msg, meta = out
        self.assertEqual(severity, "CRITICAL")
        self.assertIn("10.0.0.5", msg)
        self.assertEqual(meta["ip"], "10.0.0.5")
    def test_cooldown_prevents_spam(self):
        det = FailedLoginDetector(threshold=2, window_seconds=300, cooldown_seconds=9999)
        det.process_line("WARNING Failed login attempt from 10.0.0.5")
        first = det.process_line("WARNING Failed login attempt from 10.0.0.5")
        self.assertIsNotNone(first)
        second = det.process_line("WARNING Failed login attempt from 10.0.05")
        self.assertIsNone(second)
class TestErrorKeywordDetector(unittest.TestCase):
    def test_keyword_match_high(self):
        det = ErrorKeywordDetector(["Disk space critically low"])
        out = det.process_line("ERROR Disk space critically low")
        self.assertIsNotNone(out)
        severity, msg, meta=out
        self.assertEqual(severity, "HIGH")
        self.assertEqual(meta["keyword"], "Disk space critically low")
    def test_generic_error_medium(self):
        det=ErrorKeywordDetector(["Some other keyword"])
        out = det.process_line("ERROR Unauthorized access attempt")
        self.assertIsNotNone(out)
        severity, msg, meta = out
        self.assertEqual(severity, "MEDIUM")
        self.assertIsNone(meta["keyword"])
if __name__ == "__main__":
    unittest.main()


