# Authentication Quick Reference

## 🎯 Available Login Methods

| Method | Endpoint | Identifier | Notes |
|--------|----------|------------|-------|
| Email/Password | `POST /auth/token` | Email OR Username | Traditional auth |
| Google OAuth | `POST /auth/google` | Email from Google | Auto-creates user |
| GitHub OAuth | `POST /auth/github` | Email from GitHub | Auto-creates user |

## 🔑 Quick Examples

### Login with Email (works in Swagger)
```
POST /auth/token
username: manav@test.com
password: manav123
```

### Login with Username (works in Swagger)
```
POST /auth/token
username: manav
password: manav123
```

### Google OAuth Login
```json
POST /auth/google
{
  "email": "user@gmail.com",
  "name": "John Doe",
  "provider_id": "google_123456"
}
```

### GitHub OAuth Login
```json
POST /auth/github
{
  "email": "user@github.com",
  "name": "John Doe",
  "provider_id": "github_123456",
  "username": "johndoe"
}
```

## ✨ Features

✅ Login with email OR username
✅ OAuth automatically creates users
✅ Users can link multiple auth providers
✅ JWT tokens include user_id and email
✅ Password-less authentication for OAuth users
✅ Automatic unique username generation

## 🧪 Testing Mode

When `TESTING_MODE=true`:
- All protected endpoints auto-login as "Manav"
- No need to authenticate in Swagger
- Perfect for rapid feature testing

## 📖 Full Documentation

See `OAUTH_SETUP.md` for complete integration guide.
