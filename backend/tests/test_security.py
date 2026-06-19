import pytest
from backend.security.encryption import SecureEncryption
from backend.security.rate_limiter import RateLimiter
from backend.security.sanitizer import Sanitizer
import os
import time

@pytest.fixture(scope="module")
def secure_encryption():
    os.environ["MASTER_ENCRYPTION_KEY"] = "test-master-key"
    os.environ["ENCRYPTION_SALT"] = "c2FsdHlzYWx0eXNhbHQ=" # base64 of "saltysaltysalt"
    return SecureEncryption()

@pytest.fixture(scope="module")
def rate_limiter():
    os.environ["RATE_LIMIT"] = "5"
    os.environ["RATE_LIMIT_WINDOW"] = "10"
    return RateLimiter()

@pytest.fixture(scope="module")
def sanitizer():
    return Sanitizer()

def test_encryption_decryption(secure_encryption):
    original_data = "This is a secret message."
    encrypted_data = secure_encryption.encrypt_data(original_data)
    decrypted_data = secure_encryption.decrypt_data(encrypted_data)
    assert original_data == decrypted_data
    assert original_data != encrypted_data # Ensure it's actually encrypted

def test_password_hashing_verification(secure_encryption):
    password = "mysecretpassword"
    hashed_password = secure_encryption.hash_password(password)
    assert secure_encryption.verify_password(password, hashed_password)
    assert not secure_encryption.verify_password("wrongpassword", hashed_password)

def test_rate_limiter(rate_limiter):
    key = "test_user_ip"
    # Allow 5 requests in 10 seconds
    for _ in range(5):
        allowed, remaining = rate_limiter.is_allowed(key)
        assert allowed
    
    # 6th request should be denied
    allowed, remaining = rate_limiter.is_allowed(key)
    assert not allowed
    assert remaining == 0

    # Wait for window to pass, then it should be allowed again
    time.sleep(rate_limiter.window + 1)
    allowed, remaining = rate_limiter.is_allowed(key)
    assert allowed

def test_sanitizer_html(sanitizer):
    malicious_html = "<script>alert(\'XSS\')</script><b>Hello</b><img src=\'x\' onerror=\'alert(\'XSS\')\'>"
    clean_html = sanitizer.sanitize_html(malicious_html)
    assert "<script>" not in clean_html
    assert "onerror" not in clean_html
    assert "<b>Hello</b>" in clean_html

def test_sanitizer_text(sanitizer):
    malicious_text = "Hello <script>alert(\'XSS\')</script> World"
    clean_text = sanitizer.sanitize_text(malicious_text)
    assert "<script>" not in clean_text
    assert "Hello  World" == clean_text # bleach removes tags and content inside
