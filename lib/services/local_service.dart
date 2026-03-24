import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/transaction_model.dart';

class LocalService {
  static const key = "transactions";

  static Future<List<TransactionModel>> getAll() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(key);

    if (data == null) return [];

    final List decoded = jsonDecode(data);
    return decoded.map((e) => TransactionModel.fromMap(e)).toList();
  }

  static Future<void> saveAll(List<TransactionModel> list) async {
    final prefs = await SharedPreferences.getInstance();
    final data = jsonEncode(list.map((e) => e.toMap()).toList());
    await prefs.setString(key, data);
  }
}