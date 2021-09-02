import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/router.dart';
import 'package:provider/provider.dart';
import 'package:SigaCrud/controllers/login_provider.dart';

class LoginForms extends StatefulWidget {
  @override
  _LoginFormsState createState() => _LoginFormsState();
}

class _LoginFormsState extends State<LoginForms> {
  FocusNode _usernameFocus;
  FocusNode _passwordFocus;

  @override
  void initState() {
    _usernameFocus = FocusNode();
    _passwordFocus = FocusNode();
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
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
            ),
            onPressed: () => {
            Navigator.pushReplacementNamed(context, homeRoute)
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
              initialValue: 'admin@sigacrud.com.br',
              validator: loginProvider.validateUsername,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Nome de Usuário',
                labelStyle: Theme.of(context).textTheme.subtitle,
              ),
              keyboardType: TextInputType.emailAddress,
              onSaved: (value) => loginProvider.username = value,
              focusNode: _usernameFocus,
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
              initialValue: 'teste123',
              validator: loginProvider.validatePwd,
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Senha',
                labelStyle: Theme.of(context).textTheme.subtitle,
              ),
              obscureText: true,
              keyboardType: TextInputType.text,
              onSaved: (value) => loginProvider.password = value,
              focusNode: _passwordFocus,
              textInputAction: TextInputAction.done,
              onFieldSubmitted: (_) async {
                FocusScope.of(context).unfocus();
                loginProvider.handleSingIn().then(
                  (result) {
                    if (result == null)
                      return null;
                    else if (result.status)
                      //TODO alterar quando entrar a autenticação do firebase
                      Navigator.pushReplacementNamed(context, homeRoute);
                    else if (!result.status) return null; //show login error
                  },
                );
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
                    loginTextFields(),
                    Container(
                      alignment: Alignment.centerRight,
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: <Widget>[
                          submitLoginButton(),
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
