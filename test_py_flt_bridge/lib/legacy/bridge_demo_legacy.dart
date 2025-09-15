import 'package:flutter/material.dart';
import 'dart:io';
import 'dart:convert';

class BridgeDemo extends StatefulWidget {
  const BridgeDemo({super.key});

  @override
  State<BridgeDemo> createState() => _BridgeDemoState();
}

class _BridgeDemoState extends State<BridgeDemo> {
  String result = 'Click the button to call Python';
  bool isLoading = false;

  Future<void> callPythonFunction() async {
    setState(() {
      isLoading = true;
      result = 'Calling Python...';
    });

    try {
      // Create a directory for communication `py_dart_bridging`
      // Use hardcoded absolute path to the correct project directory
      final bridgeDir = Directory(
        r"D:\KHADER\KhaderX\KX\kx_python_flutter_bridge\py_dart_bridging",
      );

      // Ensure the directory exists
      if (!await bridgeDir.exists()) {
        await bridgeDir.create(recursive: true);
      }

      final requestFile = File('${bridgeDir.path}/flutter_request.json');
      final responseFile = File('${bridgeDir.path}/python_response.json');

      debugPrint("************************");
      debugPrint('🔥Bridge Directory: ${bridgeDir.path}');
      debugPrint('🔥Request File: ${requestFile.path}');
      debugPrint('🔥Response File: ${responseFile.path}');
      debugPrint('🔥Current Directory: ${Directory.current.path}');
      debugPrint("************************");

      // Prepare the request
      final request = {
        'function': 'add_numbers',
        'args': [5, 7],
        'request_id': DateTime.now().millisecondsSinceEpoch.toString(),
      };

      // Write request to file
      await requestFile.writeAsString(jsonEncode(request));

      // Ensure file is fully written
      await Future.delayed(const Duration(milliseconds: 100));

      // Wait for Python to process and respond
      int attempts = 0;
      const maxAttempts = 50; // 5 seconds max wait

      while (attempts < maxAttempts) {
        await Future.delayed(const Duration(milliseconds: 100));
        attempts++;

        if (await responseFile.exists() &&
            (await responseFile.stat()).size > 0) {
          final responseContent = await responseFile.readAsString();
          final response = jsonDecode(responseContent);

          setState(() {
            result = 'Python says: ${response['result']}';
          });

          // Clean up response file (only if it still exists)
          try {
            if (await responseFile.exists()) {
              await responseFile.delete();
            }
          } catch (e) {
            // Ignore deletion errors - Python might have cleaned up already
            debugPrint('Response file cleanup: $e');
          }
          break;
        }
      }

      if (attempts >= maxAttempts) {
        setState(() {
          result = 'Timeout: No response from Python';
        });
      }

      // Clean up request file (only if it still exists)
      try {
        if (await requestFile.exists()) {
          await requestFile.delete();
        }
      } catch (e) {
        // Ignore deletion errors - Python might have cleaned up already
        debugPrint('Request file cleanup: $e');
      }
    } catch (e) {
      setState(() {
        result = 'Error: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
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
          onPressed: isLoading ? null : callPythonFunction,
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
            Container(
              padding: const EdgeInsets.all(15),
              decoration: BoxDecoration(
                color: Colors.black87,
                borderRadius: BorderRadius.circular(15),
              ),
              child: Row(
                children: [
                  Text(
                    result,
                    style: const TextStyle(
                      fontSize: 18,
                      color: Colors.cyanAccent,
                    ),
                  ),
                  if (isLoading) const SizedBox(width: 20),
                  if (isLoading)
                    CircularProgressIndicator(color: Colors.cyanAccent),
                ],
              ),
            ),
          ],
        ),
      ],
    );
  }
}
