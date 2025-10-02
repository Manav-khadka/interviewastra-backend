# OAuth Authentication Setup Guide

## 🔐 Authentication Methods

InterviewAstra supports three authentication methods:

1. **Email/Password** - Traditional authentication
2. **Google OAuth** - Login with Google account
3. **GitHub OAuth** - Login with GitHub account

## 📋 Features

✅ **Flexible Login**: Users can login with email OR username
✅ **Multiple Providers**: Support for email, Google, and GitHub authentication
✅ **Automatic User Creation**: OAuth users are created automatically on first login
✅ **Provider Switching**: Users can link multiple auth providers to one account
✅ **Secure**: Passwords hashed with bcrypt, JWT tokens for sessions

---

## 🚀 API Endpoints

### 1. Email/Password Authentication

#### Register New User
```http
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "role": "user"
}
```

**Response:**
```json
{
  "id": "uuid",
  "username": "john@example.com",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "auth_provider": "email",
  "provider_id": null,
  "created_at": "2025-10-02T...",
  "updated_at": "2025-10-02T..."
}
```

#### Login with Email or Username
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=securePassword123
```

OR

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securePassword123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "username": "johndoe"
  }
}
```

### 2. Google OAuth

#### Login/Register with Google
```http
POST /auth/google
Content-Type: application/json

{
  "email": "user@gmail.com",
  "name": "John Doe",
  "provider_id": "google_user_id_123",
  "username": "johndoe" (optional)
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "user@gmail.com",
    "username": "johndoe",
    "auth_provider": "google"
  }
}
```

### 3. GitHub OAuth

#### Login/Register with GitHub
```http
POST /auth/github
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "provider_id": "github_user_id_123",
  "username": "johndoe" (optional)
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "user@example.com",
    "username": "johndoe",
    "auth_provider": "github"
  }
}
```

### 4. Get Current User

```http
GET /auth/me
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "id": "uuid",
  "username": "johndoe",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "auth_provider": "email",
  "provider_id": null,
  "created_at": "2025-10-02T...",
  "updated_at": "2025-10-02T..."
}
```

---

## 🔧 Frontend Integration

### Google OAuth Integration

```javascript
// 1. Initialize Google OAuth (using @react-oauth/google or similar)
import { GoogleLogin } from '@react-oauth/google';
import { jwtDecode } from 'jwt-decode';

function LoginPage() {
  const handleGoogleSuccess = async (credentialResponse) => {
    // Decode the Google JWT to get user info
    const decoded = jwtDecode(credentialResponse.credential);
    
    // Send to your backend
    const response = await fetch('http://localhost:8000/auth/google', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: decoded.email,
        name: decoded.name,
        provider_id: decoded.sub, // Google user ID
        username: decoded.email.split('@')[0] // Optional
      })
    });
    
    const data = await response.json();
    // Store the access_token
    localStorage.setItem('access_token', data.access_token);
    // Redirect to dashboard
  };

  return (
    <GoogleLogin
      onSuccess={handleGoogleSuccess}
      onError={() => console.log('Login Failed')}
    />
  );
}
```

### GitHub OAuth Integration

