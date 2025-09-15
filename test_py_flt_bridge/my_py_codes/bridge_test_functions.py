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
try:
    from kx_python_flutter_bridge import KX_Bridge
except ImportError:
    # Fallback for development - add the bridge module to Python path
    bridge_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "src",
        "kx_python_flutter_bridge",
        "python_package",
    )
    sys.path.insert(0, bridge_path)
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


@KX_Bridge(category="math")
def fibonacci_sequence(count: int) -> List[int]:
    """Generate Fibonacci sequence up to count numbers."""
    if count <= 0:
        return []
    elif count == 1:
        return [0]
    elif count == 2:
        return [0, 1]

    sequence = [0, 1]
    for i in range(2, count):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence


# ================================
# TEXT PROCESSING CATEGORY
# ================================


@KX_Bridge(category="text")
def word_analyzer(text: str) -> Dict[str, Any]:
    """Analyze text and return word count, character count, and other metrics."""
    words = text.split()
    unique_words = set(word.lower().strip('.,!?;:"()[]{}') for word in words)

    return {
        "text": text,
        "word_count": len(words),
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "")),
        "unique_words": len(unique_words),
        "average_word_length": (
            sum(len(word) for word in words) / len(words) if words else 0
        ),
        "longest_word": max(words, key=len) if words else "",
        "shortest_word": min(words, key=len) if words else "",
    }


@KX_Bridge(category="text")
def text_transformer(text: str, operation: str = "upper") -> str:
    """Transform text using various operations."""
    operations = {
        "upper": lambda t: t.upper(),
        "lower": lambda t: t.lower(),
        "title": lambda t: t.title(),
        "reverse": lambda t: t[::-1],
        "capitalize": lambda t: t.capitalize(),
        "snake_case": lambda t: t.lower().replace(" ", "_"),
        "camel_case": lambda t: "".join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(t.split())
        ),
    }

    if operation not in operations:
        available = ", ".join(operations.keys())
        raise ValueError(
            f"Operation '{operation}' not supported. Available: {available}"
        )

    return operations[operation](text)


@KX_Bridge(category="text")
def palindrome_checker(text: str) -> Dict[str, Any]:
    """Check if text is a palindrome and provide analysis."""
    # Clean text for palindrome check (remove spaces, punctuation, make lowercase)
    clean_text = "".join(char.lower() for char in text if char.isalnum())
    is_palindrome = clean_text == clean_text[::-1]

    return {
        "original_text": text,
        "clean_text": clean_text,
        "is_palindrome": is_palindrome,
        "length": len(clean_text),
        "reversed_text": text[::-1],
    }


# ================================
# DATA PROCESSING CATEGORY
# ================================


