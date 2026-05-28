import base64

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"

def check_auth(headers) -> bool:
    auth_header = headers.get("Authorization", "")
    if not auth_header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username == VALID_USERNAME and password == VALID_PASSWORD
    except Exception:
        return False