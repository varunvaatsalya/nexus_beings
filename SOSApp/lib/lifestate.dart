import 'package:flutter/material.dart';
import 'package:fluttertoast/fluttertoast.dart';
import 'package:sos_app/lafe_safe/bus.dart';
import 'package:sos_app/lafe_safe/hospital.dart';
import 'package:sos_app/lafe_safe/pharmacies.dart';
import 'package:sos_app/lafe_safe/police.dart';
import 'package:url_launcher/url_launcher.dart';

class lifesafe extends StatelessWidget {
  const lifesafe({super.key});
  static Future<void> openmap(String location) async {
    String googleUrl = 'https://www.google.com/maps/search/$location';
    final Uri url = Uri.parse(googleUrl);
    try {
      await launchUrl(url);
    } catch (e) {
      Fluttertoast.showToast(msg: "something went wrong");
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 90,
      width: MediaQuery.of(context).size.width,
      child: ListView(
        physics: BouncingScrollPhysics(),
        scrollDirection: Axis.horizontal,
        children: [
          police(openmap),
          hospital(openmap),
          bus(openmap),
          pharmacies(openmap),
        ],
      ),
    );
  }
}
