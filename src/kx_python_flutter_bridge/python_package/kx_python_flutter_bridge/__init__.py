"""
KX Python Flutter Bridge

A powerful and easy-to-use bridge between Python and Flutter applications using JSON-RPC.
This package provides decorators and utilities to expose Python functions to Flutter.

Usage:
    from kx_python_flutter_bridge import KX_Bridge

    @KX_Bridge(category="math")
    def add_numbers(a: float, b: float) -> float:
        return a + b
"""

# Import version
from .__version__ import __version__

# Import the decorator and main components for easy access
from .jsonrpc.function_registry import KX_Bridge, registry
from .jsonrpc.server import JsonRpcServer
from .jsonrpc.protocol import (
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcErrorResponse,
    JsonRpcError,
)

# Package metadata
__author__ = "Khader-X"
__email__ = "khader.x@example.com"
__description__ = "Python-Flutter bridge using JSON-RPC"

# Export main decorator and components
__all__ = [
    "KX_Bridge",
    "registry",
    "JsonRpcServer",
    "JsonRpcRequest",
    "JsonRpcResponse",
    "JsonRpcErrorResponse",
    "JsonRpcError",
]