```javascript
// 1. Setup GitHub OAuth App at https://github.com/settings/developers
// 2. Get CLIENT_ID and CLIENT_SECRET

function LoginPage() {
  const handleGitHubLogin = () => {
    const clientId = 'YOUR_GITHUB_CLIENT_ID';
    const redirectUri = 'http://localhost:3000/auth/github/callback';
    window.location.href = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=user:email`;
  };

  // In your callback page (e.g., /auth/github/callback)
  const handleGitHubCallback = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    // Exchange code for access token (do this on your backend for security)
    // Then get user info from GitHub API
    const githubUser = await fetchGitHubUser(code);
    
    // Send to your backend
    const response = await fetch('http://localhost:8000/auth/github', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: githubUser.email,
        name: githubUser.name,
        provider_id: githubUser.id.toString(),
        username: githubUser.login
      })
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
  };

  return (
    <button onClick={handleGitHubLogin}>
      Login with GitHub
    </button>
  );
}
```

### Email/Password Login

```javascript
function LoginPage() {
  const [identifier, setIdentifier] = useState(''); // email or username
  const [password, setPassword] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    
    const formData = new URLSearchParams();
    formData.append('username', identifier); // Can be email OR username
    formData.append('password', password);
    
    const response = await fetch('http://localhost:8000/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData
    });
    
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    // Redirect to dashboard
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        placeholder="Email or Username"
        value={identifier}
        onChange={(e) => setIdentifier(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Using Protected APIs

```javascript
// Add Authorization header to all protected requests
const fetchProtectedData = async () => {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/resumes', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const data = await response.json();
  return data;
};
```

---

## 🛠️ Setup Instructions

### Google OAuth Setup

1. **Create Google OAuth App**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google+ API
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Add authorized redirect URIs (e.g., `http://localhost:3000`)

2. **Get Credentials**:
   - Copy `Client ID` and `Client Secret`
   - Add to your frontend environment variables

3. **Frontend Library**:
   ```bash
   npm install @react-oauth/google jwt-decode
   ```

### GitHub OAuth Setup

1. **Create GitHub OAuth App**:
   - Go to [GitHub Developer Settings](https://github.com/settings/developers)
   - Click "New OAuth App"
   - Fill in:
     - Application name: InterviewAstra
     - Homepage URL: `http://localhost:3000`
     - Authorization callback URL: `http://localhost:3000/auth/github/callback`

2. **Get Credentials**:
   - Copy `Client ID` and `Client Secret`
   - Add to your environment variables

3. **Backend Endpoint** (optional - for token exchange):
   - You can create a backend endpoint to exchange the code for a token
   - This keeps your client secret secure

---

## 🔒 Security Considerations

### 1. Password Security
- Passwords are hashed using bcrypt
- Passwords truncated to 72 bytes (bcrypt limitation)
- OAuth users have `password = NULL`

### 2. JWT Tokens
- Tokens expire after 24 hours (configurable)
- Include user email and ID in payload
- Signed with secret key from environment

### 3. OAuth Security
- Never expose OAuth client secrets in frontend
- Validate provider_id uniqueness
- Use HTTPS in production
- Implement CSRF protection

### 4. Database Security
- Unique constraints on email and username
- Enum types for auth_provider and role
- Proper indexing for performance

---

## 📊 Database Schema

```sql
-- Users table with OAuth support
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255),  -- NULL for OAuth users
    auth_provider auth_provider_enum DEFAULT 'email',
    provider_id VARCHAR(255),  -- OAuth provider's user ID
    role user_role DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Enums
CREATE TYPE auth_provider_enum AS ENUM ('email', 'google', 'github');
CREATE TYPE user_role AS ENUM ('user', 'admin');
```

---

## 🧪 Testing

### Test Email Login
```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'

# Login with email
curl -X POST http://localhost:8000/auth/token \
  -d "username=test@example.com&password=test123"

# Login with username
curl -X POST http://localhost:8000/auth/token \
  -d "username=test@example.com&password=test123"
```

### Test Google OAuth
```bash
curl -X POST http://localhost:8000/auth/google \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@gmail.com",
    "name":"Google User",
    "provider_id":"google_123456"
  }'
```

### Test GitHub OAuth
```bash
curl -X POST http://localhost:8000/auth/github \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@github.com",
    "name":"GitHub User",
    "provider_id":"github_123456",
    "username":"githubuser"
  }'
```

---

## 📝 Environment Variables

Add these to your `.env` file:

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Testing Mode
TESTING_MODE=true
DEFAULT_TEST_USER_EMAIL=manav@test.com
DEFAULT_TEST_USER_PASSWORD=manav123
DEFAULT_TEST_USER_NAME=Manav

# Database
DATABASE_URL=postgresql://user:password@localhost/dbname
```

---

## 🎯 User Flow Examples

### New User with Email
1. User registers at `/auth/register`
2. System creates user with `auth_provider='email'`
3. Password is hashed and stored
4. User can login with email or username

### New User with Google
1. User clicks "Login with Google" in frontend
2. Google OAuth flow completes
3. Frontend gets Google user data
4. Frontend sends to `/auth/google`
5. Backend creates user with `auth_provider='google'`, `password=NULL`
6. User receives JWT token

### Existing Email User Adds Google
1. User already exists with email auth
2. User tries Google OAuth with same email
3. Backend finds existing user by email
4. Updates user: `auth_provider='google'`, adds `provider_id`
5. User can now login with either method

---

## 🚨 Common Issues & Solutions

### Issue: "Email already registered"
**Solution**: User exists with that email. Use login instead of register.

### Issue: "Incorrect email/username or password"
**Solutions**:
- Check if using correct credentials
- Verify if account uses OAuth (no password)
- Ensure password is correct

### Issue: OAuth user can't login with password
**Solution**: OAuth users (Google/GitHub) don't have passwords. They must use OAuth flow.

### Issue: Username already taken
**Solution**: System auto-generates unique username for OAuth users. Frontend can allow user to change it later.

---

## 📚 Additional Resources

- [FastAPI OAuth2](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [GitHub OAuth Documentation](https://docs.github.com/en/developers/apps/building-oauth-apps)
- [JWT.io](https://jwt.io/) - Debug JWT tokens

---

**Happy Authenticating! 🔐**
