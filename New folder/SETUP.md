# Setup Instructions - Kharsan Constructions

## Quick Start (Easy Way!)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create a `.env` File
Create a new file called `.env` in the project folder and add:

```
SECRET_KEY=my-secret-key-12345
FLASK_ENV=development
```

### Step 3: Run the Application
```bash
python backend.py
```

### Step 4: Visit the Website
Open your browser and go to:
```
http://127.0.0.1:5000/
```

### Step 5: Login
Use these credentials:
- **Username:** admin
- **Password:** admin123

---

## Complete Project Structure

```
New folder/
├── backend.py                 # Flask application
├── db.sql                     # Database schema
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (CREATE THIS)
├── .env.example              # Template for .env
├── .gitignore                # Git ignore rules
├── SECURITY_GUIDE.md         # Security information
├── FIREBASE_SETUP.md         # Firebase OAuth setup
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── index.html
    ├── dashboard.html
    ├── clients.html
    ├── projects.html
    ├── materials.html
    ├── labor.html
    ├── finances.html
    └── [other templates]
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `backend.py` | Main Flask application with all routes |
| `db.sql` | Database tables definition |
| `.env` | Your secrets (DO NOT commit to Git) |
| `.env.example` | Template showing what goes in `.env` |
| `.gitignore` | Prevents credentials from being committed |
| `requirements.txt` | Python package dependencies |

---

## Features

✅ **Authentication**
- Login/Register pages
- Gmail OAuth ready
- Secure password hashing

✅ **Dashboard**
- Project overview
- Statistics and metrics
- Quick access to all modules

✅ **Management**
- Clients management
- Projects tracking
- Materials inventory
- Labor/Workers management
- Finances & Invoicing

✅ **Design**
- Modern purple gradient theme
- Smooth animations
- Stylish Poppins & Playfair fonts
- Responsive layout

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python backend.py

# Run in production (not for development)
python backend.py

# Check if database exists
ls -la construction.db

# Delete database to reset
rm construction.db

# On Windows PowerShell:
Remove-Item construction.db -Force
```

---

## Troubleshooting

**Q: App won't start**
- Make sure you have `.env` file created
- Check that port 5000 is not in use
- Run: `python backend.py` again

**Q: Can't login**
- Use: admin / admin123
- Check if database exists
- Delete `construction.db` and restart to recreate

**Q: Port 5000 already in use**
- Close other Flask apps
- Or change port in backend.py

**Q: Database errors**
- Delete `construction.db`
- Restart the application
- Database will be recreated automatically

---

## Security Important!

🔒 **ALWAYS:**
- Keep `.env` file in `.gitignore`
- Never commit secrets to Git
- Use `.env.example` for templates only
- Change SECRET_KEY in production

**If you accidentally commit credentials:**
1. Revoke them immediately
2. Generate new ones
3. Update your `.env` file
4. Don't push again

---

## Next Steps

1. ✅ Install requirements.txt
2. ✅ Create .env file with SECRET_KEY
3. ✅ Run python backend.py
4. ✅ Visit http://127.0.0.1:5000/
5. ✅ Login with admin/admin123
6. ✅ Explore all features!

---

## Support

See these files for more details:
- `SECURITY_GUIDE.md` - Security best practices
- `FIREBASE_SETUP.md` - Gmail OAuth setup

---

That's it! You're ready to go! 🚀
