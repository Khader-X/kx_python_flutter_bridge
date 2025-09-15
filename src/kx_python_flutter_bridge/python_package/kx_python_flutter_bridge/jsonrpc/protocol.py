"""
JSON-RPC 2.0 Protocol Definitions for Python-Flutter Bridge

This module defines the JSON-RPC 2.0 protocol structures and error codes
used for communication between Flutter and Python via stdin/stdout.
"""

import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
from enum import IntEnum


class JsonRpcError(IntEnum):
    """Standard JSON-RPC 2.0 error codes."""

    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


@dataclass
class JsonRpcRequest:
    """JSON-RPC 2.0 request structure."""

    jsonrpc: str
    method: str
    params: Dict[str, Any]
    id: Optional[Union[str, int]]

    @classmethod
    def from_json(cls, json_str: str) -> "JsonRpcRequest":
        """Parse JSON-RPC request from JSON string."""
        try:
            data = json.loads(json_str)
            return cls(
                jsonrpc=data.get("jsonrpc", "2.0"),
                method=data["method"],
                params=data.get("params", {}),
                id=data["id"],
            )
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid JSON-RPC request: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "jsonrpc": self.jsonrpc,
            "method": self.method,
            "params": self.params,
            "id": self.id,
        }

    def toJsonString(self) -> str:
        """Convert to JSON string - Flutter compatibility method."""
        return json.dumps(self.to_dict())


@dataclass
class JsonRpcResponse:
    """JSON-RPC 2.0 response structure."""

    jsonrpc: str
    result: Any
    id: Optional[Union[str, int]]

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(
            {"jsonrpc": self.jsonrpc, "result": self.result, "id": self.id}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"jsonrpc": self.jsonrpc, "result": self.result, "id": self.id}

    @classmethod
    def fromJson(cls, json_data: Dict[str, Any]) -> "JsonRpcResponse":
        """Create from JSON data - Flutter compatibility method."""
        return cls(
            jsonrpc=json_data.get("jsonrpc", "2.0"),
            result=json_data.get("result"),
            id=json_data.get("id"),
        )

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "JsonRpcResponse":
        """Create from JSON data."""
        return cls.fromJson(json_data)


@dataclass
class JsonRpcErrorResponse:
    """JSON-RPC 2.0 error response structure."""

    jsonrpc: str
    error: Dict[str, Any]
    id: Optional[Union[str, int]]

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps({"jsonrpc": self.jsonrpc, "error": self.error, "id": self.id})

    @classmethod
    def create(
        cls,
        code: JsonRpcError,
        message: str,
        data: Any = None,
        request_id: Optional[Union[str, int]] = None,
    ) -> "JsonRpcErrorResponse":
        """Create error response."""
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data

        return cls(jsonrpc="2.0", error=error, id=request_id)

    @classmethod
    def fromJson(cls, json_data: Dict[str, Any]) -> "JsonRpcErrorResponse":
        """Create from JSON data - Flutter compatibility method."""
        return cls(
            jsonrpc=json_data.get("jsonrpc", "2.0"),
            error=json_data.get("error", {}),
            id=json_data.get("id"),
        )

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> "JsonRpcErrorResponse":
        """Create from JSON data."""
        return cls.fromJson(json_data)


def create_success_response(
    result: Any, request_id: Optional[Union[str, int]]
) -> JsonRpcResponse:
    """Create successful JSON-RPC response."""
    return JsonRpcResponse(jsonrpc="2.0", result=result, id=request_id)


def create_error_response(
    error_code: JsonRpcError,
    message: str,
    data: Any = None,
    request_id: Optional[Union[str, int]] = None,
) -> JsonRpcErrorResponse:
    """Create JSON-RPC error response."""
    return JsonRpcErrorResponse.create(error_code, message, data, request_id)
