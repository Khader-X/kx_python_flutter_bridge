import 'package:flutter/material.dart';
import 'screens/jsonrpc_bridge_demo.dart';

/// Entry point of the Flutter desktop app.
void main() {
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
      home: const JsonRpcBridgeDemo(),
    );
  }
}
