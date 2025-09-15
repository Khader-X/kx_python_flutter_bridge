import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'models.dart';

/// Connection Status Enum
enum BridgeStatus { disconnected, connecting, connected, error }

/// KX Bridge Client for Python Communication
class KXBridge {
  Process? _process;
  BridgeStatus _status = BridgeStatus.disconnected;
  String _lastError = '';
  final List<String> _errorLines = [];

  final StreamController<BridgeStatus> _statusController =
      StreamController<BridgeStatus>.broadcast();
  final Map<String, Completer<dynamic>> _pendingRequests = {};
  final Random _random = Random();

  // Getters
  BridgeStatus get status => _status;
  String get lastError => _lastError;
  Stream<BridgeStatus> get statusStream => _statusController.stream;

  /// Initialize the KX Bridge - alias for start() method
  /// This method provides a more semantic name for initialization
  Future<bool> init() async {
    return await start();
  }

  /// Start the Python JSON-RPC bridge
  Future<bool> start() async {
    if (_status == BridgeStatus.connected) {
      return true;
    }

    try {
      _setStatus(BridgeStatus.connecting);
      debugPrint('🚀 Starting JSON-RPC Bridge...');

      // Get the paths to Python executable and script
      final pythonPath = _getPythonExecutablePath();
      final scriptPath = _getPythonScriptPath();
      debugPrint('🐍 Python executable: $pythonPath');
      debugPrint('📄 Script path: $scriptPath');

      // Start Python process
      _process = await Process.start(
        pythonPath,
        [scriptPath],
        runInShell: true,
        workingDirectory: _getProjectRoot(),
      );

      // Setup stdout listener
      _process!.stdout
          .transform(utf8.decoder)
          .transform(const LineSplitter())
          .listen(_handleResponse);

      // Setup stderr listener for debugging and error capture
      _errorLines.clear(); // Clear previous errors
      _process!.stderr
          .transform(utf8.decoder)
          .transform(const LineSplitter())
          .listen((line) {
            debugPrint('🐍 Python: $line');
            _errorLines.add(line);
          });

      // Monitor process exit
      _process!.exitCode.then((exitCode) {
        debugPrint('🔚 Python process exited with code: $exitCode');
        if (_status == BridgeStatus.connected ||
            _status == BridgeStatus.connecting) {
          String errorMsg =
              'Python process terminated unexpectedly (exit code: $exitCode)';
          if (_errorLines.isNotEmpty) {
            errorMsg += '\nErrors: ${_errorLines.join('; ')}';
          }
          _setStatus(BridgeStatus.error, errorMsg);
        }
      });

      // Wait longer for process to initialize
      await Future.delayed(const Duration(milliseconds: 1500));

      // Test connection with a special method that doesn't require connected status
      try {
        debugPrint('🧪 Testing connection...');
        await _testConnection();
        _setStatus(BridgeStatus.connected);
        debugPrint('✅ JSON-RPC Bridge connected successfully');
        return true;
      } catch (e) {
        String detailedError = 'Failed to establish communication: $e';
        if (_errorLines.isNotEmpty) {
          detailedError += '\nPython errors: ${_errorLines.join('; ')}';
        }
        _setStatus(BridgeStatus.error, detailedError);
        await stop();
        return false;
      }
    } catch (e) {
      String detailedError = 'Failed to start Python process: $e';
      if (_errorLines.isNotEmpty) {
        detailedError += '\nPython errors: ${_errorLines.join('; ')}';
      }
      _setStatus(BridgeStatus.error, detailedError);
      debugPrint('❌ Bridge startup failed: $e');
      return false;
    }
  }

  /// Test connection without requiring connected status
  Future<void> _testConnection() async {
    if (_process == null) {
      throw Exception('Python process is not running');
    }

    // Generate unique request ID
    final requestId = 'test_${DateTime.now().millisecondsSinceEpoch}';

    // Create JSON-RPC request
    final request = JsonRpcRequest(
      method: 'list_functions',
      params: {},
      id: requestId,
    );

    // Create completer for response
    final completer = Completer<dynamic>();
    _pendingRequests[requestId] = completer;

    try {
      // Send request
      final requestJson = request.toJsonString();
      debugPrint('📤 Connection test request: $requestJson');

      _process!.stdin.writeln(requestJson);
      await _process!.stdin.flush();

      // Wait for response with timeout
      final result = await completer.future.timeout(
        const Duration(seconds: 15),
        onTimeout: () {
          _pendingRequests.remove(requestId);
          throw TimeoutException(
            'Connection test timeout',
            const Duration(seconds: 15),
          );
        },
      );

      debugPrint('📥 Connection test response received: $result');
      return;
    } catch (e) {
      _pendingRequests.remove(requestId);
      rethrow;
    }
  }

