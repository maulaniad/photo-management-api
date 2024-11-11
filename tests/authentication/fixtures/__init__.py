from os.path import dirname, join


CURRENT_DIR = dirname(__file__)

AUTHENTICATION_FIXTURES = [
    join(CURRENT_DIR, "user.json"),
    join(CURRENT_DIR, "profile.json"),
]
