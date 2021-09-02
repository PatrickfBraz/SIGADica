import 'package:flutter/material.dart';
import 'package:SigaCrud/controllers/auth.dart';

enum ViewState { Idle, Busy }

class LoginProvider extends ChangeNotifier {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  String _password;
  String _username;
  // String _userUid;
  bool _wrongCredentials = false;

  AuthenticationResult _authResult;

  set username(value) => _username = value;
  set password(value) => _password = value;

  // view state management
  ViewState _state = ViewState.Idle;
  ViewState get state => _state;
  void setState(ViewState viewState) {
    _state = viewState;
    notifyListeners();
  }

  GlobalKey<FormState> get formKey => _formKey;

  String validateUsername(String input) {
    if (input == "admin@openlabs.com.br") {
      String regexString =
          r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,253}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,253}[a-zA-Z0-9])?)*$";
      RegExp validEmailPattern = RegExp(regexString);
      if (validEmailPattern.hasMatch(input)) {
        if (_wrongCredentials)
          return '';
        else
          return null;
      } else {
        return 'E-mail Inválido';
      }
    } else {
      return 'E-mail incorreto';
    }
  }

  String validatePwd(String input) {
    int pwdLenght = input.length;
    if (pwdLenght < 6 || pwdLenght > 16) {
      return 'Senha deve ter entre 6 e 16 caracteres';
    } else {
      if (_wrongCredentials)
        return 'Usuário e/ou Senha incorretos';
      else
        return null;
    }
  }

  bool _validateAndSaveFields() {
    final FormState _formState = _formKey.currentState;
    if (_formState.validate()) {
      _formState.save();
      return true;
    } else {
      return false;
    }
  }

  Future<AuthenticationResult> handleSingIn() async {
    _wrongCredentials = false;
    _authResult = null;
    if (_validateAndSaveFields()) {
      // set view as busy, so it shows a loading indicator
      this.setState(ViewState.Busy);
      _authResult =
          await AuthenticationServices.emailSingIn(_username, _password);

      //debugPrint(_authResult.status.toString());
      //debugPrint(_authResult.errorCode.toString());
      //debugPrint(_authResult.errorMessage.toString());

      if (_authResult.errorCode == 'auth/user-not-found' ||
          _authResult.errorCode == 'auth/wrong-password') {
        _wrongCredentials = true;
        _validateAndSaveFields();
      }

      // _userUid = authResult.uid;
      this.setState(ViewState.Idle);
    }
    return _authResult;
  }
}
