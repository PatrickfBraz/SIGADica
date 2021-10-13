import 'package:SigaCrud/controllers/authentication.dart';
import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/router.dart';
import 'package:provider/provider.dart';
import 'package:SigaCrud/controllers/login_provider.dart';

class LoginForms extends StatefulWidget {
  @override
  _LoginFormsState createState() => _LoginFormsState();
}

class _LoginFormsState extends State<LoginForms> {
  late FocusNode _emailFocus;
  late FocusNode _passwordFocus;
  late TextEditingController textControllerEmail;
  late TextEditingController textControllerPassword;
  bool _isEditingEmail = false;
  bool _isEditingPassword = false;
  bool _isLoggingIn = false;

  String? loginStatus;
  Color loginStringColor = Colors.green;

  //Validador de email
  String? _validateEmail(String value) {
    value = value.trim();

    if (textControllerEmail.text.isNotEmpty) {
      if (value.isEmpty) {
        return 'Email can\'t be empty';
      } else if (!value.contains(RegExp(
          r"^[a-zA-Z0-9.a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~]+@[a-zA-Z0-9]+\.[a-zA-Z]+"))) {
        return 'Enter a correct email address';
      }
    }

    return null;
  }

  String? _validatePassword(String value) {
    value = value.trim();

    if (textControllerPassword.text.isNotEmpty) {
      if (value.isEmpty) {
        return 'Password can\'t be empty';
      } else if (value.length < 6) {
        return 'Length of password should be greater than 6';
      }
    }

    return null;
  }

  final _formLoginKey = GlobalKey<FormState>();

