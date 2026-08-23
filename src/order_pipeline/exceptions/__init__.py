"""Custom exceptions for the order pipeline."""


class OrderPipelineError(Exception):
    """Base exception for all order pipeline errors."""


class IngestionError(OrderPipelineError):
    """Raised when a file cannot be read or parsed during ingestion."""


class ValidationError(OrderPipelineError):
    """Raised when a record fails validation. (Used in the next milestone.)"""
