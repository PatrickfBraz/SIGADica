import 'package:SigaCrud/controllers/authentication.dart';
import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/router.dart';
import 'package:provider/provider.dart';
import 'package:SigaCrud/controllers/login_provider.dart';

class RegisterForms extends StatefulWidget {
  @override
  _RegisterFormsState createState() => _RegisterFormsState();
}

class _RegisterFormsState extends State<RegisterForms> {
  FocusNode _emailFocus = new FocusNode();
  FocusNode _passwordFocus = new FocusNode();
  FocusNode _confirmPasswordFocus = new FocusNode();
  FocusNode _matriculaFocus = new FocusNode();
  String? loginStatus;
  late TextEditingController textControllerEmail;
  late TextEditingController textControllerPassword;
  late TextEditingController textControllerConfirmPassword;
  late TextEditingController textControllerMatricula;
  bool _isRegistering = false;
  Color loginStringColor = Colors.green;
  bool _isEditingEmail = false;
  bool _isEditingMatricula = false;
  bool _isEditingPassword = false;
  bool _isEditingConfirmPassword = false;

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

  String? _validatePassword(String value, String value2) {
    value = value.trim();
    value2 = value2.trim();

    if (textControllerPassword.text.isNotEmpty &&
        textControllerConfirmPassword.text.isNotEmpty) {
      if (value.isEmpty || value2.isEmpty) {
        return 'Senha não pode ser vazia';
      } else if (value.length < 6) {
        return 'Senha não pode ser menor que 6 caracteres';
      } else if (value2.length < 6) {
        return 'Confirmar senha menor que 6 caracteres';
      } else if (value != value2) {
        return 'As senhas não conferem';
      }
    }

    return null;
  }

  @override
  void initState() {
    _emailFocus = FocusNode();
    _passwordFocus = FocusNode();
    _confirmPasswordFocus = FocusNode();
    _matriculaFocus = FocusNode();
    textControllerEmail = TextEditingController();
    textControllerPassword = TextEditingController();
    textControllerConfirmPassword = TextEditingController();
    textControllerMatricula = TextEditingController();
    textControllerEmail.text = '';
    textControllerPassword.text = '';
    textControllerConfirmPassword.text = '';
    textControllerMatricula.text = '';
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
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
            onPressed: () async {
              setState(() {
                _isRegistering = true;
              });
              await registerWithEmailPassword(
                      textControllerEmail.text, textControllerPassword.text)
                  .then((result) {
                if (result != null) {
                  setState(() {
                    loginStatus = 'Registro efetuado com sucesso';
                    loginStringColor = Colors.green;
                  });
                  print(result);
                }
              }).catchError((error) {
                print('Registration Error: $error');
                setState(() {
                  loginStatus = 'Erro na hora de registrar';
                  loginStringColor = Colors.red;
                });
              });

              setState(() {
                _isRegistering = false;
              });

              Navigator.pushReplacementNamed(context, loginRoute);
            },
          ),
        );
      });
    }

    Widget backButton() {
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
                          Icons.arrow_back,
                          color: Color(0xFF3bc2d7),
                        ),
                        SizedBox(
                          width: 10.0,
                        ),
                        Text(
                          "Voltar",
                          maxLines: 1,
                          style: TextStyle(color: Colors.white),
                        ),
                      ],
                    )
                  : CircularProgressIndicator(
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
            ),
            onPressed: () =>
                {Navigator.pushReplacementNamed(context, loginRoute)},
          ),
        );
      });
    }

    Widget registerTextFields() {
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
                FocusScope.of(context).requestFocus(_matriculaFocus);
              },
            ),
            SizedBox(
              height: 20,
            ),
            TextFormField(
              controller: textControllerMatricula,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Matricula / DRE',
                labelStyle: Theme.of(context).textTheme.subtitle1,
              ),
              keyboardType: TextInputType.none,
              autofocus: false,
              onChanged: (value) {
                setState(() {
                  _isEditingMatricula = true;
                });
              },
              focusNode: _matriculaFocus,
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
                errorText: _isEditingEmail
                    ? _validatePassword(textControllerPassword.text,
                        textControllerConfirmPassword.text)
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
              onFieldSubmitted: (_) async {
                FocusScope.of(context).unfocus();
                FocusScope.of(context).requestFocus(_confirmPasswordFocus);
              },
            ),
            SizedBox(
              height: 20,
            ),
            TextFormField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Confirmar Senha',
                labelStyle: Theme.of(context).textTheme.subtitle1,
                errorText: _isEditingEmail
                    ? _validatePassword(textControllerConfirmPassword.text,
                        textControllerPassword.text)
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
              focusNode: _confirmPasswordFocus,
              textInputAction: TextInputAction.done,
              onFieldSubmitted: (_) async {
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
          key: loginProvider.formKey,
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
                    registerTextFields(),
                    Container(
                      alignment: Alignment.centerRight,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          backButton(),
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
