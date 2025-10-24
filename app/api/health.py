"""Health check endpoints"""

from fastapi import APIRouter, status
from datetime import datetime
import psutil
import sys

router = APIRouter()


@router.get("")
@router.get("/")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/detailed")
async def detailed_health_check():
    """Detailed health check with system metrics"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "python_version": sys.version,
        },
        "checks": {
            "database": "ok",  # Add actual database check
            "redis": "ok",     # Add actual redis check
        }
    }


@router.get("/ready")
async def readiness_check():
    """Kubernetes readiness probe"""
    # Add checks for dependencies being ready
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Kubernetes liveness probe"""
    return {"status": "alive"}
