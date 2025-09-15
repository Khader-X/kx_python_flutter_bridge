import 'package:flutter/material.dart';
import 'package:kx_python_flutter_bridge/kx_python_flutter_bridge.dart';

/// Enhanced JSON-RPC Bridge Demo Screen - comprehensive test suite
class KXBridgeDemo extends StatefulWidget {
  const KXBridgeDemo({super.key});

  @override
  State<KXBridgeDemo> createState() => _KXBridgeDemoState();
}

class _KXBridgeDemoState extends State<KXBridgeDemo> {
  String _result = 'Select a function to test Python bridge';
  bool _isLoading = false;
  String _selectedFunction = 'add_numbers';

  // Test functions with their parameters and descriptions
  final Map<String, Map<String, dynamic>> _testFunctions = {
    // Math functions
    'add_numbers': {
      'category': 'Math',
      'description': 'Add two numbers',
      'params': {'a': 5.0, 'b': 7.0},
      'display': '5 + 7',
    },
    'power_calculation': {
      'category': 'Math',
      'description': 'Calculate base^exponent',
      'params': {'base': 2.0, 'exponent': 8.0},
      'display': '2^8',
    },
    'factorial': {
      'category': 'Math',
      'description': 'Calculate factorial',
      'params': {'n': 6},
      'display': '6!',
    },
    'calculate_circle_area': {
      'category': 'Math',
      'description': 'Circle area & circumference',
      'params': {'radius': 5.0},
      'display': 'Circle r=5',
    },
    'fibonacci_sequence': {
      'category': 'Math',
      'description': 'Generate Fibonacci sequence',
      'params': {'count': 10},
      'display': 'Fib(10)',
    },

    // Text functions
    'word_analyzer': {
      'category': 'Text',
      'description': 'Analyze text properties',
      'params': {'text': 'Flutter Python Bridge Test'},
      'display': 'Analyze Text',
    },
    'text_transformer': {
      'category': 'Text',
      'description': 'Transform text case',
      'params': {'text': 'hello world', 'operation': 'title'},
      'display': 'Transform Text',
    },
    'palindrome_checker': {
      'category': 'Text',
      'description': 'Check if palindrome',
      'params': {'text': 'A man a plan a canal Panama'},
      'display': 'Check Palindrome',
    },

    // Data functions
    'list_statistics': {
      'category': 'Data',
      'description': 'Statistical analysis',
      'params': {
        'numbers': [1.0, 2.0, 3.0, 4.0, 5.0, 10.0, 15.0, 20.0],
      },
      'display': 'Stats Analysis',
    },
    'filter_and_sort': {
      'category': 'Data',
      'description': 'Filter and sort numbers',
      'params': {
        'numbers': [5.0, 15.0, 25.0, 2.0, 18.0, 30.0],
        'min_value': 10.0,
        'max_value': 25.0,
      },
      'display': 'Filter Numbers',
    },

    // Utility functions
    'get_system_info': {
      'category': 'Utility',
      'description': 'System information',
      'params': {},
      'display': 'System Info',
    },
    'validate_email': {
      'category': 'Utility',
      'description': 'Validate email format',
      'params': {'email': 'test@example.com'},
      'display': 'Validate Email',
    },
    'generate_password': {
      'category': 'Utility',
      'description': 'Generate random password',
      'params': {'length': 12, 'include_symbols': true},
      'display': 'Generate Password',
    },

    // DateTime functions
    'time_operations': {
      'category': 'DateTime',
      'description': 'Current time operations',
      'params': {'operation': 'now'},
      'display': 'Current Time',
    },
    'calculate_age': {
      'category': 'DateTime',
      'description': 'Calculate age',
      'params': {'birth_year': 1990, 'birth_month': 6, 'birth_day': 15},
      'display': 'Age Calculator',
    },
  };

  @override
  void initState() {
    super.initState();
    _checkBridgeStatus();
  }

  void _checkBridgeStatus() {
    if (kxBridge.status != BridgeStatus.connected) {
      setState(() {
        _result = 'Bridge not ready: ${kxBridge.lastError}';
      });
    } else {
      setState(() {
        _result = 'Bridge ready! Select a function to test';
      });
    }
  }

