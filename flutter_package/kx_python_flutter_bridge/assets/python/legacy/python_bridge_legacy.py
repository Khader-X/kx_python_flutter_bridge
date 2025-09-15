import json
import time
import os
from pathlib import Path


def add_numbers(a: int | float, b: int | float) -> float:
    """Simple Python function that adds two numbers"""
    a = float(a)
    b = float(b)
    return a + b


def watch_for_requests():
    """Watch for requests from Flutter and respond"""
    # Get bridge directory - ensure we're using the correct working directory
    # First, get the script's directory and go up to project root
    script_dir = Path(__file__).parent.parent.parent.parent  # Go up to project root
    bridge_dir = script_dir / "py_dart_bridging"

    # Ensure directory exists
    bridge_dir.mkdir(exist_ok=True)

    request_file = bridge_dir / "flutter_request.json"
    response_file = bridge_dir / "python_response.json"

    print(f"Python bridge is running and watching for requests...")
    print(f"Script directory: {Path(__file__).parent}")
    print(f"Project root: {script_dir}")
    print(f"Bridge directory: {bridge_dir.absolute()}")
    print(f"Request file: {request_file.absolute()}")
    print(f"Response file: {response_file.absolute()}")
    print(f"Current working directory: {Path.cwd()}")
    print("=" * 50)

    while True:
        try:
            # Check if request file exists and is not empty
            if request_file.exists() and request_file.stat().st_size > 0:
                print("Request detected, processing...")

                # Wait a bit to ensure file write is complete
                time.sleep(0.05)

                # Read and parse the request
                try:
                    with open(request_file, "r") as f:
                        content = f.read().strip()
                        if not content:  # Skip empty files
                            continue
                        request = json.loads(content)
                except (json.JSONDecodeError, FileNotFoundError):
                    print("Skipping invalid or incomplete file")
                    # Clean up potentially corrupted file
                    if request_file.exists():
                        request_file.unlink()
                    continue

                # Process the request
                function_name = request.get("function")
                args = request.get("args", [])
                request_id = request.get("request_id")

                # Call the appropriate function
                if function_name == "add_numbers":
                    result = add_numbers(*args)
                else:
                    result = f"Unknown function: {function_name}"

                # Prepare response
                response = {"result": result, "request_id": request_id, "success": True}

                # Write response
                with open(response_file, "w") as f:
                    json.dump(response, f)

                print(f"Request processed, result: {result}")

                # Clean up request file
                request_file.unlink()

        except Exception as e:
            print(f"Error processing request: {e}")

            # Write error response
            if "request_id" in locals():
                error_response = {
                    "result": str(e),
                    "request_id": request_id,
                    "success": False,
                }
                with open(response_file, "w") as f:
                    json.dump(error_response, f)

        # Wait before checking again
        time.sleep(0.1)


if __name__ == "__main__":
    watch_for_requests()
