"""
Function Registry System for Dynamic Function Discovery

This module provides automatic discovery of Python functions using introspection,
extracts their signatures, type hints, and documentation for dynamic UI generation.
"""

import inspect
from typing import Dict, Any, Callable, List, Optional, get_type_hints
from dataclasses import dataclass


@dataclass
class ParameterInfo:
    """Information about a function parameter."""

    name: str
    type_name: str
    default: Any
    required: bool
    description: str = ""


@dataclass
class FunctionInfo:
    """Information about a discoverable function."""

    name: str
    description: str
    parameters: List[ParameterInfo]
    return_type: str
    category: str = "general"


class FunctionRegistry:
    """Registry for discoverable Python functions."""

    def __init__(self):
        self._functions: Dict[str, Callable] = {}
        self._function_info: Dict[str, FunctionInfo] = {}

    def register(self, func: Callable, category: str = "general") -> None:
        """Register a function for discovery."""
        func_name = func.__name__
        self._functions[func_name] = func
        self._function_info[func_name] = self._analyze_function(func, category)

    def get_function(self, name: str) -> Optional[Callable]:
        """Get registered function by name."""
        return self._functions.get(name)

    def get_function_info(self, name: str) -> Optional[FunctionInfo]:
        """Get function information by name."""
        return self._function_info.get(name)

    def list_functions(self) -> Dict[str, Dict[str, Any]]:
        """List all registered functions with their information."""
        result = {}
        for name, info in self._function_info.items():
            result[name] = {
                "description": info.description,
                "category": info.category,
                "parameters": [
                    {
                        "name": param.name,
                        "type": param.type_name,
                        "required": param.required,
                        "default": (
                            param.default
                            if param.default != inspect.Parameter.empty
                            else None
                        ),
                        "description": param.description,
                    }
                    for param in info.parameters
                ],
                "return_type": info.return_type,
            }
        return result

    def call_function(self, name: str, params: Dict[str, Any]) -> Any:
        """Call registered function with parameters."""
        func = self.get_function(name)
        if not func:
            raise ValueError(f"Function '{name}' not found")

        try:
            # Convert params to positional/keyword arguments
            sig = inspect.signature(func)
            bound_args = sig.bind_partial(**params)
            bound_args.apply_defaults()

            return func(*bound_args.args, **bound_args.kwargs)
        except Exception as e:
            raise RuntimeError(f"Error calling function '{name}': {str(e)}")

    def _analyze_function(self, func: Callable, category: str) -> FunctionInfo:
        """Analyze function to extract metadata."""
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        # Extract description from docstring
        doc = inspect.getdoc(func) or f"Execute {func.__name__}"
        description = doc.split("\n")[0]  # First line of docstring

        # Extract parameters
        parameters = []
        for param_name, param in sig.parameters.items():
            param_type = type_hints.get(param_name, type(None))
            type_name = self._get_type_name(param_type)

            parameters.append(
                ParameterInfo(
                    name=param_name,
                    type_name=type_name,
                    default=param.default,
                    required=param.default == inspect.Parameter.empty,
                    description=f"Parameter {param_name}",
                )
            )

        # Extract return type
        return_type = type_hints.get("return", type(None))
        return_type_name = self._get_type_name(return_type)

        return FunctionInfo(
            name=func.__name__,
            description=description,
            parameters=parameters,
            return_type=return_type_name,
            category=category,
        )

    def _get_type_name(self, type_obj: Any) -> str:
        """Get string representation of type."""
        if type_obj == type(None):
            return "any"
        if hasattr(type_obj, "__name__"):
            return type_obj.__name__.lower()
        if hasattr(type_obj, "__origin__"):
            # Handle generic types like List[int], Dict[str, Any]
            return str(type_obj).replace("typing.", "").lower()
        return str(type_obj).lower()


# Global registry instance
registry = FunctionRegistry()


def discoverable(category: str = "general"):
    """Decorator to mark functions as discoverable."""

    def decorator(func: Callable) -> Callable:
        registry.register(func, category)
        return func

    return decorator


# Example functions for testing
@discoverable(category="math")
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@discoverable(category="math")
def multiply_numbers(a: float, b: float = 1.0) -> float:
    """Multiply two numbers together."""
    return a * b


@discoverable(category="text")
def reverse_string(text: str) -> str:
    """Reverse a string."""
    return text[::-1]


@discoverable(category="data")
def calculate_average(numbers: List[float]) -> float:
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


if __name__ == "__main__":
    # Test the registry
    print("Registered functions:")
    functions = registry.list_functions()
    for name, info in functions.items():
        print(f"  {name}: {info['description']}")
        for param in info["parameters"]:
            required = "required" if param["required"] else "optional"
            print(f"    - {param['name']} ({param['type']}, {required})")