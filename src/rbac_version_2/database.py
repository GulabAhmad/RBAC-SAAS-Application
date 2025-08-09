from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

# Handle database URL with special characters in password
def get_database_url():
    """Get the database URL with proper encoding for special characters"""
    database_url = settings.database_url
    
    # If the URL contains special characters in the password, encode them
    if '@' in database_url and '://' in database_url:
        try:
            # Split the URL to handle password encoding
            protocol, rest = database_url.split('://', 1)
            if '@' in rest:
                # Find the last @ symbol (which should be the separator between user:pass and host)
                parts = rest.rsplit('@', 1)
                if len(parts) == 2:
                    user_pass, host_db = parts
                    if ':' in user_pass:
                        user, password = user_pass.split(':', 1)
                        # URL encode the password
                        encoded_password = quote_plus(password)
                        database_url = f"{protocol}://{user}:{encoded_password}@{host_db}"
        except Exception as e:
            print(f"Warning: Could not encode database URL: {e}")
            # If parsing fails, use the original URL
            pass
    
    return database_url

# Create database engine with connection retry
def create_database_engine():
    """Create database engine with proper error handling"""
    try:
        url = get_database_url()
        print(f"Connecting to database with URL: {url.replace('Gulab%40123000', '***')}")  # Hide password in logs
        return create_engine(url, pool_pre_ping=True, pool_recycle=300)
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise

# Create database engine
engine = create_database_engine()

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
