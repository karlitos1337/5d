import unittest
from datetime import datetime, timedelta
from auth.github_oauth import SessionManager

class TestSessionDoS(unittest.TestCase):
    def test_bounded_session_growth(self):
        """Verify that SessionManager enforces session limit."""
        manager = SessionManager()

        # Create 2000 sessions (limit is 1000)
        for i in range(2000):
            manager.create_session(f"session_{i}", (datetime.now() + timedelta(hours=1)).isoformat())

        # Verify limit is enforced
        self.assertLessEqual(len(manager.sessions), 1000)
        self.assertEqual(len(manager.sessions), 1000)

        # Verify oldest sessions were removed (session_0 should be gone, session_1999 should be present)
        self.assertNotIn("session_0", manager.sessions)
        self.assertIn("session_1999", manager.sessions)

        print(f"Verified fix: Stored {len(manager.sessions)} sessions (Limit: {manager.MAX_SESSIONS}).")

if __name__ == "__main__":
    unittest.main()
