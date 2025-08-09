# RBAC System Setup Guide

This guide will help you set up and run the RBAC (Role-Based Access Control) system.

## Prerequisites

1. **Python 3.13+** - Make sure you have Python 3.13 or higher installed
2. **PostgreSQL** - Install and configure PostgreSQL database
3. **UV** - Install UV package manager (recommended) or use pip

## Quick Setup

### 1. Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL container
docker run --name rbac-postgres \
  -e POSTGRES_DB=rbac_db \
  -e POSTGRES_USER=rbac_user \
  -e POSTGRES_PASSWORD=rbac_password \
  -p 5432:5432 \
  -d postgres:15
```

#### Option B: Local PostgreSQL

```bash
# Create database
createdb rbac_db
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://rbac_user:rbac_password@localhost/rbac_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME=RBAC System
DEBUG=true
```

### 4. Database Migration

```bash
# Initialize Alembic (first time only)
uv run alembic init alembic

# Create initial migration
uv run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
uv run alembic upgrade head
```

### 5. Initialize Sample Data

```bash
# Run the initialization script
uv run python -m src.rbac_version_2.init_db
```

### 6. Run the Application

```bash
# Using UV
uv run uvicorn src.rbac_version_2.main:app --reload --host 0.0.0.0 --port 8000

# Or using the run script
python run.py
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Sample Users

After running the initialization script, you'll have these sample users:

1. **Admin User**
   - Email: `admin@example.com`
   - Password: `admin123`
   - Role: `admin` (all permissions)

2. **Manager User**
   - Email: `manager@example.com`
   - Password: `manager123`
   - Role: `manager` (most permissions except organization management)

3. **Regular User**
   - Email: `user@example.com`
   - Password: `user123`
   - Role: `user` (basic view permissions)

## Testing the API

### 1. Login to get access token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123"
```

### 2. Use the access token

```bash
# Replace YOUR_ACCESS_TOKEN with the token from step 1
curl -X GET "http://localhost:8000/api/v1/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

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

### Database Migrations

```bash
# Create new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Make sure PostgreSQL is running
   - Check the DATABASE_URL in your .env file
   - Ensure the database exists

2. **Import Errors**
   - Make sure you're in the correct directory
   - Check that all dependencies are installed
   - Verify Python version (3.13+)

3. **Permission Errors**
   - Check file permissions
   - Make sure you have write access to the project directory

### Getting Help

1. Check the logs for error messages
2. Verify your environment variables
3. Ensure all dependencies are installed
4. Check the API documentation at `/docs`

## Production Deployment

For production deployment:

1. Set `DEBUG=false` in your environment
2. Use a strong `SECRET_KEY`
3. Configure proper CORS settings
4. Use a production database
5. Set up proper logging
6. Use HTTPS
7. Configure proper backup strategies

## License

This project is licensed under the MIT License.
