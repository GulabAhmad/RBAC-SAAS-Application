#!/usr/bin/env python3
"""
Script to run the RBAC FastAPI application.
"""

import uvicorn
from src.rbac_version_2.main import app

if __name__ == "__main__":
    uvicorn.run(
        "src.rbac_version_2.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
