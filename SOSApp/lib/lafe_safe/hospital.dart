import 'package:flutter/material.dart';

class hospital extends StatelessWidget {
  const hospital(this.openmapf, {super.key});
  final Function openmapf;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(left: 20),
      child: Column(
        children: [
          InkWell(
            onTap: () {
              openmapf("hospital near me");
            },
            child: Card(
              elevation: 3,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20)),
              child: SizedBox(
                height: 50,
                width: 50,
                child: Center(
                  child: Image.asset(
                    'images/hospital.png',
                    height: 32,
                  ),
                ),
              ),
            ),
          ),
          Text("hospitals")
        ],
      ),
    );
  }
}
