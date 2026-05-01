# ANY COMMENTS YOU SEE ARE FOR MY LEARNING

# I found this password hashing solution here https://til.simonwillison.net/python/password-hashing-with-pbkdf2
# After some research i found that this is a decent solution to store passwords.
# instead of having two seperate columns in your database for salt and hash this format bundles everything into one string: algorithm$iterations$salt$hash
# this method also allows me to increase my iterations from 260000 to 500000 if i wanted to and would still work with old users because the iteration count is stored.

import os
from dotenv import load_dotenv
from typing import Optional
import base64  # converts binary into plain string
import hashlib
import secrets  # generates our salt randomly
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "pbkdf2_sha256")
ITERATIONS = int(os.getenv("ITERATIONS", 260000))
SECRET_KEY = os.getenv("SECRET_KEY")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    # make token expire. if a token is stolen its only valid for limited time
    to_encode.update({"exp": expire})

    # hashing algo used specifically with JWT signature
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def hash_password(
    password: str, salt: Optional[str] = None, iterations: int = ITERATIONS
):
    if salt is None:
        salt = secrets.token_hex(16)  # this is a random string added to the password

    pw_hash = hashlib.pbkdf2_hmac(  # this mixes your super secret password and salt 260000 times.
        "sha256",
        password.encode("utf-8"),  # turns strings into bytes
        salt.encode("utf-8"),
        iterations,
    )

    # Turn messy binary pw_hash into noice base64 string
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return f"{ALGORITHM}${iterations}${salt}${b64_hash}"


# Now we gots to make a way to check if a users login password is correct.


def verify_password(plain_password: str, stored_hash: str):
    # we check if the stored hash has 3 dollar signs. if not its a corrupted record.
    if (stored_hash or "").count("$") != 3:
        return False

    # we unpack the stored string into its original parts.
    algorithm, iterations, salt, b64_hash = stored_hash.split("$", 3)
    iterations = int(iterations)

    # we take the plain pass the user gave use and ran it through hash_password, using the same salt and iterations
    compare_hash = hash_password(plain_password, salt, iterations)

    # if the newly generated string matches the one in our database then bobs your uncle.
    return secrets.compare_digest(stored_hash, compare_hash)


# JWT TOKEN AUTH

# Looks for bearer token header in every request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_access_token(token: str):
    try:
        # uses your secret key to check if the token has been messed with.
        # if someone changed user_id in the token, signature wont match and will throw an error
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: Optional[str] = payload.get("sub")

        if user_id is None:
            return None

        return user_id

    except jwt.PyJWTError:
        return None


# me tests

if __name__ == "__main__":
    super_secret_password = "shhh-123"

    hashed = hash_password(super_secret_password)
    print(f"Hashed String: {hashed}")

    is_correct = verify_password(super_secret_password, hashed)
    print(f"Verification (Correct PW): {is_correct}")

    is_wrong = verify_password("not-my-super-secret-password", hashed)
    print(f"Verification (Wrong PW): {is_wrong}")
