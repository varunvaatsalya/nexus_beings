import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';

final _firebase = FirebaseAuth.instance;

class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final _formkey = GlobalKey<FormState>();
  var _islogin = true;
  var _enteremail = '';
  var enterpassword = '';
  void _submit() async {
    final isvalid = _formkey.currentState!.validate();
    if (!isvalid) {
      return;
    }

    if (isvalid) {
      _formkey.currentState!.save();
      try {
        if (_islogin) {
          //login
          final UserCredential = await _firebase.signInWithEmailAndPassword(
              email: _enteremail, password: enterpassword);
        } else {
          final UserCredential = await _firebase.createUserWithEmailAndPassword(
              email: _enteremail, password: enterpassword);
        }
      } on FirebaseAuthException catch (error) {
        if (error.code == 'email already in use') {}
        ScaffoldMessenger.of(context).clearSnackBars();
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(error.message ?? 'authentication failed')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Theme.of(context).colorScheme.primary,
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                margin: const EdgeInsets.only(
                  top: 30,
                  bottom: 20,
                  left: 20,
                  right: 20,
                ),
                child: Card(
                  margin: const EdgeInsets.all(20),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Form(
                      key: _formkey,
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: 'Email Address',
                              border: OutlineInputBorder(),
                            ),
                            keyboardType: TextInputType.emailAddress,
                            autocorrect: false,
                            textCapitalization: TextCapitalization.none,
                            validator: (value) {
                              if (value == null ||
                                  value.trim().isEmpty ||
                                  !value.contains('@')) {
                                return 'please enter a valid email address';
                              }
                              return null;
                            },
                            onSaved: (value) {
                              _enteremail = value!;
                            },
                          ),
                          SizedBox(
                            height: 10,
                          ),
                          TextFormField(
                            decoration: const InputDecoration(
                              labelText: 'password',
                              border: OutlineInputBorder(),
                            ),
                            obscureText: true,
                            validator: (value) {
                              if (value == null || value.trim().length < 6) {
                                return 'password must be at least 6 characters long';
                              }
                              return null;
                            },
                            onSaved: (value) {
                              enterpassword = value!;
                            },
                          ),
                          SizedBox(
                            height: 30,
                          ),
                          ElevatedButton(
                              onPressed: _submit,
                              style: ElevatedButton.styleFrom(
                                  backgroundColor: Theme.of(context)
                                      .colorScheme
                                      .primaryContainer),
                              child: Text(_islogin ? "Log in" : "Sign up")),
                          TextButton(
                            onPressed: () {
                              setState(() {
                                _islogin = !_islogin;
                              });
                            },
                            child: Text(_islogin
                                ? "create new account"
                                : "I already have an account "),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
