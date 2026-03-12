#!/usr/bin/env python3
"""
WIGEON Custom Exceptions
Structured error handling for the WIGEON data integration agent
"""


class WigeonError(Exception):
    """Base exception for all WIGEON errors"""

    def __init__(self, message: str, details: str = None):
        self.details = details
        super().__init__(message)

    def __str__(self):
        msg = super().__str__()
        if self.details:
            msg += f"\n  Details: {self.details}"
        return msg


class ParseError(WigeonError):
    """Raised when file parsing fails"""

    def __init__(
        self, message: str, file_path: str = None, file_format: str = None, line_number: int = None, details: str = None
    ):
        self.file_path = file_path
        self.file_format = file_format
        self.line_number = line_number
        parts = [message]
        if file_path:
            parts.append(f"File: {file_path}")
        if file_format:
            parts.append(f"Format: {file_format}")
        if line_number:
            parts.append(f"Line: {line_number}")
        super().__init__(" | ".join(parts), details)


class DatabaseError(WigeonError):
    """Raised when database operations fail"""

    def __init__(self, message: str, operation: str = None, table: str = None, details: str = None):
        self.operation = operation
        self.table = table
        parts = [message]
        if operation:
            parts.append(f"Operation: {operation}")
        if table:
            parts.append(f"Table: {table}")
        super().__init__(" | ".join(parts), details)


class IngestError(WigeonError):
    """Raised when file ingestion fails"""

    def __init__(self, message: str, file_path: str = None, third_party: str = None, details: str = None):
        self.file_path = file_path
        self.third_party = third_party
        parts = [message]
        if file_path:
            parts.append(f"File: {file_path}")
        if third_party:
            parts.append(f"Third-party: {third_party}")
        super().__init__(" | ".join(parts), details)


class ExportError(WigeonError):
    """Raised when data export fails"""

    def __init__(self, message: str, output_path: str = None, format: str = None, details: str = None):
        self.output_path = output_path
        self.format = format
        parts = [message]
        if output_path:
            parts.append(f"Output: {output_path}")
        if format:
            parts.append(f"Format: {format}")
        super().__init__(" | ".join(parts), details)


class ValidationError(WigeonError):
    """Raised when data validation fails"""

    def __init__(self, message: str, field: str = None, value: str = None, details: str = None):
        self.field = field
        self.value = value
        parts = [message]
        if field:
            parts.append(f"Field: {field}")
        if value:
            parts.append(f"Value: {value}")
        super().__init__(" | ".join(parts), details)
