import 'package:flutter/material.dart';
import 'package:kx_python_flutter_bridge/kx_python_flutter_bridge.dart';

/// Simple JSON-RPC Bridge Demo Screen - minimalistic version
class KXBridgeDemo extends StatefulWidget {
  const KXBridgeDemo({super.key});

  @override
  State<KXBridgeDemo> createState() => _KXBridgeDemoState();
}

class _KXBridgeDemoState extends State<KXBridgeDemo> {
  String _result = 'Click the button to call Python';
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    // Bridge is already initialized in main(), just check status
    _checkBridgeStatus();
  }

  void _checkBridgeStatus() {
    if (kxBridge.status != BridgeStatus.connected) {
      setState(() {
        _result = 'Bridge not ready: ${kxBridge.lastError}';
      });
    } else {
      setState(() {
        _result = 'Bridge ready! Click button to call Python';
      });
    }
  }

  Future<void> _callPythonFunction() async {
    setState(() {
      _isLoading = true;
      _result = 'Calling Python...';
    });

    try {
      // Call a simple function - add_numbers with hardcoded values
      final result = await kxBridge.callFunction('add_numbers', {
        'a': 5,
        'b': 7,
      });

      setState(() {
        _result = 'Python says: $result';
      });
    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Simple Python Bridge'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            //////////////////////////
            // What we are computing
            //////////////////////////
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(15),
              ),
              child: const Text(
                '5 + 7',
                style: TextStyle(fontSize: 24, color: Colors.cyanAccent),
              ),
            ),
            const SizedBox(height: 20),

            //////////////////////////
            // Button to call Python function
            //////////////////////////
            ElevatedButton(
              onPressed: _isLoading ? null : _callPythonFunction,
              child: const Text('Call Python Function'),
            ),
            const SizedBox(height: 20),

            //////////////////////////
            // Display result or loading indicator
            //////////////////////////
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(15),
                    margin: const EdgeInsets.symmetric(horizontal: 20),
                    decoration: BoxDecoration(
                      color: Colors.black87,
                      borderRadius: BorderRadius.circular(15),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Flexible(
                          child: Text(
                            _result,
                            style: const TextStyle(
                              fontSize: 18,
                              color: Colors.cyanAccent,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ),
                        if (_isLoading) const SizedBox(width: 20),
                        if (_isLoading)
                          const CircularProgressIndicator(
                            color: Colors.cyanAccent,
                          ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
