"""
Application-wide custom exception classes mapping logical domain errors.
"""
class BankSaathiException(Exception):
    """Base exception class for all errors in the application."""
    pass

class DatabaseException(BankSaathiException):
    """Database-related failures."""
    pass

class ValidationException(BankSaathiException):
    """Validation errors."""
    pass