  /// Stop the Python JSON-RPC bridge
  Future<void> stop() async {
    debugPrint('🛑 Stopping JSON-RPC Bridge...');

    // Cancel pending requests
    for (final completer in _pendingRequests.values) {
      if (!completer.isCompleted) {
        completer.completeError('Bridge disconnected');
      }
    }
    _pendingRequests.clear();

    // Kill Python process
    if (_process != null) {
      _process!.kill();
      _process = null;
    }

    _setStatus(BridgeStatus.disconnected);
    debugPrint('✅ Bridge stopped');
  }

  /// List available Python functions
  Future<FunctionListResponse> listFunctions() async {
    final response = await _sendRequest('list_functions', {});
    return FunctionListResponse.fromJson(response);
  }

  /// Get information about a specific function
  Future<FunctionInfo> getFunctionInfo(String functionName) async {
    final response = await _sendRequest('get_function_info', {
      'name': functionName,
    });
    return FunctionInfo.fromJson(functionName, response);
  }

  /// Call a Python function
  Future<dynamic> callFunction(
    String functionName,
    Map<String, dynamic> params,
  ) async {
    return await _sendRequest(functionName, params);
  }

  /// Send JSON-RPC request and wait for response
  Future<dynamic> _sendRequest(
    String method,
    Map<String, dynamic> params,
  ) async {
    if (_status != BridgeStatus.connected) {
      throw Exception('Bridge is not connected (status: $_status)');
    }

    if (_process == null) {
      throw Exception('Python process is not running');
    }

    // Generate unique request ID
    final requestId =
        'req_${DateTime.now().millisecondsSinceEpoch}_${_random.nextInt(1000)}';

    // Create JSON-RPC request
    final request = JsonRpcRequest(
      method: method,
      params: params,
      id: requestId,
    );

    // Create completer for response
    final completer = Completer<dynamic>();
    _pendingRequests[requestId] = completer;

    try {
      // Send request
      final requestJson = request.toJsonString();
      debugPrint('📤 Sending request: $method');
      debugPrint('📄 Request: $requestJson');

      _process!.stdin.writeln(requestJson);
      await _process!.stdin.flush();

      // Wait for response with timeout
      final result = await completer.future.timeout(
        const Duration(seconds: 10),
        onTimeout: () {
          _pendingRequests.remove(requestId);
          throw TimeoutException(
            'Request timeout for $method',
            const Duration(seconds: 10),
          );
        },
      );

      return result;
    } catch (e) {
      _pendingRequests.remove(requestId);
      rethrow;
    }
  }

  /// Handle response from Python process
  void _handleResponse(String line) {
    if (line.trim().isEmpty) return;

    try {
      debugPrint('📥 Received response: $line');
      final json = jsonDecode(line) as Map<String, dynamic>;

      // Check if it's an error response
      if (json.containsKey('error')) {
        final errorResponse = JsonRpcErrorResponse.fromJson(json);
        final requestId = errorResponse.id;

        if (requestId != null && _pendingRequests.containsKey(requestId)) {
          final completer = _pendingRequests.remove(requestId)!;
          if (!completer.isCompleted) {
            completer.completeError(errorResponse.error);
          }
        }
        return;
      }

      // Handle success response
      final response = JsonRpcResponse.fromJson(json);
      final requestId = response.id;

      if (_pendingRequests.containsKey(requestId)) {
        final completer = _pendingRequests.remove(requestId)!;
        if (!completer.isCompleted) {
          completer.complete(response.result);
        }
      }
    } catch (e) {
      debugPrint('❌ Failed to parse response: $e');
      debugPrint('📄 Raw response: $line');
    }
  }

  /// Set bridge status and notify listeners
  void _setStatus(BridgeStatus status, [String error = '']) {
    _status = status;
    _lastError = error;
    _statusController.add(status);
    debugPrint(
      '🔄 Status changed to: $status ${error.isNotEmpty ? '($error)' : ''}',
    );
  }

  /// Get path to Python JSON-RPC script
  String _getPythonScriptPath() {
    // Get the project root and construct path to Python script
    final projectRoot = _getProjectRoot();
    final scriptPath =
        '$projectRoot\\src\\kx_python_flutter_bridge\\jsonrpc_bridge.py';
    return scriptPath;
  }

  /// Get path to Python executable in virtual environment
  String _getPythonExecutablePath() {
    final projectRoot = _getProjectRoot();
    final pythonPath = '$projectRoot\\.venv\\Scripts\\python.exe';

    // Check if virtual environment Python exists
    if (File(pythonPath).existsSync()) {
      return pythonPath;
    }

    // Fallback to system Python
    debugPrint(
      '⚠️ Virtual environment Python not found at $pythonPath, falling back to system Python',
    );
    return 'python';
  }

  /// Get project root directory
  String _getProjectRoot() {
    final currentDir = Directory.current.path;

    // Navigate up from flutter_ui/test_py_flt_bridge to project root
    final projectRoot = '$currentDir\\..\\..';
    final resolvedRoot = Directory(projectRoot).resolveSymbolicLinksSync();

    debugPrint('📁 Project root: $resolvedRoot');
    return resolvedRoot;
  }

  /// Dispose resources
  void dispose() {
    stop();
    _statusController.close();
  }
}

/// Singleton instance
final kxBridge = KXBridge();
