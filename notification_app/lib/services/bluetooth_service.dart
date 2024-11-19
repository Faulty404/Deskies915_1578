import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';
import 'dart:typed_data';
import 'package:logger/logger.dart';

class BluetoothService {
  final Logger _logger = Logger();

  BluetoothDevice? connectedDevice;
  BluetoothConnection? connection;

  // Get a list of paired devices
  Future<List<BluetoothDevice>> getPairedDevices() async {
    try {
      return await FlutterBluetoothSerial.instance.getBondedDevices();
    } catch (e) {
      _logger.e('Error getting paired devices', e);
      return [];
    }
  }

  // Connect to a specific Bluetooth device
  Future<void> connectToDevice(BluetoothDevice device) async {
    try {
      connection = await BluetoothConnection.toAddress(device.address);
      connectedDevice = device;
      _logger.i('Connected to ${device.name}');
      
      connection?.input?.listen((data) {
        _logger.d('Received: ${String.fromCharCodes(data)}');
      }).onDone(() {
        _logger.w('Disconnected from ${device.name}');
        connectedDevice = null;
      });
    } catch (e) {
      _logger.e('Error connecting to device', e);
    }
  }

  // Send data to the connected Bluetooth device
  Future<void> sendData(String data) async {
    if (connection != null && connection!.isConnected) {
      try {
        Uint8List uint8Data = Uint8List.fromList(data.codeUnits);
        connection!.output.add(uint8Data);
        await connection!.output.allSent;
        _logger.i("Data sent: $data");
      } catch (e) {
        _logger.e("Error sending data", e);
      }
    } else {
      _logger.w("No device connected!");
    }
  }

  // Disconnect from the currently connected device
  void disconnect() {
    try {
      connection?.finish(); // Gracefully close the connection
      _logger.i('Disconnected from ${connectedDevice?.name}');
    } catch (e) {
      _logger.e('Error during disconnection', e);
    } finally {
      connectedDevice = null;
    }
  }

  // Check if a device is currently connected
  bool isConnected() {
    return connection != null && connection!.isConnected;
  }
}
