from pydantic import BaseModel

# user schema


# this defines what is common to all user related data.
class UserBase(BaseModel):
    username: str


# this is where the users plain password lives for a split second
class UserCreate(UserBase):
    password: str


# this is what you send back to the user when they ask who ami
class UserPublic(UserBase):
    # we do not include a password field because we want to ensure even the hashed password string never leaves our server.
    id: int


# todo schema


class TodoBase(BaseModel):
    title: str
    is_done: bool = False


class TodoCreate(TodoBase):
    pass  # when a user creates a task they only need to send the title. the db handles the id. and auth handles user_id


class TodoPublic(TodoBase):
    id: int
    user_id: int


# me tests

if __name__ == "__main__":
    # test 1: valid data
    user_data = {"username": "victor", "password": "supersecretpass"}
    user_in = UserCreate(**user_data)
    print(f"Validated User: {user_in.username}")

# test 2: missing data

# try:
#     UserCreate(username="victor")
#
# except Exception as e:
#     print(f"Validation caught error: {e}")