  Future<void> _callPythonFunction() async {
    final functionData = _testFunctions[_selectedFunction]!;

    setState(() {
      _isLoading = true;
      _result = 'Calling ${functionData['description']}...';
    });

    try {
      final result = await kxBridge.callFunction(
        _selectedFunction,
        functionData['params'],
      );

      setState(() {
        _result = _formatResult(_selectedFunction, result);
      });
    } catch (e) {
      setState(() {
        _result = 'Error calling $_selectedFunction: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  String _formatResult(String functionName, dynamic result) {
    if (result is Map) {
      return _formatMapResult(functionName, result);
    } else if (result is List) {
      return _formatListResult(functionName, result);
    } else {
      return 'Result: $result';
    }
  }

  String _formatMapResult(String functionName, Map result) {
    switch (functionName) {
      case 'calculate_circle_area':
        return 'Area: ${result['area']?.toStringAsFixed(2)}\nCircumference: ${result['circumference']?.toStringAsFixed(2)}';
      case 'word_analyzer':
        return 'Words: ${result['word_count']}\nChars: ${result['character_count']}\nUnique: ${result['unique_words']}';
      case 'list_statistics':
        return 'Mean: ${result['mean']?.toStringAsFixed(2)}\nMedian: ${result['median']}\nStd Dev: ${result['standard_deviation']?.toStringAsFixed(2)}';
      case 'validate_email':
        return 'Valid: ${result['is_valid']}\nDomain: ${result['domain_part']}';
      case 'generate_password':
        return 'Password: ${result['password']}\nStrength: ${result['strength']}';
      default:
        return result.toString();
    }
  }

  String _formatListResult(String functionName, List result) {
    switch (functionName) {
      case 'fibonacci_sequence':
        return 'Fibonacci: ${result.take(8).join(", ")}${result.length > 8 ? "..." : ""}';
      default:
        return result.toString();
    }
  }

  Future<void> _listAvailableFunctions() async {
    setState(() {
      _isLoading = true;
      _result = 'Getting available functions...';
    });

    try {
      final result = await kxBridge.callFunction('list_functions', {});
      final functions = result['functions'] as Map;

      setState(() {
        _result =
            'Available functions (${functions.length}):\n${functions.entries.take(10).map((e) => '• ${e.key} (${e.value['category']})').join('\n')}${functions.length > 10 ? '\n... and ${functions.length - 10} more' : ''}';
      });
    } catch (e) {
      setState(() {
        _result = 'Error listing functions: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final functionData = _testFunctions[_selectedFunction]!;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Python Bridge Test Suite'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            //////////////////////////
            // Function Selector
            //////////////////////////
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Select Test Function:',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    DropdownButtonFormField<String>(
                      initialValue: _selectedFunction,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        contentPadding: EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                      ),
                      items: _testFunctions.entries.map((entry) {
                        return DropdownMenuItem(
                          value: entry.key,
                          child: Text(
                            '${entry.value['display']} (${entry.value['category']})',
                            overflow: TextOverflow.ellipsis,
                          ),
                        );
                      }).toList(),
                      onChanged: _isLoading
                          ? null
                          : (value) {
                              if (value != null) {
                                setState(() {
                                  _selectedFunction = value;
                                  _result =
                                      'Selected: ${_testFunctions[value]!['description']}';
                                });
                              }
                            },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            //////////////////////////
            // Current Function Info
            //////////////////////////
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '${functionData['category']}: ${functionData['display']}',
                    style: const TextStyle(
                      fontSize: 18,
                      color: Colors.cyanAccent,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    functionData['description'],
                    style: const TextStyle(fontSize: 14, color: Colors.white70),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            //////////////////////////
            // Action Buttons
            //////////////////////////
            Row(
              children: [
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _callPythonFunction,
                    child: _isLoading
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('Test Function'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: _isLoading ? null : _listAvailableFunctions,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange,
                    ),
                    child: const Text('List All'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            //////////////////////////
            // Results Display
            //////////////////////////
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.black87,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.cyanAccent, width: 1),
                ),
                child: SingleChildScrollView(
                  child: SelectableText(
                    _result,
                    style: const TextStyle(
                      fontSize: 14,
                      color: Colors.cyanAccent,
                      fontFamily: 'Courier',
                    ),
                  ),
                ),
              ),
            ),

            //////////////////////////
            // Status Bar
            //////////////////////////
            Container(
              padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
              decoration: BoxDecoration(
                color: Colors.grey.shade800,
                borderRadius: BorderRadius.circular(4),
              ),
              child: Row(
                children: [
                  Icon(
                    kxBridge.status == BridgeStatus.connected
                        ? Icons.wifi
                        : Icons.wifi_off,
                    size: 16,
                    color: kxBridge.status == BridgeStatus.connected
                        ? Colors.green
                        : Colors.red,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Bridge: ${kxBridge.status.toString().split('.').last}',
                    style: const TextStyle(fontSize: 12, color: Colors.white70),
                  ),
                  const Spacer(),
                  Text(
                    '${_testFunctions.length} test functions available',
                    style: const TextStyle(fontSize: 12, color: Colors.white70),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
