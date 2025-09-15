import 'package:flutter/material.dart';
import 'package:kx_python_flutter_bridge/kx_python_flutter_bridge.dart';

/// Very simple bridge demo
class KXBridgeDemo extends StatefulWidget {
  const KXBridgeDemo({super.key});

  @override
  State<KXBridgeDemo> createState() => _KXBridgeDemoState();
}

class _KXBridgeDemoState extends State<KXBridgeDemo> {
  String _result = 'Press button to test bridge';
  bool _isLoading = false;

  Future<void> _testBridge() async {
    setState(() {
      _isLoading = true;
      _result = 'Testing...';
    });

    try {
      final result = await kxBridge.callFunction('power_calculation', {
        'base': 5.0,
        'exponent': 2.0,
      });
      setState(() {
        _result = 'Result: $result';
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
      appBar: AppBar(title: const Text('Bridge Test')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: _isLoading ? null : _testBridge,
              child: _isLoading
                  ? const CircularProgressIndicator()
                  : const Text('Test Bridge'),
            ),
            const SizedBox(height: 20),
            Text(
              _result,
              style: const TextStyle(fontSize: 16),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
