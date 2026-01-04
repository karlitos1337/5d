
import unittest
from datetime import datetime, timedelta
from auth.github_oauth import SessionManager

class TestSessionManagerSecurity(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()
        # Reduce limit for testing
        self.manager.MAX_SESSIONS = 10

    def test_session_limit_enforcement(self):
        """Test that session limit is strictly enforced."""
        # Create sessions up to limit
        for i in range(15):
            token = f"session_{i}"
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            self.manager.create_session(token, expires_at)

        # Should not exceed limit (might be less due to batch cleanup)
        self.assertLessEqual(len(self.manager.sessions), self.manager.MAX_SESSIONS)

        # Verify cleanup happened (batch cleanup removes 10% extra)
        # 10 limit -> triggers cleanup at 10.
        # Logic: if >= MAX: delete (len - MAX + MAX//10)
        # if len=10, MAX=10: delete (10 - 10 + 1) = 1.
        # So it should be around 9 or 10.
        # Let's just verify it is <= MAX_SESSIONS
        self.assertLessEqual(len(self.manager.sessions), self.manager.MAX_SESSIONS)

    def test_cleanup_expired_sessions(self):
        """Test that expired sessions are prioritized for cleanup."""
        # Add 5 expired sessions
        for i in range(5):
            token = f"expired_{i}"
            # Expired 1 hour ago
            expires_at = (datetime.now() - timedelta(hours=1)).isoformat()
            self.manager.create_session(token, expires_at)

        # Add 5 valid sessions
        for i in range(5):
            token = f"valid_{i}"
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            self.manager.create_session(token, expires_at)

        self.assertEqual(len(self.manager.sessions), 10)

        # Add one more session to trigger cleanup
        self.manager.create_session("trigger", (datetime.now() + timedelta(hours=1)).isoformat())

        # Expired sessions should be gone first
        count_expired = sum(1 for k in self.manager.sessions if k.startswith("expired_"))
        self.assertEqual(count_expired, 0, "Expired sessions should be removed")

        # Valid sessions should remain
        count_valid = sum(1 for k in self.manager.sessions if k.startswith("valid_"))
        self.assertEqual(count_valid, 5, "Valid sessions should be preserved")

    def test_lru_cleanup(self):
        """Test that oldest sessions are removed if no expired sessions exist."""
        # Add 10 valid sessions with different creation times (implicitly by order)
        for i in range(10):
            token = f"session_{i}"
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            self.manager.create_session(token, expires_at)
            # Ensure unique timestamps if fast

        # Add one more
        self.manager.create_session("new_session", (datetime.now() + timedelta(hours=1)).isoformat())

        # Oldest session (session_0) should be gone
        self.assertNotIn("session_0", self.manager.sessions)
        self.assertIn("new_session", self.manager.sessions)

if __name__ == "__main__":
    unittest.main()
