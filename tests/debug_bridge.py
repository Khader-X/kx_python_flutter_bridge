"""
Debug test for JSON-RPC bridge - manual interaction
"""

import sys
import os
import json
from pathlib import Path

# Add the current directory to Python path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src" / "kx_python_flutter_bridge"
sys.path.insert(0, str(src_dir))


def test_direct_communication():
    """Test direct communication with the JSON-RPC server"""
    try:
        print("🚀 Testing JSON-RPC Bridge Direct Communication", file=sys.stderr)

        from jsonrpc.server import JsonRpcServer
        from jsonrpc.function_registry import registry

        # Test creating request
        test_request = {
            "jsonrpc": "2.0",
            "method": "list_functions",
            "params": {},
            "id": "test_123",
        }

        print(f"📤 Test request: {json.dumps(test_request)}", file=sys.stderr)

        # Create server instance
        server = JsonRpcServer()

        # Process the request manually
        response = server._process_request(json.dumps(test_request))
        print(f"📥 Response: {response}", file=sys.stderr)

        # Parse and show the response
        response_data = json.loads(response)
        if "result" in response_data:
            functions = response_data["result"]["functions"]
            print(f"✅ Successfully got {len(functions)} functions:", file=sys.stderr)
            for name in functions:
                print(f"  🔧 {name}", file=sys.stderr)

        return True

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)
        return False


if __name__ == "__main__":
    success = test_direct_communication()
    if success:
        print("✅ Direct communication test passed!", file=sys.stderr)
    else:
        print("❌ Direct communication test failed!", file=sys.stderr)
        sys.exit(1)
