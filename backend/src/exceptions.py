from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class ThreatSysException(Exception):
    """Base exception for application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UserNotFoundException(ThreatSysException):
    def __init__(self, user_id: str):
        super().__init__(f"User with id {user_id} not found", 404)

class UserExistsException(ThreatSysException):
    def __init__(self, email: str):
        super().__init__(f"User with email {email} already exists", 400)

class OrganizationNotFoundException(ThreatSysException):
    def __init__(self, org_id: str):
        super().__init__(f"Organization with id {org_id} not found", 404)

class OrganizationExistsException(ThreatSysException):
    def __init__(self, name: str):
        super().__init__(f"Organization with name {name} already exists", 400)

class IOCNotFoundException(ThreatSysException):
    def __init__(self, field: str, value: str):
        super().__init__(f"IOC with {field} '{value}' not found", 404)

async def threatsys_exception_handler(request: Request, exc: ThreatSysException):
    logger.error(
        "ThreatSys exception occurred",
        extra={
            "message": exc.message,
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        }
    )
    if exc.status_code == 404:
        user_message = "Requested resource not found."
    elif exc.status_code == 400:
        user_message = "Bad request."
    else:
        user_message = "Internal server error."

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": user_message}
    )

def setup_handlers(app):
    app.add_exception_handler(ThreatSysException, threatsys_exception_handler)