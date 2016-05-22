import collections
import hashlib

User = collections.namedtuple("User", ["username", "password"])

_users = {}


def load_users():
    global _users
    _users = {}

    # Add a single test user
    username = "andreea"
    password = "example"
    sha = hashlib.sha256()
    sha.update(password.encode("utf-8"))
    user = User(username, sha.hexdigest())

    _users[user] = "Andreea Lucau"


def get_user_for_credentials(username, password):
    sha = hashlib.sha256()
    sha.update(password.encode("utf-8"))
    user = User(username, sha.hexdigest())

    return _users.get(user)
