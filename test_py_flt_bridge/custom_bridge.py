"""
Custom JSON-RPC Bridge Entry Point with Test Functions

This script extends the main bridge with our custom test functions.
"""

import sys
import os
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
bridge_dir = (
    current_dir.parent.parent / "src" / "kx_python_flutter_bridge" / "assets" / "python"
)
my_codes_dir = current_dir / "my_py_codes"

sys.path.insert(0, str(bridge_dir))
sys.path.insert(0, str(current_dir))

try:
    # Import the bridge system
    from jsonrpc.server import JsonRpcServer
    from jsonrpc.function_registry import registry

    # Import our custom test functions (this will register them)
    try:
        import my_py_codes

        print("✅ Custom test functions loaded!", file=sys.stderr, flush=True)

        # List all registered functions
        functions = registry.list_functions()
        print(
            f"📋 Total registered functions: {len(functions)}",
            file=sys.stderr,
            flush=True,
        )
        for name, info in functions.items():
            print(
                f"  - {name} ({info['category']}): {info['description']}",
                file=sys.stderr,
                flush=True,
            )

    except ImportError as e:
        print(f"⚠️ Could not import custom functions: {e}", file=sys.stderr, flush=True)
        print("📋 Using default functions only", file=sys.stderr, flush=True)

    def main():
        """Main entry point for the extended JSON-RPC server"""
        try:
            # Create and start the server
            server = JsonRpcServer()
            print(
                "🚀 Extended JSON-RPC Bridge Server starting...",
                file=sys.stderr,
                flush=True,
            )

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
