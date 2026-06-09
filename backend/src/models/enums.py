from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    ANALYST = "ANALYST"
    EXECUTIVE = "EXECUTIVE"