# Server (Flask + SQLAlchemy)

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
python -m main
```

The API endpoint domains available:

- users - crud users, roles and cars
- bookings - crud bookings
- parkings - crud parkings
- 
The SQLite DB file `app.db` will be created in folder "db" if not changed in .env file.`
