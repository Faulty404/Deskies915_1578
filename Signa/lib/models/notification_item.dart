import 'package:flutter/material.dart';

class NotificationItem {
  final String message;
  final IconData icon;
  final String type;
  bool isExpanded;

  NotificationItem(this.message, this.icon, this.type, {this.isExpanded = false});
}
