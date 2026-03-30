def api_error(message: str, code: str | None = None):
    """Build a consistent JSON error body for API responses."""
    body = {"error": message}
    if code:
        body["code"] = code
    return body
