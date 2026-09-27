import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from src.core.security import (
        verify_password,
        get_password_hash,
        create_access_token,
        decode_access_token
    )
except ImportError:
    verify_password = None
    get_password_hash = None
    create_access_token = None
    decode_access_token = None


class TestAuth(unittest.TestCase):

    def test_password_hashing_and_verification(self):
        if verify_password is None:
            self.skipTest("passlib not installed in current environment")
        raw = "SuperSecretAI123"
        hashed = get_password_hash(raw)
        self.assertNotEqual(hashed, raw)
        self.assertTrue(verify_password(raw, hashed))
        self.assertFalse(verify_password("wrong_password", hashed))

    def test_jwt_creation_and_decoding(self):
        if create_access_token is None:
            self.skipTest("jose not installed in current environment")
        user_id = "test-usr-999"
        token = create_access_token(subject=user_id)
        self.assertIsInstance(token, str)
        
        payload = decode_access_token(token)
        self.assertIsNotNone(payload)
        self.assertEqual(payload.get("sub"), user_id)


if __name__ == "__main__":
    unittest.main()
