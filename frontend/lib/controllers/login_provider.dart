import 'package:flutter/material.dart';

enum ViewState { Idle, Busy }

class LoginProvider extends ChangeNotifier {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  String _password = "";
  String _username = "";
  String _registration = "";
  String _confirmPassword = "";
  // String _userUid;
  bool _wrongCredentials = false;

  //Salvar a classe usuário futuramente para registro interno

  set username(value) => _username = value;
  set registration(value) => _registration = value;
  set confirmPassword(value) => _confirmPassword = value;
  set password(value) => _password = value;

  get username => _username;
  get password => _password;

  // view state management
  ViewState _state = ViewState.Idle;
  ViewState get state => _state;
  void setState(ViewState viewState) {
    _state = viewState;
    notifyListeners();
  }

  GlobalKey<FormState> get formKey => _formKey;
}
