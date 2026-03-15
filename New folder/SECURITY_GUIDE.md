# Security Guide - Handling Credentials Properly

## ⚠️ Important: Never commit credentials to GitHub!

If GitHub detected exposed credentials, follow these steps immediately:

### Step 1: Revoke Exposed Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Regenerate your service account keys
3. Delete the old credentials
4. Do the same for Firebase

### Step 2: Clean Git History
If you've already committed credentials:

```bash
# Option A: Remove from current commit only
git rm --cached *-credentials.json
git commit -m "Remove exposed credentials"

# Option B: Remove from entire history (nuclear option)
git filter-branch --tree-filter 'rm -f *-credentials.json' HEAD
```

### Step 3: Set Up Environment Variables

#### Windows (PowerShell)
```powershell
$env:SECRET_KEY = "your-secret-key"
$env:FIREBASE_CREDENTIALS_PATH = "C:\path\to\firebase-credentials.json"
```

#### Windows (Command Prompt)
```cmd
set SECRET_KEY=your-secret-key
set FIREBASE_CREDENTIALS_PATH=C:\path\to\firebase-credentials.json
```

#### Linux/Mac
```bash
export SECRET_KEY="your-secret-key"
export FIREBASE_CREDENTIALS_PATH="/path/to/firebase-credentials.json"
```

### Step 4: Update Backend Code

Install python-dotenv:
```bash
pip install python-dotenv
```

Update `backend.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

# Use environment variables
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')

# Initialize Firebase conditionally
if FIREBASE_CREDENTIALS_PATH:
    import firebase_admin
    from firebase_admin import credentials
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
```

### Step 5: Create .env File (Local Only)
Create a `.env` file in your project root:
```
SECRET_KEY=your-actual-secret-key
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
GOOGLE_CLIENT_ID=your-id
GOOGLE_CLIENT_SECRET=your-secret
```

**NEVER COMMIT THIS FILE** - it's in `.gitignore`

### Step 6: Share Configuration with Team
Use `.env.example` instead:
```bash
# Team members copy this and fill in their own values
cp .env.example .env
```

### Step 7: GitHub Repository Settings
1. Go to repository Settings → Security → Secret scanning
2. Enable "Push protection"
3. Review all detected secrets
4. Mark false positives if any

## File Structure
```
project/
├── .gitignore              # Ignores credentials
├── .env.example            # Template (safe to commit)
├── .env                    # Actual values (NOT committed)
├── firebase-credentials.json  # NOT committed
├── backend.py              # Uses environment variables
├── db.sql
└── templates/
```

## Best Practices

✅ **DO:**
- Use environment variables for sensitive data
- Keep credentials in `.env` (local only)
- Use `.env.example` for templates
- Rotate credentials regularly
- Use `.gitignore` for sensitive files

❌ **DON'T:**
- Commit credentials to Git
- Share credentials in code
- Put secrets in version control
- Use the same credentials for development and production
- Push `.env` files

## For Deployment (Production)

Use platform-specific secret management:
- **Heroku**: Config Vars
- **AWS**: Secrets Manager
- **Google Cloud**: Secret Manager
- **Azure**: Key Vault
- **Docker**: Secrets or environment variables

## Emergency: Credentials Leaked

1. **Immediately revoke** the exposed credentials
2. **Delete** from Git history using `git filter-branch`
3. **Force push** to repository (carefully!)
4. **Generate new** credentials
5. **Regenerate** all tokens/keys

## Resources
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP: Secrets Management](https://owasp.org/www-community/Secrets_Management)
- [12 Factor App: Config](https://12factor.net/config)

## Questions?
Always err on the side of caution with credentials. When in doubt, treat it as a secret!
