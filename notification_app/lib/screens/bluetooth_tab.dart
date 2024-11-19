import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import '../services/bluetooth_service.dart';

class BluetoothTab extends StatefulWidget {
  const BluetoothTab({super.key});

  @override
  State<BluetoothTab> createState() => _BluetoothTabState();
}

class _BluetoothTabState extends State<BluetoothTab> {
  final BluetoothService _bluetoothService = BluetoothService();
  List<BluetoothDevice> _devices = [];
  BluetoothDevice? _selectedDevice;
  bool _isConnecting = false;
  bool _isConnected = false;

  @override
  void initState() {
    super.initState();
    _getPairedDevices();
  }

  Future<void> _getPairedDevices() async {
    try {
      List<BluetoothDevice> devices = await _bluetoothService.getPairedDevices();
      setState(() {
        _devices = devices;
      });
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error fetching paired devices: $e")),
      );
    }
  }

  Future<void> _connectToDevice() async {
    if (_selectedDevice != null) {
      setState(() {
        _isConnecting = true;
      });
      try {
        await _bluetoothService.connectToDevice(_selectedDevice!);
        setState(() {
          _isConnected = true;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Connected to ${_selectedDevice!.name}")),
        );
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed to connect: $e")),
        );
      } finally {
        setState(() {
          _isConnecting = false;
        });
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select a device to connect.")),
      );
    }
  }

  Future<void> _sendData(String data) async {
    try {
      await _bluetoothService.sendData(data);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Data sent: $data")),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to send data: $e")),
      );
    }
  }

  void _disconnect() {
    _bluetoothService.disconnect();
    setState(() {
      _isConnected = false;
      _selectedDevice = null;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Disconnected")),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          DropdownButton<BluetoothDevice>(
            value: _selectedDevice,
            hint: const Text("Select a device"),
            items: _devices.map((device) {
              return DropdownMenuItem(
                value: device,
                child: Text(device.name ?? "Unknown"),
              );
            }).toList(),
            onChanged: (device) {
              setState(() {
                _selectedDevice = device;
              });
            },
          ),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: _isConnecting
                ? null
                : (_isConnected ? _disconnect : _connectToDevice),
            child: Text(
              _isConnecting
                  ? "Connecting..."
                  : (_isConnected ? "Disconnect" : "Connect"),
            ),
          ),
          if (_isConnected) ...[
            const SizedBox(height: 16),
            Text(
              "Connected to: ${_bluetoothService.connectedDevice?.name}",
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            TextField(
              decoration: const InputDecoration(
                labelText: "Send Data",
                border: OutlineInputBorder(),
              ),
              onSubmitted: (value) {
                if (value.isNotEmpty) {
                  _sendData(value);
                }
              },
            ),
          ],
        ],
      ),
    );
  }
}
