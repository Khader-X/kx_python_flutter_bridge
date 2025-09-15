"""
Example: Using KX Bridge with the installable package

This example shows how to use the kx_python_flutter_bridge package
after it's been installed with pip install.
"""

# Simple import from the installed package
from kx_python_flutter_bridge import KX_Bridge, registry


# Define some example functions
@KX_Bridge(category="example")
def greet_user(name: str, title: str = "User") -> str:
    """Greet a user with optional title."""
    return f"Hello, {title} {name}! Welcome to KX Bridge!"


@KX_Bridge(category="example")
def calculate_bmi(weight: float, height: float) -> dict:
    """Calculate BMI and return with category."""
    bmi = weight / (height**2)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    return {
        "bmi": round(bmi, 2),
        "category": category,
        "weight": weight,
        "height": height,
    }


@KX_Bridge(category="example")
def process_shopping_list(items: list, budget: float = 100.0) -> dict:
    """Process a shopping list with budget analysis."""
    total_items = len(items)
    estimated_cost = total_items * 5.0  # $5 per item estimate

    return {
        "total_items": total_items,
        "items": items,
        "estimated_cost": estimated_cost,
        "budget": budget,
        "within_budget": estimated_cost <= budget,
        "remaining_budget": max(0, budget - estimated_cost),
    }


def main():
    """Test the example functions."""
    print("🚀 KX Bridge Package Example")
    print("=" * 40)

    # List all registered functions
    functions = registry.list_functions()
    print(f"📋 Registered functions: {len(functions)}")
    for name, info in functions.items():
        print(f"  • {name} ({info['category']}): {info['description']}")

    print("\n🧪 Testing functions:")
    print("-" * 20)

    # Test greet_user
    result1 = registry.call_function("greet_user", {"name": "Alice", "title": "Dr."})
    print(f"Greeting: {result1}")

    # Test calculate_bmi
    result2 = registry.call_function("calculate_bmi", {"weight": 70, "height": 1.75})
    print(f"BMI: {result2}")

    # Test shopping list
    result3 = registry.call_function(
        "process_shopping_list",
        {"items": ["apples", "bread", "milk", "eggs"], "budget": 25.0},
    )
    print(f"Shopping: {result3}")

    print("\n✅ All tests completed successfully!")


if __name__ == "__main__":
    main()
