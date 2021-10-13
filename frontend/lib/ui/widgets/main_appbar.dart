import 'package:flutter/material.dart';

class MainAppBar extends AppBar {
  final String appBarTitle;
  MainAppBar({@required this.appBarTitle})
      : super(
          centerTitle: false,
          title: Text(
            appBarTitle,
            textAlign: TextAlign.left,
            style: TextStyle(
              color: Colors.white,
              fontSize: 22,
              fontWeight: FontWeight.bold,
            ),
          ),
        );
}
