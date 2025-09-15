"""
JSON-RPC Server for Python-Flutter Bridge

This server handles JSON-RPC 2.0 communication via stdin/stdout,
providing a professional interface for function calls between
Flutter and Python without requiring HTTP servers or external APIs.
"""

import sys
import json
import traceback
from typing import Any, Dict
from .protocol import (
    JsonRpcRequest,
    JsonRpcResponse,
    JsonRpcErrorResponse,
    JsonRpcError,
    create_success_response,
    create_error_response,
)
from .function_registry import registry


class JsonRpcServer:
    """JSON-RPC 2.0 server using stdin/stdout communication."""

    def __init__(self):
        self.running = True

    def start(self) -> None:
        """Start the JSON-RPC server."""
        try:
            # Send startup message
            self._log("JSON-RPC Bridge Server started - ready for requests")

            # Main server loop
            while self.running:
                try:
                    # Read request from stdin
                    line = sys.stdin.readline().strip()
                    if not line:
                        continue

                    # Process request and send response
                    response = self._process_request(line)
                    if response:
                        print(response, flush=True)

                except EOFError:
                    # Client closed connection
                    self._log("Client disconnected")
                    break
                except KeyboardInterrupt:
                    # Graceful shutdown
                    self._log("Server shutting down")
                    break
                except Exception as e:
                    # Unexpected error
                    self._log(f"Unexpected error: {e}")
                    error_response = create_error_response(
                        JsonRpcError.INTERNAL_ERROR, "Internal server error", str(e)
                    )
                    print(error_response.to_json(), flush=True)

        except Exception as e:
            self._log(f"Server startup failed: {e}")
            sys.exit(1)

    def stop(self) -> None:
        """Stop the JSON-RPC server."""
        self.running = False

    def _process_request(self, request_line: str) -> str:
        """Process a JSON-RPC request and return response."""
        try:
            # Parse JSON-RPC request
            request = JsonRpcRequest.from_json(request_line)
            self._log(f"Processing request: {request.method}")

            # Handle different methods
            if request.method == "list_functions":
                result = self._handle_list_functions(request.params)
            elif request.method == "get_function_info":
                result = self._handle_get_function_info(request.params)
            else:
                result = self._handle_function_call(request.method, request.params)

            # Create success response
            response = create_success_response(result, request.id)
            return response.to_json()

        except ValueError as e:
            # JSON parsing or request format error
            self._log(f"Invalid request format: {e}")
            error_response = create_error_response(
                JsonRpcError.INVALID_REQUEST, "Invalid request format", str(e)
            )
            return error_response.to_json()

        except Exception as e:
            # General error
            self._log(f"Request processing error: {e}")
            request_id = None
            try:
                # Try to extract request ID for error response
                data = json.loads(request_line)
                request_id = data.get("id")
            except:
                pass

            error_response = create_error_response(
                JsonRpcError.INTERNAL_ERROR,
                "Request processing failed",
                str(e),
                request_id,
            )
            return error_response.to_json()

    def _handle_list_functions(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_functions request."""
        functions = registry.list_functions()
        return {"functions": functions, "count": len(functions)}

    def _handle_get_function_info(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_function_info request."""
        function_name = params.get("name")
        if not function_name:
            raise ValueError("Function name is required")

        info = registry.get_function_info(function_name)
        if not info:
            raise ValueError(f"Function '{function_name}' not found")

        return registry.list_functions()[function_name]

    def _handle_function_call(self, method_name: str, params: Dict[str, Any]) -> Any:
        """Handle function call request."""
        try:
            result = registry.call_function(method_name, params)
            return result
        except ValueError as e:
            # Function not found
            raise Exception(f"Method not found: {method_name}")
        except Exception as e:
            # Function execution error
            raise Exception(f"Function execution error: {str(e)}")

    def _log(self, message: str) -> None:
        """Log message to stderr (won't interfere with stdout communication)."""
        print(f"[JsonRpcServer] {message}", file=sys.stderr, flush=True)


def main():
    """Main entry point for the JSON-RPC server."""
    try:
        server = JsonRpcServer()
        server.start()
    except KeyboardInterrupt:
        print("[JsonRpcServer] Server stopped by user", file=sys.stderr)
    except Exception as e:
        print(f"[JsonRpcServer] Server error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()