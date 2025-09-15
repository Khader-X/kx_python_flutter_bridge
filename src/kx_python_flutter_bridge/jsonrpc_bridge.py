#!/usr/bin/env python3
"""
KX Python-Flutter Bridge - Auto-Discovery JSON-RPC Server

This is the main bridge server that automatically discovers all Python modules
with @KX_Bridge decorated functions and serves them via JSON-RPC.

Features:
- Automatic function discovery
- Built-in auto-restart capabilities
- Health monitoring
- Comprehensive error handling
- Zero-configuration setup

Usage:
This script is automatically launched by the Flutter KX Bridge when kxBridge.init() is called.
Users only need to create Python functions with @KX_Bridge decorators.
"""

import sys
import os
import json
import traceback
import time
import threading
import signal
import importlib
import importlib.util
import pkgutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import logging

# Setup logging to file (won't interfere with stdout communication)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("kx_bridge.log"),
        logging.StreamHandler(sys.stderr),  # Log to stderr, not stdout
    ],
)
logger = logging.getLogger(__name__)


class AutoRestartBridge:
    """Auto-discovery JSON-RPC Bridge with built-in restart capabilities"""

    def __init__(self):
        self.running = True
        self.restart_count = 0
        self.max_restarts = 10
        self.last_restart_time = 0
        self.restart_cooldown = 60  # seconds
        self.health_check_interval = 30  # seconds
        self.last_health_check = time.time()

        # Import bridge components
        self._setup_imports()

        # Discovered modules
        self.discovered_modules: Set[str] = set()

        # Auto-discovery
        self._discover_bridge_functions()

        # Setup signal handlers for graceful restart
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

        # Start health monitor
        self._start_health_monitor()

    def _setup_imports(self):
        """Setup imports for bridge components"""
        try:
            # Try to import from the package structure
            from kx_python_flutter_bridge.jsonrpc.server import JsonRpcServer
            from kx_python_flutter_bridge.jsonrpc.function_registry import registry
            from kx_python_flutter_bridge.jsonrpc.protocol import (
                JsonRpcRequest,
                JsonRpcResponse,
                JsonRpcErrorResponse,
                JsonRpcError,
                create_success_response,
                create_error_response,
            )

            self.JsonRpcServer = JsonRpcServer
            self.registry = registry
            self.JsonRpcRequest = JsonRpcRequest
            self.create_success_response = create_success_response
            self.create_error_response = create_error_response
            self.JsonRpcError = JsonRpcError

            logger.info("✅ Successfully imported bridge components")

        except ImportError as e:
            logger.error(f"❌ Failed to import bridge components: {e}")
            # Try alternative import paths
            self._try_alternative_imports()

    def _try_alternative_imports(self):
        """Try alternative import paths"""
        current_dir = Path(__file__).parent
        possible_paths = [
            current_dir.parent / "src" / "kx_python_flutter_bridge" / "python_package",
            current_dir / "src" / "kx_python_flutter_bridge" / "python_package",
            current_dir / "kx_python_flutter_bridge" / "python_package",
        ]

        for path in possible_paths:
            if path.exists():
                sys.path.insert(0, str(path))
                try:
                    from kx_python_flutter_bridge.jsonrpc.server import JsonRpcServer
                    from kx_python_flutter_bridge.jsonrpc.function_registry import (
                        registry,
                    )
                    from kx_python_flutter_bridge.jsonrpc.protocol import (
                        JsonRpcRequest,
                        create_success_response,
                        create_error_response,
                        JsonRpcError,
                    )

                    self.JsonRpcServer = JsonRpcServer
                    self.registry = registry
                    self.JsonRpcRequest = JsonRpcRequest
                    self.create_success_response = create_success_response
                    self.create_error_response = create_error_response
                    self.JsonRpcError = JsonRpcError

                    logger.info(
                        f"✅ Successfully imported bridge components from: {path}"
                    )
                    return
                except ImportError:
                    continue

        logger.error("❌ Could not find bridge components in any location")
        sys.exit(1)

    def _discover_bridge_functions(self):
        """Automatically discover Python modules with @KX_Bridge decorated functions"""
        logger.info("🔍 Discovering bridge functions...")

        # Get the current working directory (should be the Flutter project root)
        project_root = Path.cwd()

        # Common locations to search for Python modules
        search_paths = [
            project_root,
            project_root / "my_py_codes",
            project_root / "python_modules",
            project_root / "src",
            project_root / "lib" / "python",
            project_root / "scripts",
        ]

        discovered_count = 0

        for search_path in search_paths:
            if search_path.exists():
                discovered_count += self._scan_directory(search_path)

        # List all registered functions
        functions = self.registry.list_functions()
        logger.info(f"📋 Total discovered functions: {len(functions)}")
        for name, info in functions.items():
            logger.info(f"  - {name} ({info['category']}): {info['description']}")

        if len(functions) == 0:
            logger.warning(
                "⚠️ No bridge functions discovered! Make sure to use @KX_Bridge decorator."
            )

    def _scan_directory(self, directory: Path) -> int:
        """Scan directory for Python files with bridge functions"""
        discovered_count = 0

        try:
            # Add directory to Python path
            if str(directory) not in sys.path:
                sys.path.insert(0, str(directory))

            # Find all Python files
            for py_file in directory.rglob("*.py"):
                # Skip special files, Flutter files, and this bridge script
                if (
                    py_file.name.startswith("__")
                    or py_file.name == "jsonrpc_bridge.py"
                    or "flutter" in py_file.name.lower()
                    or "Flutter" in str(py_file)
                    or "ephemeral" in str(py_file)
                    or py_file.suffix != ".py"
                ):
                    continue

                try:
                    # Calculate module name
                    relative_path = py_file.relative_to(directory)
                    module_parts = list(relative_path.parts[:-1]) + [relative_path.stem]
                    module_name = ".".join(module_parts)

                    if module_name in self.discovered_modules:
                        continue  # Already discovered

                    # Import the module to trigger @KX_Bridge registration
                    logger.info(f"📦 Importing module: {module_name} from {py_file}")

                    spec = importlib.util.spec_from_file_location(module_name, py_file)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        self.discovered_modules.add(module_name)
                        discovered_count += 1

                except Exception as e:
                    logger.warning(f"⚠️ Could not import {py_file}: {e}")

        except Exception as e:
            logger.error(f"❌ Error scanning directory {directory}: {e}")

        return discovered_count

    def _start_health_monitor(self):
        """Start background health monitoring"""

        def health_monitor():
            while self.running:
                try:
                    current_time = time.time()

                    # Periodic health check
                    if (
                        current_time - self.last_health_check
                        > self.health_check_interval
                    ):
                        self.last_health_check = current_time
                        self._perform_health_check()

                    time.sleep(5)  # Check every 5 seconds

                except Exception as e:
                    logger.error(f"Health monitor error: {e}")
                    time.sleep(10)

        health_thread = threading.Thread(target=health_monitor, daemon=True)
        health_thread.start()
        logger.info("💓 Health monitor started")

    def _perform_health_check(self):
        """Perform health check"""
        try:
            # Check if we can list functions
            functions = self.registry.list_functions()
            logger.info(f"💓 Health check: {len(functions)} functions available")

            # Write status to file for external monitoring
            status = {
                "status": "healthy",
                "timestamp": time.time(),
                "uptime": (
                    time.time() - self.last_restart_time
                    if self.last_restart_time > 0
                    else 0
                ),
                "function_count": len(functions),
                "restart_count": self.restart_count,
            }

            with open("kx_bridge_status.json", "w") as f:
                json.dump(status, f, indent=2)

        except Exception as e:
            logger.error(f"Health check failed: {e}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def _should_restart(self) -> bool:
        """Check if server should restart"""
        current_time = time.time()

        # Check restart limits
        if self.restart_count >= self.max_restarts:
            logger.error(f"Maximum restarts ({self.max_restarts}) reached")
            return False

        # Check cooldown period
        if current_time - self.last_restart_time < self.restart_cooldown:
            logger.warning("Still in restart cooldown period")
            return False

        return True

    def start(self):
        """Start the auto-restart bridge server"""
        logger.info("🚀 Starting KX Auto-Restart Bridge Server...")

        while self.running:
            try:
                self.last_restart_time = time.time()

                # Create and start server
                server = self.JsonRpcServer()
                logger.info(f"✅ Bridge server started (restart #{self.restart_count})")

                # Start server (blocks until error or shutdown)
                server.start()

                # If we get here, server stopped normally
                if self.running:
                    logger.warning("Server stopped unexpectedly")
                    if self._should_restart():
                        self.restart_count += 1
                        logger.info(
                            f"🔄 Restarting server (attempt #{self.restart_count})..."
                        )
                        time.sleep(min(self.restart_count * 2, 30))  # Progressive delay
                        continue
                    else:
                        logger.error("❌ Cannot restart server")
                        break
                else:
                    logger.info("Server stopped gracefully")
                    break

            except KeyboardInterrupt:
                logger.info("🛑 Server stopped by user")
                self.running = False
                break

            except Exception as e:
                logger.error(f"❌ Server error: {e}")
                logger.error(traceback.format_exc())

                if self.running and self._should_restart():
                    self.restart_count += 1
                    logger.info(
                        f"🔄 Restarting due to error (attempt #{self.restart_count})..."
                    )
                    time.sleep(min(self.restart_count * 2, 30))  # Progressive delay
                    continue
                else:
                    logger.error("❌ Cannot restart server")
                    break

        logger.info("Bridge server shutdown complete")


def main():
    """Main entry point"""
    try:
        bridge = AutoRestartBridge()
        bridge.start()
    except Exception as e:
        logger.critical(f"💥 Critical error: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
