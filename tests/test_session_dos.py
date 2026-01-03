import unittest
from datetime import datetime, timedelta
from auth.github_oauth import SessionManager

class TestSessionDoS(unittest.TestCase):
    def test_session_limit_enforced(self):
        """Verify that sessions are limited to MAX_SESSIONS."""
        manager = SessionManager()
        # Reduce max sessions for test speed
        manager.MAX_SESSIONS = 10

        # Add 20 sessions (10 more than limit)
        for i in range(20):
            token = f"session_{i}"
            # Ensure different creation times for predictable eviction
            # Although loop is fast, we rely on stable sort or slight time diffs if we used sleep
            # But ISO string sort is fine if created_at is unique enough or implementation is stable.
            # To be safe, we can mock time or just rely on insertion order if py dict.
            # But the code sorts by `created_at` string. If execution is too fast, they might have same timestamp.
            # Let's ensure we just test the count for now.
            expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
            manager.create_session(token, expires_at)

        self.assertEqual(len(manager.sessions), 10)

    def test_cleanup_logic_working(self):
        """Verify that expired sessions are automatically cleaned up on new creation."""
        manager = SessionManager()

        # Add an expired session
        expired_token = "expired"
        # Expired 1 hour ago
        expired_time = (datetime.now() - timedelta(hours=1)).isoformat()

        # We need to manually inject it or force create_session to accept it (create_session sets created_at to NOW)
        # create_session takes expires_at as arg.
        manager.create_session(expired_token, expired_time)

        # At this point, it is in the dict
        self.assertIn(expired_token, manager.sessions)

        # Add a new session. This should trigger cleanup.
        new_token = "new"
        new_time = (datetime.now() + timedelta(hours=1)).isoformat()
        manager.create_session(new_token, new_time)

        # expired_token should be gone
        self.assertNotIn(expired_token, manager.sessions)
        # new_token should be there
        self.assertIn(new_token, manager.sessions)

    def test_eviction_policy(self):
        """Verify that oldest session is evicted when full."""
        manager = SessionManager()
        manager.MAX_SESSIONS = 2

        # Add session 1
        manager.create_session("s1", (datetime.now() + timedelta(hours=1)).isoformat())
        # Cheat to make s1 older
        manager.sessions["s1"]["created_at"] = "2000-01-01T00:00:00"

        # Add session 2
        manager.create_session("s2", (datetime.now() + timedelta(hours=1)).isoformat())
        # Cheat to make s2 newer
        manager.sessions["s2"]["created_at"] = "2099-01-01T00:00:00"

        self.assertEqual(len(manager.sessions), 2)

        # Add session 3 (should trigger eviction of s1)
        manager.create_session("s3", (datetime.now() + timedelta(hours=1)).isoformat())

        self.assertEqual(len(manager.sessions), 2)
        self.assertNotIn("s1", manager.sessions)
        self.assertIn("s2", manager.sessions)
        self.assertIn("s3", manager.sessions)
