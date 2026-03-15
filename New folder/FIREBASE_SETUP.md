# Firebase OAuth Setup Guide for Kharsan Constructions

This guide will help you integrate Gmail/Google OAuth authentication using Firebase.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a new project"
3. Name it: `Kharsan Constructions`
4. Follow the setup wizard and enable Google Analytics (optional)
5. Once created, go to the project settings

## Step 2: Get Firebase Credentials

1. In Firebase Console, click the gear icon → Project Settings
2. Go to the "Service Accounts" tab
3. Click "Generate New Private Key"
4. Save the JSON file securely (you'll need this)

## Step 3: Enable Google Sign-In

1. In Firebase Console, go to Authentication → Sign-in method
2. Enable "Google"
3. Add your app's domain to authorized domains
4. Configure OAuth consent screen in Google Cloud Console

## Step 4: Install Firebase Admin SDK

```bash
pip install firebase-admin
```

## Step 5: Add Firebase Credentials to Backend

1. Copy the JSON credentials file to your project folder
2. Update `backend.py` with Firebase initialization:

```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Initialize Firebase (use the path to your credentials JSON)
cred = credentials.Certificate('path/to/firebase_credentials.json')
firebase_admin.initialize_app(cred)
```

## Step 6: Web Configuration

Add this to your login/register pages for frontend integration:

```javascript
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js"></script>
<script src="https://www.gstatic.com/firebasejs/ui/4.8.1/firebase-ui-auth.js"></script>

<script>
  const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
  };
  
  firebase.initializeApp(firebaseConfig);
</script>
```

## Step 7: Backend Routes for OAuth

Add these routes to handle Google authentication:

```python
@app.route('/auth/google', methods=['POST'])
def auth_google():
    token = request.json.get('token')
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        
        # Create or update user in database
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if not user:
            username = email.split('@')[0]
            conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, 'oauth-google'))
            conn.commit()
        
        conn.close()
        session['user_id'] = uid
        session['username'] = email
        return redirect(url_for('dashboard'))
    except Exception as e:
        return render_template('login.html', error=str(e))
```

## Step 8: Testing

1. Refresh browser (F5 or Ctrl+R)
2. You should see "Login with Gmail" and "Sign up with Gmail" buttons
3. Click the Gmail button to test authentication

## Troubleshooting

**Issue: Gmail button not working**
- Check browser console for errors
- Verify Firebase credentials are correct
- Ensure Firebase SDK is loaded

**Issue: CORS errors**
- Add your domain to Firebase authorized domains
- Check CORS settings in Firebase Console

**Issue: User not created**
- Verify user creation logic in backend
- Check database connection
- Ensure users table has email field

## Security Notes

1. Never commit credentials JSON file to Git
2. Add to `.gitignore`:
   ```
   firebase_credentials.json
   *.key
   .env
   ```

3. Use environment variables for sensitive data:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   
   FIREBASE_CREDENTIALS_PATH = os.getenv('FIREBASE_CREDENTIALS_PATH')
   ```

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Google Sign-In Integration](https://developers.google.com/identity/sign-in)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)

## Support

For more help, refer to Firebase documentation or contact Firebase support.
