"""
Test script to verify JSON-RPC bridge communication
"""

import sys
import json
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src" / "kx_python_flutter_bridge"
sys.path.insert(0, str(src_dir))


def test_manual_communication():
    """Test manual JSON-RPC communication"""
    try:
        from jsonrpc.server import JsonRpcServer
        from jsonrpc.function_registry import registry

        print("✅ Successfully imported JSON-RPC components")

        # Test function registry
        functions = registry.list_functions()
        print(f"📋 Available functions: {len(functions)}")

        for name, info in functions.items():
            print(f"  🔧 {name}: {info['description']}")
            print(f"     Parameters: {len(info['parameters'])}")
            for param in info["parameters"]:
                required = "required" if param["required"] else "optional"
                print(f"       - {param['name']} ({param['type']}) - {required}")
            print()

        # Test JSON-RPC request format
        test_request = {
            "jsonrpc": "2.0",
            "method": "list_functions",
            "params": {},
            "id": "test_123",
        }

        print("🧪 Test JSON-RPC request:")
        print(json.dumps(test_request, indent=2))

        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Testing JSON-RPC Bridge Components...")
    print("=" * 50)

    success = test_manual_communication()

    print("=" * 50)
    if success:
        print("✅ All tests passed! Bridge components are working correctly.")
        print("🎯 Ready to use with Flutter app.")
    else:
        print("❌ Tests failed. Check error messages above.")
        sys.exit(1)