@KX_Bridge(category="data")
def list_statistics(numbers: List[float]) -> Dict[str, float]:
    """Calculate comprehensive statistics for a list of numbers."""
    if not numbers:
        return {"error": "Empty list provided"}

    sorted_numbers = sorted(numbers)
    n = len(numbers)
    mean = sum(numbers) / n
    median = (sorted_numbers[n // 2] + sorted_numbers[(n - 1) // 2]) / 2

    # Calculate variance and standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = variance**0.5

    return {
        "count": n,
        "sum": sum(numbers),
        "mean": mean,
        "median": median,
        "min": min(numbers),
        "max": max(numbers),
        "range": max(numbers) - min(numbers),
        "variance": variance,
        "standard_deviation": std_dev,
    }


@KX_Bridge(category="data")
def filter_and_sort(
    numbers: List[float],
    min_value: float = 0,
    max_value: float = 100,
    ascending: bool = True,
) -> Dict[str, Any]:
    """Filter numbers within range and sort them."""
    filtered = [n for n in numbers if min_value <= n <= max_value]
    sorted_filtered = sorted(filtered, reverse=not ascending)

    return {
        "original_count": len(numbers),
        "filtered_count": len(filtered),
        "excluded_count": len(numbers) - len(filtered),
        "filtered_numbers": sorted_filtered,
        "filter_range": {"min": min_value, "max": max_value},
        "sort_order": "ascending" if ascending else "descending",
    }


@KX_Bridge(category="data")
def group_by_range(
    numbers: List[float], range_size: float = 10
) -> Dict[str, List[float]]:
    """Group numbers into ranges."""
    if not numbers:
        return {}

    min_val = min(numbers)
    max_val = max(numbers)
    groups = {}

    for num in numbers:
        range_start = int(num / range_size) * range_size
        range_key = f"{range_start}-{range_start + range_size}"

        if range_key not in groups:
            groups[range_key] = []
        groups[range_key].append(num)

    return groups


# ================================
# UTILITY FUNCTIONS CATEGORY
# ================================


@KX_Bridge(category="utility")
def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    import platform
    import os

    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd(),
        "timestamp": datetime.datetime.now().isoformat(),
    }


@KX_Bridge(category="utility")
def format_json(data: str, indent: int = 2) -> str:
    """Format JSON string with proper indentation."""
    try:
        parsed = json.loads(data)
        return json.dumps(parsed, indent=indent, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"


@KX_Bridge(category="utility")
def generate_password(length: int = 12, include_symbols: bool = True) -> Dict[str, str]:
    """Generate a random password."""
    import random
    import string

    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = "".join(random.choice(chars) for _ in range(length))

    return {
        "password": password,
        "length": len(password),
        "includes_symbols": include_symbols,
        "strength": "strong" if length >= 12 else "medium" if length >= 8 else "weak",
    }


@KX_Bridge(category="utility")
def validate_email(email: str) -> Dict[str, Any]:
    """Validate email format and provide analysis."""
    import re

    # Simple email regex pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    is_valid = bool(re.match(pattern, email))

    parts = email.split("@") if "@" in email else [email]
    local_part = parts[0] if len(parts) > 0 else ""
    domain_part = parts[1] if len(parts) > 1 else ""

    return {
        "email": email,
        "is_valid": is_valid,
        "local_part": local_part,
        "domain_part": domain_part,
        "has_at_symbol": "@" in email,
        "has_dot_in_domain": "." in domain_part,
        "length": len(email),
    }


# ================================
# TIME AND DATE CATEGORY
# ================================


@KX_Bridge(category="datetime")
def time_operations(operation: str = "now") -> Dict[str, Any]:
    """Perform various time and date operations."""
    now = datetime.datetime.now()

    operations = {
        "now": lambda: now,
        "utc": lambda: datetime.datetime.utcnow(),
        "date_only": lambda: now.date(),
        "time_only": lambda: now.time(),
        "timestamp": lambda: now.timestamp(),
        "iso": lambda: now.isoformat(),
        "weekday": lambda: now.strftime("%A"),
        "month": lambda: now.strftime("%B"),
        "year": lambda: now.year,
    }

    if operation not in operations:
        available = ", ".join(operations.keys())
        return {
            "error": f"Operation '{operation}' not supported. Available: {available}"
        }

    result = operations[operation]()

    return {
        "operation": operation,
        "result": str(result),
        "timestamp": now.timestamp(),
        "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
    }


@KX_Bridge(category="datetime")
def calculate_age(
    birth_year: int, birth_month: int = 1, birth_day: int = 1
) -> Dict[str, Any]:
    """Calculate age from birth date."""
    try:
        birth_date = datetime.date(birth_year, birth_month, birth_day)
        today = datetime.date.today()

        age_years = today.year - birth_date.year
        if today.month < birth_date.month or (
            today.month == birth_date.month and today.day < birth_date.day
        ):
            age_years -= 1

        # Calculate next birthday
        next_birthday = datetime.date(today.year + 1, birth_month, birth_day)
        if datetime.date(today.year, birth_month, birth_day) >= today:
            next_birthday = datetime.date(today.year, birth_month, birth_day)

        days_to_birthday = (next_birthday - today).days

        return {
            "birth_date": birth_date.isoformat(),
            "current_date": today.isoformat(),
            "age_years": age_years,
            "days_to_birthday": days_to_birthday,
            "next_birthday": next_birthday.isoformat(),
        }
    except ValueError as e:
        return {"error": f"Invalid date: {str(e)}"}


if __name__ == "__main__":
    # Test functions locally
    print("Testing KX Bridge Functions...")

    # Test math functions
    print(f"Power calculation: {power_calculation(2, 3)}")
    print(f"Factorial: {factorial(5)}")
    print(f"Circle area: {calculate_circle_area(5)}")

    # Test text functions
    print(f"Word analyzer: {word_analyzer('Hello World Test')}")
    print(f"Text transformer: {text_transformer('hello world', 'title')}")

    # Test data functions
    print(f"List statistics: {list_statistics([1, 2, 3, 4, 5, 10, 20])}")

    # Test utility functions
    print(f"System info: {get_system_info()}")
    print(f"Email validation: {validate_email('test@example.com')}")

    print("All tests completed!")
