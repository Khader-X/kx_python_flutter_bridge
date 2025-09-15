"""
JSON-RPC Bridge Entry Point
Main executable for the Python JSON-RPC server that communicates with Flutter.
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from jsonrpc.server import JsonRpcServer
    from jsonrpc.function_registry import registry

    def main():
        """Main entry point for the JSON-RPC server"""
        try:
            # Create and start the server
            server = JsonRpcServer()
            print("🚀 JSON-RPC Bridge Server starting...", file=sys.stderr, flush=True)

            # Start the server (this will block until the process is terminated)
            server.start()

        except KeyboardInterrupt:
            print("🛑 Server stopped by user", file=sys.stderr, flush=True)
        except Exception as e:
            print(f"❌ Server error: {e}", file=sys.stderr, flush=True)
            sys.exit(1)

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}", file=sys.stderr, flush=True)
    print("Make sure all required modules are available", file=sys.stderr, flush=True)
    sys.exit(1)
