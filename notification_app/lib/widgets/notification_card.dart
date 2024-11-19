import 'package:flutter/material.dart';
import '../models/notification_item.dart';

class NotificationCard extends StatelessWidget {
  final NotificationItem notification;
  final VoidCallback onDelete;
  final VoidCallback onTap;

  const NotificationCard({
    super.key,
    required this.notification,
    required this.onDelete,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 8.0),
        padding: const EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          color: Colors.deepPurple[100],
          borderRadius: BorderRadius.circular(8.0),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 2,
              blurRadius: 5,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Column(
          children: [
            Row(
              children: [
                Icon(notification.icon, size: 32.0, color: Colors.deepPurple),
                const SizedBox(width: 12.0),
                Expanded(
                  child: Text(notification.message,
                      style: const TextStyle(fontSize: 16.0)),
                ),
                IconButton(
                  icon: const Icon(Icons.delete, color: Colors.deepPurple),
                  onPressed: onDelete,
                ),
              ],
            ),
            if (notification.isExpanded)
              Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  notification.type,
                  style: const TextStyle(fontSize: 14.0, color: Colors.black),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
