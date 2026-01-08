
import unittest
from datetime import datetime
from auth.github_oauth import SessionManager

class TestSessionDoS(unittest.TestCase):
    def test_max_sessions_limit(self):
        """Verify that SessionManager enforces MAX_SESSIONS limit."""
        manager = SessionManager()

        # Ensure we are testing the limit we expect
        self.assertEqual(manager.MAX_SESSIONS, 1000)

        # Simulate creating many sessions > MAX_SESSIONS
        # In this test we use the current time for created_at
        # To strictly verify eviction order, we should mock or vary the times,
        # but since we add them sequentially, created_at will naturally increase.
        for i in range(1200):
            manager.create_session(f"token_{i}", datetime.now().isoformat())

        # Check that the number of sessions is capped at MAX_SESSIONS
        self.assertEqual(len(manager.sessions), 1000)

        # Verify that the newest sessions are present
        self.assertIn("token_1199", manager.sessions)

        # Verify that oldest sessions were evicted
        # token_0 was the first one created, so it should be gone
        self.assertNotIn("token_0", manager.sessions)

if __name__ == "__main__":
    unittest.main()
