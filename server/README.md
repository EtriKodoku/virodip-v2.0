# Server (Flask + Peewee)

Quick setup and run instructions (Windows PowerShell):

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
python main.py
```

The API endpoints available:

- POST /users - create user
- GET /users - list users
- GET /users/<id> - get user
- PUT /users/<id> - update user
- DELETE /users/<id> - delete user

The SQLite DB file `app.db` will be created next to the server code.`
