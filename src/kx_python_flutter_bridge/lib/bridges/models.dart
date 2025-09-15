import 'dart:convert';

/// JSON-RPC 2.0 Request Model
class JsonRpcRequest {
  final String jsonrpc;
  final String method;
  final Map<String, dynamic> params;
  final String id;

  JsonRpcRequest({
    this.jsonrpc = '2.0',
    required this.method,
    required this.params,
    required this.id,
  });

  Map<String, dynamic> toJson() {
    return {'jsonrpc': jsonrpc, 'method': method, 'params': params, 'id': id};
  }

  String toJsonString() {
    return jsonEncode(toJson());
  }
}

/// JSON-RPC 2.0 Response Model
class JsonRpcResponse {
  final String jsonrpc;
  final dynamic result;
  final String id;

  JsonRpcResponse({
    required this.jsonrpc,
    required this.result,
    required this.id,
  });

  factory JsonRpcResponse.fromJson(Map<String, dynamic> json) {
    return JsonRpcResponse(
      jsonrpc: json['jsonrpc'] ?? '2.0',
      result: json['result'],
      id: json['id'].toString(),
    );
  }

  factory JsonRpcResponse.fromJsonString(String jsonString) {
    final json = jsonDecode(jsonString) as Map<String, dynamic>;
    return JsonRpcResponse.fromJson(json);
  }
}

/// JSON-RPC 2.0 Error Response Model
class JsonRpcErrorResponse {
  final String jsonrpc;
  final JsonRpcError error;
  final String? id;

  JsonRpcErrorResponse({required this.jsonrpc, required this.error, this.id});

  factory JsonRpcErrorResponse.fromJson(Map<String, dynamic> json) {
    return JsonRpcErrorResponse(
      jsonrpc: json['jsonrpc'] ?? '2.0',
      error: JsonRpcError.fromJson(json['error']),
      id: json['id']?.toString(),
    );
  }

  factory JsonRpcErrorResponse.fromJsonString(String jsonString) {
    final json = jsonDecode(jsonString) as Map<String, dynamic>;
    return JsonRpcErrorResponse.fromJson(json);
  }
}

/// JSON-RPC 2.0 Error Model
class JsonRpcError {
  final int code;
  final String message;
  final dynamic data;

  JsonRpcError({required this.code, required this.message, this.data});

  factory JsonRpcError.fromJson(Map<String, dynamic> json) {
    return JsonRpcError(
      code: json['code'],
      message: json['message'],
      data: json['data'],
    );
  }

  @override
  String toString() {
    return 'JsonRpcError(code: $code, message: $message${data != null ? ', data: $data' : ''})';
  }
}

/// Function Parameter Model
class FunctionParameter {
  final String name;
  final String type;
  final bool required;
  final dynamic defaultValue;
  final String description;

  FunctionParameter({
    required this.name,
    required this.type,
    required this.required,
    this.defaultValue,
    this.description = '',
  });

  bool get hasDefault => !required;

  factory FunctionParameter.fromJson(Map<String, dynamic> json) {
    return FunctionParameter(
      name: json['name'],
      type: json['type'],
      required: json['required'] ?? true,
      defaultValue: json['default'],
      description: json['description'] ?? '',
    );
  }
}

/// Function Information Model
class FunctionInfo {
  final String name;
  final String description;
  final String category;
  final List<FunctionParameter> parameters;
  final String returnType;

  FunctionInfo({
    required this.name,
    required this.description,
    required this.category,
    required this.parameters,
    required this.returnType,
  });

  String get docstring => description;

  factory FunctionInfo.fromJson(String name, Map<String, dynamic> json) {
    final paramList = (json['parameters'] as List<dynamic>? ?? [])
        .map(
          (param) => FunctionParameter.fromJson(param as Map<String, dynamic>),
        )
        .toList();

    return FunctionInfo(
      name: name,
      description: json['description'] ?? '',
      category: json['category'] ?? 'general',
      parameters: paramList,
      returnType: json['return_type'] ?? 'any',
    );
  }
}

/// Available Functions Response Model
class FunctionListResponse {
  final Map<String, FunctionInfo> _functionsMap;
  final int count;

  FunctionListResponse({
    required Map<String, FunctionInfo> functions,
    required this.count,
  }) : _functionsMap = functions;

  List<FunctionInfo> get functions => _functionsMap.values.toList();
  Map<String, FunctionInfo> get functionsMap => _functionsMap;

  factory FunctionListResponse.fromJson(Map<String, dynamic> json) {
    final functionsJson = json['functions'] as Map<String, dynamic>? ?? {};
    final functions = <String, FunctionInfo>{};

    for (final entry in functionsJson.entries) {
      functions[entry.key] = FunctionInfo.fromJson(
        entry.key,
        entry.value as Map<String, dynamic>,
      );
    }

    return FunctionListResponse(
      functions: functions,
      count: json['count'] ?? functions.length,
    );
  }
}
