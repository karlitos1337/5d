
import unittest
from datetime import datetime, timedelta
from auth.github_oauth import SessionManager

class TestSessionManagerDoS(unittest.TestCase):
    def setUp(self):
        self.manager = SessionManager()
        # Reduce limit for testing
        self.manager.MAX_SESSIONS = 10

    def test_max_sessions_enforced(self):
        """Test that the number of sessions does not exceed the limit."""
        # Create sessions up to the limit
        for i in range(15):
            token = f"session_{i}"
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            self.manager.create_session(token, expires_at)

        self.assertLessEqual(len(self.manager.sessions), self.manager.MAX_SESSIONS)
        self.assertEqual(len(self.manager.sessions), 10)

    def test_eviction_policy(self):
        """Test that the oldest session is evicted when limit is reached."""
        # Fill sessions
        for i in range(10):
            token = f"session_{i}"
            # Ensure different timestamps (though loop is fast, datetime.now might be same, so we manually check logic)
            # Since _evict_oldest_session sorts by created_at, and we insert sequentially, session_0 is oldest.
            self.manager.create_session(token, (datetime.now() + timedelta(hours=1)).isoformat())

        # Add one more
        self.manager.create_session("session_new", (datetime.now() + timedelta(hours=1)).isoformat())

        # Check size
        self.assertEqual(len(self.manager.sessions), 10)

        # Check eviction
        self.assertNotIn("session_0", self.manager.sessions)
        self.assertIn("session_new", self.manager.sessions)

    def test_expired_cleanup_priority(self):
        """Test that expired sessions are removed before evicting valid ones."""
        # Create 9 valid sessions
        for i in range(9):
            token = f"valid_{i}"
            self.manager.create_session(token, (datetime.now() + timedelta(hours=1)).isoformat())

        # Create 1 expired session
        expired_token = "expired_session"
        expired_time = (datetime.now() - timedelta(hours=1)).isoformat()

        # We need to manually inject it or force create_session to accept past date
        # create_session sets created_at to now, so we need to mock it or just rely on expires_at logic
        # create_session accepts expires_at string.

        # But wait, create_session calls _cleanup_expired_sessions() at start.
        # So if we insert an expired session, it won't be cleaned up UNTIL the NEXT create_session call.

        # Let's manually insert an expired session to simulate time passing
        self.manager.sessions[expired_token] = {
            "expires_at": expired_time,
            "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "survey_completed": False
        }

        # Now we have 10 sessions (limit). Next create should trigger cleanup of expired one,
        # so we shouldn't need to evict a valid one.

        self.manager.create_session("new_valid", (datetime.now() + timedelta(hours=1)).isoformat())

        self.assertEqual(len(self.manager.sessions), 10)
        self.assertNotIn(expired_token, self.manager.sessions)
        # All valid sessions should still be there
        for i in range(9):
            self.assertIn(f"valid_{i}", self.manager.sessions)

if __name__ == "__main__":
    unittest.main()
