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
from .python_package.kx_python_flutter_bridge.__version__ import __version__

# Import the decorator and main components for easy access
from .python_package.kx_python_flutter_bridge.jsonrpc.function_registry import (
    KX_Bridge,
    registry,
)
from .python_package.kx_python_flutter_bridge.jsonrpc.server import JsonRpcServer
from .python_package.kx_python_flutter_bridge.jsonrpc.protocol import (
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcErrorResponse,
    JsonRpcError,
)

# Package metadata
__author__ = "Khader-X"
__email__ = "contact@khaderx.com"
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
