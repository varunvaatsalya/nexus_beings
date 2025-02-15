import 'package:flutter/material.dart';
import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:shared_preferences/shared_preferences.dart';

class safehome extends StatefulWidget {
  const safehome({super.key});

  @override
  State<safehome> createState() => _safehomeState();
}

class _safehomeState extends State<safehome> {
  Position? _currentPosition;
  String? _currentAddress;
  String? emergencyNumber; // Store emergency number

  @override
  void initState() {
    super.initState();
    _getCurrentLocation();
    _loadEmergencyNumber();
  }

  Future<void> _getCurrentLocation() async {
    LocationPermission permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        Fluttertoast.showToast(msg: "Location permission is denied");
        return;
      }
    }

    if (permission == LocationPermission.deniedForever) {
      Fluttertoast.showToast(
          msg:
              "Location permission is permanently denied. Please enable it in settings.");
      return;
    }

    try {
      Position position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        forceAndroidLocationManager: true,
      );

      setState(() {
        _currentPosition = position;
      });

      _getAddressFromLatLon();
    } catch (e) {
      Fluttertoast.showToast(msg: e.toString());
    }
  }

  Future<void> _getAddressFromLatLon() async {
    if (_currentPosition == null) {
      Fluttertoast.showToast(msg: "Location not available");
      return;
    }

    try {
      List<Placemark> placemarks = await placemarkFromCoordinates(
        _currentPosition!.latitude,
        _currentPosition!.longitude,
      );

      if (placemarks.isNotEmpty) {
        Placemark place = placemarks[0];
        setState(() {
          _currentAddress =
              "${place.locality ?? "Unknown Locality"}, ${place.postalCode ?? "Unknown Postal Code"}, ${place.street ?? "Unknown Street"}";
        });
      }
    } catch (e) {
      Fluttertoast.showToast(msg: e.toString());
    }
  }

// add new
  Future<void> _saveEmergencyNumber(String number) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setString('emergencyNumber', number);
    setState(() {
      emergencyNumber = number;
    });
    Fluttertoast.showToast(msg: "Emergency contact updated successfully!");
  }

  final TextEditingController _numberController = TextEditingController();

  void _updateEmergencyNumber() {
    String newNumber = _numberController.text.trim();
    if (newNumber.isNotEmpty) {
      _saveEmergencyNumber(newNumber);
    } else {
      Fluttertoast.showToast(msg: "Please enter a valid number");
    }
  }

  Future<void> _loadEmergencyNumber() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    setState(() {
      emergencyNumber = prefs.getString('emergencyNumber') ?? '';
    });
    _numberController.text = emergencyNumber ?? ''; // Update text field
  }

// can delete
  // Future<void> _loadEmergencyNumber() async {
  //   SharedPreferences prefs = await SharedPreferences.getInstance();
  //   setState(() {
  //     emergencyNumber = prefs.getString('emergencyNumber') ?? '';
  //   });
  // }

  void showModel(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (context) {
        return Container(
          height: MediaQuery.of(context).size.height * 0.5,
          decoration: BoxDecoration(
            color: const Color.fromARGB(100, 101, 95, 95),
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(30),
              topRight: Radius.circular(30),
            ),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Padding(
                padding: EdgeInsets.all(10),
                child: Text(
                  "SEND YOUR CURRENT LOCATION IMMEDIATELY TO YOUR EMERGENCY CONTACTS",
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 20,
                  ),
                ),
              ),
              Text(_currentAddress ?? "Fetching address..."),
              ElevatedButton(
                onPressed: _getCurrentLocation,
                child: const Text("GET LOCATION"),
              ),
              ElevatedButton(
                onPressed: () async {
                  if (emergencyNumber == null || emergencyNumber!.isEmpty) {
                    Fluttertoast.showToast(msg: "No emergency contact set!");
                    return;
                  }

                  if (_currentPosition == null) {
                    Fluttertoast.showToast(msg: "Location not available!");
                    return;
                  }

                  String mapsLink =
                      "https://www.google.com/maps?q=${_currentPosition!.latitude},${_currentPosition!.longitude}";
                  String message = "I need help! My location: $mapsLink";

                  final Uri smsUri = Uri.parse(
                      "sms:$emergencyNumber?body=${Uri.encodeComponent(message)}");

                  if (!await launchUrl(smsUri)) {
                    Fluttertoast.showToast(msg: "Could not send SMS");
                  }
                },
                child: const Text("SEND LOCATION"),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () => showModel(context),
      child: Card(
        elevation: 5,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        child: Container(
          height: 150,
          width: MediaQuery.of(context).size.width * 0.9,
          decoration: const BoxDecoration(),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  children: [
                    const ListTile(
                      title: Text("Send Location"),
                      subtitle: Text("Share Location"),
                    ),
                  ],
                ),
              ),
              ClipRRect(
                borderRadius: BorderRadius.circular(20),
                child: Image.asset('images/route.jpeg'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