  @override
  void initState() {
    _emailFocus = FocusNode();
    _passwordFocus = FocusNode();
    textControllerEmail = TextEditingController();
    textControllerPassword = TextEditingController();
    textControllerEmail.text = '';
    textControllerPassword.text = '';
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    Widget submitLoginButton() {
      return Consumer<LoginProvider>(
          builder: (BuildContext context, LoginProvider loginProvider, _) {
        return SizedBox(
            height: 45,
            child: RawMaterialButton(
                constraints: BoxConstraints(minWidth: 45),
                fillColor: Color(0xFF094563),
                splashColor: Color(0xFF00304a),
                animationDuration: Duration(milliseconds: 600),
                child: Padding(
                  padding: EdgeInsets.all(
                      loginProvider.state == ViewState.Idle ? 10 : 0),
                  child: loginProvider.state == ViewState.Idle
                      ? Row(
                          mainAxisSize: MainAxisSize.min,
                          children: const <Widget>[
                            Icon(
                              Icons.face,
                              color: Color(0xFF3bc2d7),
                            ),
                            SizedBox(
                              width: 10.0,
                            ),
                            Text(
                              "Entrar",
                              maxLines: 1,
                              style: TextStyle(color: Colors.white),
                            ),
                          ],
                        )
                      : CircularProgressIndicator(
                          valueColor:
                              AlwaysStoppedAnimation<Color>(Colors.white),
                        ),
                ),
                onPressed: () async {
                  setState(() {
                    _isLoggingIn = true;
                    _emailFocus.unfocus();
                    _passwordFocus.unfocus();
                  });
                  if (_validateEmail(textControllerEmail.text) == null &&
                      _validatePassword(textControllerPassword.text) == null) {
                    await signInWithEmailPassword(textControllerEmail.text,
                            textControllerPassword.text)
                        .then((result) {
                      if (result != null) {
                        print(result);
                        setState(() {
                          loginStatus = 'You have successfully logged in';
                          loginStringColor = Colors.green;
                        });
                        Future.delayed(Duration(milliseconds: 500), () {
                          Navigator.of(context).pop();
                          Navigator.of(context).pushReplacementNamed(homeRoute);
                        });
                      }
                    }).catchError((error) {
                      print('Login Error: $error');
                      setState(() {
                        loginStatus = 'Erro na hora de logar';
                        loginStringColor = Colors.red;
                      });
                    });
                  } else {
                    setState(() {
                      loginStatus = 'Please enter email & password';
                      loginStringColor = Colors.red;
                    });
                  }
                  setState(() {
                    _isLoggingIn = false;
                    textControllerEmail.text = '';
                    textControllerPassword.text = '';
                    _isEditingEmail = false;
                    _isEditingPassword = false;
                  });
                }));
      });
    }

    Widget submitCadastrarButton() {
      return Consumer<LoginProvider>(
          builder: (BuildContext context, LoginProvider loginProvider, _) {
        return SizedBox(
          height: 45,
          child: RawMaterialButton(
            constraints: BoxConstraints(minWidth: 45),
            fillColor: Color(0xFF094563),
            splashColor: Color(0xFF00304a),
            animationDuration: Duration(milliseconds: 600),
            child: Padding(
              padding: EdgeInsets.all(
                  loginProvider.state == ViewState.Idle ? 10 : 0),
              child: loginProvider.state == ViewState.Idle
                  ? Row(
                      mainAxisSize: MainAxisSize.min,
                      children: const <Widget>[
                        Icon(
                          Icons.face,
                          color: Color(0xFF3bc2d7),
                        ),
                        SizedBox(
                          width: 10.0,
                        ),
                        Text(
                          "Cadastrar",
                          maxLines: 1,
                          style: TextStyle(color: Colors.white),
                        ),
                      ],
                    )
                  : CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
            ),
            onPressed: () => {
              Navigator.pushNamedAndRemoveUntil(
                  context, registerRoute, (route) => false)
            },
          ),
        );
      });
    }

    Widget loginTextFields() {
      return Consumer<LoginProvider>(
          builder: (BuildContext context, LoginProvider loginProvider, _) {
        return Column(
          children: [
            TextFormField(
              controller: textControllerEmail,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Email',
                labelStyle: Theme.of(context).textTheme.subtitle1,
                errorText: _isEditingEmail
                    ? _validateEmail(textControllerEmail.text)
                    : null,
                errorStyle: TextStyle(
                  fontSize: 12,
                  color: Colors.redAccent,
                ),
              ),
              autofocus: false,
              onChanged: (value) {
                setState(() {
                  _isEditingEmail = true;
                });
              },
              focusNode: _emailFocus,
              textInputAction: TextInputAction.next,
              onFieldSubmitted: (_) {
                FocusScope.of(context).unfocus();
                FocusScope.of(context).requestFocus(_passwordFocus);
              },
            ),
            SizedBox(
              height: 20,
            ),
            TextFormField(
              controller: textControllerPassword,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Senha',
                labelStyle: Theme.of(context).textTheme.subtitle1,
                errorText: _isEditingPassword
                    ? _validatePassword(textControllerPassword.text)
                    : null,
                errorStyle: TextStyle(
                  fontSize: 12,
                  color: Colors.redAccent,
                ),
              ),
              obscureText: true,
              keyboardType: TextInputType.text,
              autofocus: false,
              onChanged: (value) {
                setState(() {
                  _isEditingPassword = true;
                });
              },
              focusNode: _passwordFocus,
              textInputAction: TextInputAction.done,
              onFieldSubmitted: (_) {
                FocusScope.of(context).unfocus();
              },
            ),
            SizedBox(
              height: 10,
            ),
          ],
        );
      });
    }

    return Consumer<LoginProvider>(
        builder: (BuildContext context, LoginProvider loginProvider, _) {
      return Padding(
        padding: const EdgeInsets.all(10),
        child: Form(
          key: _formLoginKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Container(
                padding:
                    EdgeInsets.only(top: 10, left: 10, right: 10, bottom: 5),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                ),
                width: 375,
                child: Column(
                  children: <Widget>[
                    loginTextFields(),
                    Container(
                      alignment: Alignment.centerRight,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          submitLoginButton(),
                          SizedBox(
                            width: 50,
                          ),
                          submitCadastrarButton(),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      );
    });
  }
}
