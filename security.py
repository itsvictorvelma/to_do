# ANY COMMENTS YOU SEE ARE FOR MY LEARNING 

# I found this password hashing solution here https://til.simonwillison.net/python/password-hashing-with-pbkdf2
# After some research i found that this is a decent solution to store passwords. instead of having two seperate columns in your database
# for salt and hash this format bundles everything into one string: algorithm$iterations$salt$hash
# this method allows me to increase my iterations from 260000 to 500000 if i wanted to and would still work with old users because the iteration - 
# count is stored. 

import os
from dotenv import load_dotenv
from typing import Optional
import base64 # converts binary into plain string 
import hashlib
import secrets # generates our salt randomly
import jwt
from datetime import datetime, timedelta, timezone

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

    to_encode.update({"exp": expire}) # make token expire. if a token is stolen its only valid for limited time
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") # hashing algo used specifically with JWT signature
    return encoded_jwt

def hash_password(password: str, salt: Optional[str] = None, iterations: int = ITERATIONS):
    if salt is None:
        salt = secrets.token_hex(16)

    pw_hash = hashlib.pbkdf2_hmac( # this mixes your super secret password and salt 260000 times.
        "sha256",
        password.encode("utf-8"), # turns strings into bytes
        salt.encode("utf-8"),
        iterations
    )

    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip() # Turn messy binary pw_hash into noice base64 string
    return f"{ALGORITHM}${iterations}${salt}${b64_hash}"

# Now we gots to make a way to check if a users login password is correct. 

def verify_password(plain_password: str, stored_hash: str):
    if (stored_hash or "").count("$") != 3: # we check if the stored hash has 3 dollar signs. if not its a corrupted record.
        return False
    
    algorithm, iterations, salt, b64_hash = stored_hash.split("$", 3) # we unpack the stored string into its original parts.
    iterations = int(iterations)

    compare_hash = hash_password(plain_password, salt, iterations) # we take the plain pass the user gave use and ran it through hash_password, using the same salt and iterations
    return secrets.compare_digest(stored_hash, compare_hash) # if the newly generated string matches the one in our database then bobs your uncle. 


# me tests 

if __name__ == "__main__": 

    super_secret_password = "shhh-123"

    hashed = hash_password(super_secret_password)
    print(f"Hashed String: {hashed}")

    is_correct = verify_password(super_secret_password, hashed)
    print(f"Verification (Correct PW): {is_correct}")

    is_wrong = verify_password("not-my-super-secret-password", hashed)
    print(f"Verification (Wrong PW): {is_wrong}")

