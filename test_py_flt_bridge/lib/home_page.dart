import 'package:flutter/material.dart';
import 'screens/jsonrpc_bridge_demo.dart';

/// Home page with a container showing "1+1" and a button below it.
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Flutter-Python Bridge')),
      body: Center(child: JsonRpcBridgeDemo()),
    );
  }
}
