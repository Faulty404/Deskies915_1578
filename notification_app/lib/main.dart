import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class NotificationItem {
  final String message;
  final IconData icon;
  final String type;
  bool isExpanded; // To handle expanded/collapsed state

  NotificationItem(this.message, this.icon, this.type,
      {this.isExpanded = false});
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _selectedIndex = 0;

  // List of notifications
  List<NotificationItem> notifications = [
    NotificationItem(
        "Health update from Hospital", Icons.medical_services, "hospital",
        isExpanded: false),
    NotificationItem("Alarm for Meeting", Icons.access_time, "meeting",
        isExpanded: false),
    NotificationItem("You have a new message.", Icons.email, "message",
        isExpanded: false),
    NotificationItem("Check your app settings.", Icons.settings, "settings",
        isExpanded: false),
  ];

  void _onBottomNavItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  void _deleteNotification(int index) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text("Confirm Delete"),
        content:
            const Text("Are you sure you want to delete this notification?"),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Close the dialog without deleting
            },
            child: const Text("Cancel"),
          ),
          TextButton(
            onPressed: () {
              setState(() {
                notifications.removeAt(index); // Delete the notification
              });
              Navigator.pop(context); // Close the dialog after deleting
            },
            child: const Text("Delete", style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            GestureDetector(
              onTap: _showProfileDialog,
              child: CircleAvatar(
                backgroundImage:
                    NetworkImage('https://via.placeholder.com/150'),
                radius: 16,
              ),
            ),
            Text(_getPageTitle(_selectedIndex)),
            PopupMenuButton<String>(
              onSelected: (value) {
                if (value == 'Settings') {
                  // Navigate to Settings page
                } else if (value == 'Logout') {
                  _logout();
                }
              },
              itemBuilder: (context) => [
                const PopupMenuItem(value: 'Settings', child: Text('Settings')),
                const PopupMenuItem(value: 'Logout', child: Text('Logout')),
              ],
              icon: const Icon(Icons.menu),
            ),
          ],
        ),
      ),
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          _notificationsTab(),
          _watchTab(),
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
        ],
        selectedItemColor: Colors.deepPurple,
        unselectedItemColor: Colors.grey,
      ),
    );
  }

  // Helper method to get the title based on the selected index
  String _getPageTitle(int index) {
    switch (index) {
      case 1:
        return "Watch";
      default:
        return "Notifications";
    }
  }

  // Notifications tab widget
  Widget _notificationsTab() {
    return ListView.builder(
      padding: const EdgeInsets.all(16.0),
      itemCount: notifications.length,
      itemBuilder: (context, index) {
        final notification = notifications[notifications.length - 1 - index];
        return GestureDetector(
          onTap: () {
            setState(() {
              notification.isExpanded = !notification.isExpanded;
            });
          },
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
                    Icon(notification.icon,
                        size: 32.0, color: Colors.deepPurple),
                    const SizedBox(width: 12.0),
                    Expanded(
                      child: Text(
                        notification.message,
                        style: const TextStyle(fontSize: 16.0),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.delete, color: Colors.deepPurple),
                      onPressed: () {
                        _deleteNotification(notifications.length - 1 - index);
                      },
                    ),
                  ],
                ),
                if (notification.isExpanded)
                  Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: Text(
                      _getFullNotificationInfo(notification),
                      style:
                          const TextStyle(fontSize: 14.0, color: Colors.black),
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  String _getFullNotificationInfo(NotificationItem notification) {
    switch (notification.type) {
      case 'hospital':
        return 'Health update from Hospital. Please check your appointment status and follow up.';
      case 'meeting':
        return 'Alarm for Meeting. The meeting is scheduled at 3:00 p.m.';
      case 'message':
        return notification.message; // Display the whole message
      case 'settings':
        return 'Check your app settings to update preferences and notifications.';
      default:
        return 'No additional information available.';
    }
  }

  // Watch Tab Widget
  Widget _watchTab() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          GestureDetector(
            onTap: () {
              // Add functionality for Watch Settings here
            },
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 10),
              padding: const EdgeInsets.all(16),
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
                  Icon(Icons.watch, size: 48.0, color: Colors.deepPurple),
                  const SizedBox(height: 8.0),
                  Text(
                    'Watch Settings',
                    style: TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.bold,
                      color: Colors.deepPurple,
                    ),
                  ),
                ],
              ),
            ),
          ),
          GestureDetector(
            onTap: () {
              // Add functionality for BuzzFit Settings here
            },
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 10),
              padding: const EdgeInsets.all(16),
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
                  Icon(Icons.memory, size: 48.0, color: Colors.deepPurple),
                  const SizedBox(height: 8.0),
                  Text(
                    'BuzzFit Settings',
                    style: TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.bold,
                      color: Colors.deepPurple,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Profile Dialog
  Future<void> _showProfileDialog() async {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('User Profile'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const CircleAvatar(
                radius: 40,
                backgroundImage:
                    NetworkImage('https://via.placeholder.com/150'),
              ),
              const SizedBox(height: 16),
              const Text('John Doe', style: TextStyle(fontSize: 18)),
              const Text('john.doe@example.com'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  // Logout
  void _logout() {
    // Add logout functionality here
  }
}
