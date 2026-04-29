# Todo API (Backend)

 Multi-user Todo API built to handle secure task management. The focus here was moving away from simple tutorials and implementing real world security patterns like JWT authorization and strict data isolation.

### Tech Stack
* **FastAPI**: Core framework
* **SQLModel**: Handling database logic and Pydantic schemas
* **SQLite**: Local data storage
* **JWT**: Secure user sessions and token based auth
* **Hashlib**: Custom PBKDF2 implementation for password hashing

### Core Features
* **Auth Flow**: Full registration and login system returning bearer tokens
* **Data Security**: Every request is verified against the `current_user`. Even with a valid token, you can't view, edit, or delete tasks belonging to other user IDs
* **Clean CRUD**: Standard endpoints for managing tasks with a focus on ownership validation

### Project Context
The goal here was to move past basic "hello world" APIs and actually figure out how real-world backends handle security. I wanted to stop using hardcoded user IDs and build a system where the server actually knows who is making the request.

Building this helped me get a better handle on:
* **Real Auth**: Implementing JWTs so the frontend doesn't have to keep track of passwords after login.
* **Security Guards**: Writing custom dependencies to check user ownership on every single database hit.
* **Data Integrity**: Using SQLModel to make sure the data coming in is exactly what the database expects.

Basically, I wanted to build something that wouldn't fall apart or leak data the second more than one person started using it.

**What's Next**: 
Build out a React frontend. The plan is to turn this API into a proper web app where you can actually log in, manage your tasks through a UI, and have everything sync up with the backend in real-time.