class EmailMessage:
    """Helper class to create an email message."""
    def __init__(self, subject: str, body: str, to: list[str], from_email: str | None = None):
        self.subject = subject
        self.body = body
        self.to = to
        self.from_email = from_email
