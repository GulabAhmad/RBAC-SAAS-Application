# RBAC Version 2 - Role-Based Access Control System

A comprehensive Role-Based Access Control (RBAC) system built with FastAPI and PostgreSQL. This system provides a complete solution for managing organizations, users, roles, and permissions with JWT-based authentication, email verification, and password reset functionality.

## Features

- **Organizations**: Multi-tenant support with organization-based isolation
- **Users**: User management with email-based authentication
- **Roles**: Role-based access control with organization-specific roles
- **Permissions**: Granular permission system for fine-grained access control
- **Authentication**: JWT-based authentication with secure password hashing
- **Email Verification**: Email verification with 6-digit codes via SMTP
- **Password Reset**: Secure password reset with email verification
- **Authorization**: Middleware-based authorization with permission checking
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Database Migrations**: Alembic-based database migrations
- **Type Safety**: Full type hints and Pydantic validation

## Project Structure

```
src/rbac_version_2/
├── __init__.py              # Main entry point
├── main.py                  # FastAPI application
├── config.py               # Configuration settings
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── auth.py                 # Authentication utilities
├── email_service.py        # Email service for verification and reset
├── middleware.py           # Authorization middleware
├── crud.py                 # CRUD operations
└── routers/                # API routers
    ├── __init__.py
    ├── auth.py             # Authentication endpoints
    ├── organizations.py    # Organization management
    ├── users.py           # User management
    ├── roles.py           # Role management
    └── permissions.py     # Permission management
```

## Database Schema

### Tables

1. **organizations**
   - `id` (PK) - Primary key
   - `name` - Organization name
   - `created_at` - Creation timestamp

2. **users**
   - `id` (PK) - Primary key
   - `organization_id` (FK) - Reference to organizations
   - `first_name` - User's first name
   - `last_name` - User's last name
   - `email` - Unique email address
   - `hashed_password` - Hashed password
   - `role_id` (FK) - Reference to roles
   - `is_email_verified` - Email verification status
   - `email_verification_code` - Email verification code
   - `email_verification_expires` - Email verification expiry
   - `password_reset_code` - Password reset code
   - `password_reset_expires` - Password reset expiry
   - `created_at` - Creation timestamp

3. **roles**
   - `id` (PK) - Primary key
   - `name` - Role name
   - `organization_id` (FK) - Reference to organizations
   - `created_at` - Creation timestamp

4. **permissions**
   - `id` (PK) - Primary key
   - `name` - Permission name
   - `description` - Permission description

5. **role_permissions** (Association table)
   - `role_id` (FK) - Reference to roles
   - `permission_id` (FK) - Reference to permissions

## Setup Instructions

### Prerequisites

- Python 3.13+
- PostgreSQL database
- UV package manager
- Gmail account for SMTP (or other SMTP provider)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rbac-version-2
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database settings
   DATABASE_URL=postgresql://user:password@localhost/rbac_db
   
   # JWT settings
   JWT_SECRET_KEY=your-secret-key-here
   JWT_ALGORITHM=HS256
   JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
   JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
   
   # Email settings
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   EMAIL_SMTP_SERVER=smtp.gmail.com
   EMAIL_SMTP_PORT=465
   ```

4. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uv run python run.py
   ```

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/register` - Register a new user with email verification
- `POST /api/v1/auth/verify-email` - Verify email with 6-digit code
- `POST /api/v1/auth/login` - Login with email and password
- `POST /api/v1/auth/refresh-token` - Refresh access token
- `POST /api/v1/auth/forgot-password` - Request password reset
- `POST /api/v1/auth/verify-reset-code` - Verify password reset code
- `POST /api/v1/auth/reset-password` - Reset password with code

### User Registration Flow

1. **Register User**
   ```json
   POST /api/v1/auth/register
   {
     "first_name": "John",
     "last_name": "Doe",
     "email": "john.doe@example.com",
     "password": "securepassword",
     "confirm_password": "securepassword",
     "organization_name": "Acme Corp"
   }
   ```

2. **Verify Email**
   ```json
   POST /api/v1/auth/verify-email
   {
     "email": "john.doe@example.com",
     "verification_code": "123456"
   }
   ```

3. **Login**
   ```json
   POST /api/v1/auth/login
   {
     "username": "john.doe@example.com",
     "password": "securepassword"
   }
   ```

### Password Reset Flow

1. **Request Password Reset**
   ```json
   POST /api/v1/auth/forgot-password
   {
     "email": "john.doe@example.com"
   }
   ```

2. **Verify Reset Code**
   ```json
   POST /api/v1/auth/verify-reset-code
   {
     "email": "john.doe@example.com",
     "reset_code": "123456"
   }
   ```

3. **Reset Password**
   ```json
   POST /api/v1/auth/reset-password
   {
     "email": "john.doe@example.com",
     "reset_code": "123456",
     "new_password": "newpassword",
     "confirm_password": "newpassword"
   }
   ```

## Email Configuration

The system uses SMTP for sending verification and password reset emails. Configure your email settings in the `.env` file:

```env
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password  # Use App Password for Gmail
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=465
```

### Gmail Setup

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate a new app password for "Mail"
3. Use the generated password in your `.env` file

## Security Features

- **Password Hashing**: Bcrypt-based password hashing
- **JWT Tokens**: Secure JWT-based authentication with access and refresh tokens
- **Email Verification**: Required email verification before login
- **Password Reset**: Secure password reset with email verification
- **Rate Limiting**: Built-in rate limiting for security endpoints
- **CORS**: Configurable CORS settings
- **Input Validation**: Pydantic-based input validation
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run isort src/
```

### Type Checking

```bash
uv run mypy src/
```

## License

This project is licensed under the MIT License.
