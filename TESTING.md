# Testing Mode Documentation

## 🧪 Default Test User Configuration

This project includes a **testing mode** that automatically logs in a default user for easy feature testing and development.

### Default Test User Credentials

- **Username**: `manav`
- **Email**: `manav@test.com`
- **Password**: `manav123`
- **Role**: `admin`
- **Name**: `Manav`

## 🚀 How It Works

### In Testing Mode (Default)

When `TESTING_MODE=true` (default):

1. **Automatic Authentication**: All protected endpoints automatically use the default test user "Manav"
2. **No Token Required**: You don't need to authenticate in Swagger UI
3. **Instant Testing**: Just click "Try it out" on any endpoint and execute
4. **Auto-Seeding**: The default user is automatically created on application startup

### Testing Mode Features

✅ **Bypass Authentication**: No need to manually login for each test
✅ **Swagger UI Ready**: Swagger automatically uses the default user
✅ **Quick Feature Testing**: Test new features without authentication friction
✅ **Database Seeding**: Default user is created if it doesn't exist

## 📝 Configuration

### Environment Variables

Add these to your `.env` file (optional - defaults are provided):

```env
# Testing Configuration
TESTING_MODE=true                          # Set to false for production
DEFAULT_TEST_USER_EMAIL=manav@test.com
DEFAULT_TEST_USER_PASSWORD=manav123
DEFAULT_TEST_USER_NAME=Manav
```

### Toggle Testing Mode

**For Development (Testing Mode ON):**
```env
TESTING_MODE=true
```

**For Production (Testing Mode OFF):**
```env
TESTING_MODE=false
```

## 🔒 Production Mode

When `TESTING_MODE=false`:

1. **Authentication Required**: All protected endpoints require valid JWT tokens
2. **Token Validation**: Proper OAuth2 token validation is enforced
3. **Manual Login**: Users must login via `/auth/token` endpoint
4. **Secure**: No automatic authentication bypass

## 📖 Usage Examples

### 1. Using Swagger UI (Testing Mode)

1. Start the server: `uvicorn app.main:app --reload`
2. Open Swagger UI: http://localhost:8000/docs
3. Try any protected endpoint - no authentication needed!
4. The default user "Manav" is automatically used

### 2. Manual Login (If Needed)

Even in testing mode, you can manually login:

```bash
# Login endpoint
POST /auth/token

# Form data:
username: manav@test.com
password: manav123
```

### 3. API Testing with curl

```bash
# In testing mode, no token needed (automatically uses default user)
curl http://localhost:8000/resumes

# In production mode, token required
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/resumes
```

### 4. Check Current Mode

```bash
# Check if testing mode is active
GET http://localhost:8000/

# Response includes:
{
  "API": "InterviewAstra is running successfully v1.0",
  "testing_mode": true,
  "default_user": "Manav",
  "message": "Authentication bypassed in testing mode"
}
```

## 🛡️ Security Notes

⚠️ **IMPORTANT**: 

- **Never deploy to production with `TESTING_MODE=true`**
- Testing mode bypasses all authentication
- Only use testing mode in local development
- Always set `TESTING_MODE=false` in production environments
- Use environment-specific `.env` files

## 🔧 Implementation Details

### Files Modified

1. **`app/core/config.py`**: Added testing mode configuration
2. **`app/core/dependencies.py`**: Modified `get_current_user()` to bypass auth in testing mode
3. **`app/db/init_db.py`**: Added default test user seeding
4. **`app/main.py`**: Added testing mode information to Swagger docs

### How Authentication Works

```python
# In testing mode
def get_current_user(...):
    if settings.testing_mode:
        return default_test_user  # Always return "Manav"
    else:
        # Validate JWT token
        # Return authenticated user
```

## 🎯 Benefits

- **Faster Development**: No need to authenticate for every test
- **Easier Collaboration**: Team members can test immediately
- **Better Swagger Experience**: Swagger UI "just works" without authentication
- **Flexible**: Easy to toggle between testing and production modes
- **Safe**: Clear separation between testing and production

## 🐛 Troubleshooting

### "Default test user not found" error

**Solution**: Restart the application. The user is created automatically on startup.

```bash
# Stop the server (Ctrl+C)
# Start again
uvicorn app.main:app --reload
```

### Authentication still required in testing mode

**Check**:
1. Verify `.env` has `TESTING_MODE=true`
2. Restart the application after changing `.env`
3. Check the root endpoint response to confirm mode

### Want to test real authentication

**Option 1**: Temporarily set `TESTING_MODE=false` in `.env`

**Option 2**: Create additional test users and use the `/auth/token` endpoint

## 📚 Additional Resources

- See `app/core/dependencies.py` for authentication logic
- See `app/db/init_db.py` for user seeding
- See `app/main.py` for Swagger configuration

---

**Happy Testing! 🚀**
