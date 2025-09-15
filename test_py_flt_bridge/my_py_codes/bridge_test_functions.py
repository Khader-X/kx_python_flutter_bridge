"""
Bridge Test Functions - Comprehensive test suite for KX Bridge functionality

This module contains various test functions that demonstrate different capabilities
of the KX Bridge system including different parameter types, return types, and categories.
"""

import sys
import os
import json
import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

# Import from the installable package
from kx_python_flutter_bridge import KX_Bridge


# ================================
# MATH OPERATIONS CATEGORY
# ================================


@KX_Bridge(category="math")
def power_calculation(base: float, exponent: float = 2.0) -> float:
    """Calculate base raised to the power of exponent."""
    return base**exponent


@KX_Bridge(category="math")
def factorial(n: int) -> int:
    """Calculate factorial of a number."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


@KX_Bridge(category="math")
def calculate_circle_area(radius: float) -> Dict[str, float]:
    """Calculate circle area and circumference given radius."""
    import math

    area = math.pi * radius**2
    circumference = 2 * math.pi * radius
    return {"area": area, "circumference": circumference, "radius": radius}


if __name__ == "__main__":
    # Test functions locally
    print("Testing KX Bridge Functions...")

    # Test math functions
    print(f"Power calculation: {power_calculation(2, 3)}")
    print(f"Factorial: {factorial(5)}")
    print(f"Circle area: {calculate_circle_area(5)}")

    print("All tests completed!")
