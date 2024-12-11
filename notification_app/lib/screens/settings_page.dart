import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key, required Function(bool p1) onToggleTheme});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  bool _isDarkMode = false; // Track current theme mode

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          ListTile(
            leading: Icon(_isDarkMode ? Icons.dark_mode : Icons.light_mode),
            title: const Text('Appearance'),
            subtitle: Text(_isDarkMode ? 'Dark Mode' : 'Light Mode'),
            trailing: Switch(
              value: _isDarkMode,
              onChanged: (value) {
                setState(() {
                  _isDarkMode = value;
                });
                // Notify the app of the theme change
                final brightness = value ? Brightness.dark : Brightness.light;
                final themeData = ThemeData(brightness: brightness);
                // Use MaterialApp or similar to update the theme dynamically
                (context as Element).markNeedsBuild();
              },
            ),
          ),
        ],
      ),
    );
  }
}
