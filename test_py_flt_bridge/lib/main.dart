import 'package:flutter/material.dart';
import 'package:kx_python_flutter_bridge/kx_python_flutter_bridge.dart';
import 'home_page.dart';

/// Entry point of the Flutter desktop app.
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize the Flutter-Python bridge here:
  debugPrint('🚀 Initializing KX Bridge...');
  final success = await kxBridge.init();
  if (success) {
    debugPrint('✅ KX Bridge initialized successfully!');
  } else {
    debugPrint('❌ KX Bridge initialization failed: ${kxBridge.lastError}');
  }

  runApp(const MyApp());
}

/// JSON-RPC Python Bridge App
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'JSON-RPC Python Bridge',
      debugShowCheckedModeBanner: false,
      debugShowMaterialGrid: false,
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      home: const HomePage(),
    );
  }
}
