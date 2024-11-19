import 'package:flutter/material.dart';
import '../models/notification_item.dart';
import '../widgets/notification_card.dart';
import '../widgets/watch_tab_item.dart';
import '../utils/dialog_helpers.dart';
import './bluetooth_tab.dart'; // Import the BluetoothTab screen

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _selectedIndex = 0;

  List<NotificationItem> notifications = [
    NotificationItem("Health update from Hospital", Icons.medical_services, "hospital"),
    NotificationItem("Alarm for Meeting", Icons.access_time, "meeting"),
    NotificationItem("You have a new message.", Icons.email, "message"),
    NotificationItem("Check your app settings.", Icons.settings, "settings"),
  ];

  // Method to handle bottom navigation item taps
  void _onBottomNavItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  // Method to delete a notification
  void _deleteNotification(int index) {
  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: const Text('Delete Notification'),
      content: const Text('Are you sure you want to delete this notification?'),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context), // Dismiss dialog
          child: const Text('Cancel'),
        ),
        TextButton(
          onPressed: () {
            setState(() {
              notifications.removeAt(index);
            });
            Navigator.pop(context); // Dismiss dialog
          },
          child: const Text('Delete'),
        ),
      ],
    ),
  );
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_getPageTitle(_selectedIndex)),
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle),
            onPressed: () => showProfileDialog(context),
          ),
        ],
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          _notificationsTab(),
          _watchTab(),
          const BluetoothTab(), // Add the BluetoothTab screen here
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onBottomNavItemTapped,
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.notifications),
            label: 'Notifications',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.watch),
            label: 'Watch',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bluetooth),
            label: 'Bluetooth',
          ),
        ],
      ),
    );
  }

  // Helper method to get the title based on the selected index
  String _getPageTitle(int index) {
    switch (index) {
      case 1:
        return "Watch";
      case 2:
        return "Bluetooth";
      default:
        return "Notifications";
    }
  }

  // Notifications tab widget
  Widget _notificationsTab() {
    return ListView.builder(
      itemCount: notifications.length,
      itemBuilder: (context, index) {
        final notification = notifications[index];
        return NotificationCard(
          notification: notification,
          onTap: () {
            setState(() {
              notification.isExpanded = !notification.isExpanded;
            });
          },
          onDelete: () => _deleteNotification(index),
        );
      },
    );
  }

  // Watch tab widget
  Widget _watchTab() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          WatchTabItem(
            icon: Icons.watch,
            label: "Watch Settings",
            onTap: () {
              // Add functionality for Watch Settings here
            },
          ),
          WatchTabItem(
            icon: Icons.memory,
            label: "BuzzFit Settings",
            onTap: () {
              // Add functionality for BuzzFit Settings here
            },
          ),
        ],
      ),
    );
  }
}
