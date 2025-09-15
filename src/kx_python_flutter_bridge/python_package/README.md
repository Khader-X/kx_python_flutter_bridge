# KX Python Flutter Bridge

A powerful and easy-to-use bridge between Python and Flutter applications using JSON-RPC communication.

## Features

- 🚀 Simple decorator-based function registration
- 🔄 Bidirectional communication between Python and Flutter
- 📝 Automatic type inference and documentation
- 🎯 Category-based function organization
- 🛡️ Type-safe JSON-RPC communication
- 📦 Easy installation via pip

## Installation

```bash
pip install kx-python-flutter-bridge
```

## Quick Start

### 1. Create Python Functions

```python
from kx_python_flutter_bridge import KX_Bridge

@KX_Bridge(category="math")
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@KX_Bridge(category="text")
def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]

@KX_Bridge(category="data")
def calculate_average(numbers: list[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)
```

### 2. Start the Bridge Server

```bash
# Command line
kx-bridge-server

# Or in Python
from kx_python_flutter_bridge import JsonRpcServer

server = JsonRpcServer()
server.start()
```

### 3. Use in Flutter

```dart
import 'package:kx_python_flutter_bridge/kx_python_flutter_bridge.dart';

// Initialize the bridge
await kxBridge.start();

// Call Python functions
final result = await kxBridge.callFunction('add_numbers', {
  'a': 5.0,
  'b': 3.0,
});

print('Result: $result'); // Result: 8.0
```

## Categories

Functions can be organized into categories for better management:

- **math**: Mathematical operations
- **text**: String manipulation
- **data**: Data processing and analysis
- **utility**: General utility functions
- **datetime**: Date and time operations

## Advanced Usage

### Custom Categories

```python
@KX_Bridge(category="custom")
def my_custom_function(param: str) -> dict:
    """Custom function with complex return type."""
    return {
        "processed": param.upper(),
        "length": len(param),
        "timestamp": datetime.now().isoformat()
    }
```

### Function Discovery

```python
from kx_python_flutter_bridge import registry

# List all registered functions
functions = registry.list_functions()
print(f"Available functions: {list(functions.keys())}")

# Get function information
info = registry.get_function_info("add_numbers")
print(f"Function info: {info}")
```

## Examples

See the `examples/` directory for complete example applications showing:

- Basic math operations
- Text processing
- Data analysis
- File operations
- Real-time communication

## Requirements

- Python 3.8+
- No external dependencies for core functionality

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## Support

- 📖 [Documentation](https://github.com/Khader-X/kx_python_flutter_bridge)
- 🐛 [Bug Reports](https://github.com/Khader-X/kx_python_flutter_bridge/issues)
- 💬 [Discussions](https://github.com/Khader-X/kx_python_flutter_bridge/discussions)