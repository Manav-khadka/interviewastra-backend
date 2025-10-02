"# InterviewAstra Backend

🚀 A powerful backend API for interview preparation, resume building, and job application management.

## 🎯 Features

- **Authentication System**
  - Email/Username + Password authentication
  - Google OAuth integration
  - GitHub OAuth integration
  - JWT token-based authorization
  - Testing mode for easy development

- **Resume Management**
  - Create and manage resumes
  - Multiple template support (LaTeX-based)
  - AI-enhanced content optimization

- **Job Preparation Tools**
  - Job description analysis
  - Resume analysis and feedback
  - Interview question generation (HR, Technical, DSA, Puzzles)
  - Cover letter generation
  - Email draft creation

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL database
- Gemini API key (for AI features)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
GEMINI_API_KEY=your-gemini-api-key
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Testing Mode (set to false in production)
TESTING_MODE=true
DEFAULT_TEST_USER_EMAIL=manav@test.com
DEFAULT_TEST_USER_PASSWORD=manav123
DEFAULT_TEST_USER_NAME=Manav
```

5. **Run the application**
```bash
uvicorn app.main:app --reload
```

6. **Access the API**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Root: http://localhost:8000/

## 🔐 Authentication

### Testing Mode (Default)
When `TESTING_MODE=true`:
- All protected endpoints automatically use the default user "Manav"
- No authentication needed in Swagger UI
- Perfect for rapid feature testing and development

### Default Test User
- **Username**: `manav`
- **Email**: `manav@test.com`
- **Password**: `manav123`
- **Role**: `admin`

### Login Methods
1. **Email/Password**: Login with email or username
2. **Google OAuth**: Login with Google account
3. **GitHub OAuth**: Login with GitHub account

📖 **See [AUTH_IMPLEMENTATION_COMPLETE.md](AUTH_IMPLEMENTATION_COMPLETE.md) for complete authentication guide**

## 📚 Documentation

- **[AUTH_IMPLEMENTATION_COMPLETE.md](AUTH_IMPLEMENTATION_COMPLETE.md)** - Complete authentication system overview
- **[OAUTH_SETUP.md](OAUTH_SETUP.md)** - OAuth integration guide (Google & GitHub)
- **[TESTING.md](TESTING.md)** - Testing mode documentation
- **[AUTH_QUICK_REFERENCE.md](AUTH_QUICK_REFERENCE.md)** - Quick authentication reference

## 🛠️ API Endpoints

### Authentication (`/auth`)
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login (email or username)
- `POST /auth/google` - Google OAuth login
- `POST /auth/github` - GitHub OAuth login
- `GET /auth/me` - Get current user info

### Resumes (`/resumes`)
- `GET /resumes` - List user's resumes
- `POST /resumes` - Create new resume
- `GET /resumes/{id}` - Get resume details
- `PUT /resumes/{id}` - Update resume
- `DELETE /resumes/{id}` - Delete resume

### Analysis (`/analysis`)
- `POST /analysis/resume` - Analyze resume
- `POST /analysis/job-match` - Match resume to job description

### Job Prep (`/job-prep`)
- `POST /job-prep/create` - Generate job preparation kit
- `GET /job-prep/{id}` - Get prep kit details

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/                   # Core functionality
│   │   ├── config.py          # Configuration & settings
│   │   ├── security.py        # Authentication & security
│   │   └── dependencies.py    # Dependency injection
│   ├── db/                     # Database
│   │   ├── session.py         # Database session
│   │   └── init_db.py         # Database initialization
│   ├── modules/                # Feature modules
│   │   ├── auth/              # Authentication
│   │   ├── resumes/           # Resume management
│   │   ├── analysis/          # Resume/Job analysis
│   │   └── job_prep/          # Job preparation tools
│   ├── services/               # Business logic services
│   │   ├── ai_service.py      # AI/Gemini integration
│   │   └── latex_service.py   # LaTeX processing
│   └── templates/              # LaTeX templates
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🧪 Testing

### Using Swagger UI
1. Navigate to http://localhost:8000/docs
2. In testing mode, all endpoints work without authentication
3. Try any endpoint by clicking "Try it out"

### Using curl

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"test123"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/token \
  -d "username=manav@test.com&password=manav123"
```

**Access Protected Endpoint (in production mode):**
```bash
curl http://localhost:8000/resumes \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🔒 Security

- Passwords hashed with bcrypt
- JWT tokens for authentication
- OAuth support for Google and GitHub
- Environment-based configuration
- Testing mode disabled in production

⚠️ **Important**: Always set `TESTING_MODE=false` in production!

## 🚢 Deployment

### Production Setup
1. Set environment variables:
   ```env
   TESTING_MODE=false
   JWT_SECRET_KEY=<strong-random-secret>
   DATABASE_URL=<production-database-url>
   ```

2. Run migrations:
   ```bash
   alembic upgrade head
   ```

3. Start the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license here]

## 👥 Authors

- Manav Khadka ([@Manav-khadka](https://github.com/Manav-khadka))

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Google Gemini for AI capabilities
- PostgreSQL for robust database support

---

**Happy Coding! 🎉**
" 
