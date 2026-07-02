import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "backlink-publisher" / "SKILL.md"
FAILURE_POLICY_PATH = (
    ROOT / "skills" / "backlink-publisher" / "references" / "failure-policy.md"
)
CONTENT_PROMPT_PATH = (
    ROOT / "skills" / "backlink-publisher" / "references" / "content-subagent-prompt.md"
)


class BacklinkPublisherPolicyTests(unittest.TestCase):
    def test_failure_policy_records_reason_and_stops_current_batch(self):
        policy = FAILURE_POLICY_PATH.read_text(encoding="utf-8")
        skill = SKILL_PATH.read_text(encoding="utf-8")
        content_prompt = CONTENT_PROMPT_PATH.read_text(encoding="utf-8")
        combined = f"{policy}\n{skill}\n{content_prompt}"

        self.assertIn("把 `error` 设置为一句简短原因", policy)
        self.assertIn("停止处理后续队列项", policy)
        self.assertIn("保留当前 Chrome 标签页", policy)
        self.assertIn("停止本轮任务", combined)
        self.assertNotIn("继续处理当前 batch 中的下一个 `pending` 队列项", combined)
        self.assertNotIn("然后继续下一个队列项", combined)


if __name__ == "__main__":
    unittest.main()
