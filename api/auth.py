import base64

# --- Credentials ---
# In a real app, store these hashed in a database. Never hardcode in production.
VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"


def check_auth(headers) -> bool:
    """
    Validates Basic Auth credentials from the Authorization header.

    Expected format:
        Authorization: Basic <base64(username:password)>

    Returns:
        True  → credentials are valid, request is allowed
        False → credentials are missing or wrong, caller should return 401
    """
    auth_header = headers.get("Authorization", "")

    # Must start with "Basic "
    if not auth_header.startswith("Basic "):
        return False

    try:
        # Decode base64 and split into username:password
        decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD

    except Exception:
        # Malformed header — treat as unauthorized
        return False