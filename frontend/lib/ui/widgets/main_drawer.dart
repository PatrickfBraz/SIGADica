import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/router.dart';

class MainDrawer extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: <Widget>[
          DrawerHeader(
            child: Center(
              child: Text(
                'Siga Crud',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
            decoration: BoxDecoration(
              color: Colors.blue,
            ),
          ),
          ListTile(
            title: Text('Home'),
            onTap: () {
              Navigator.pushReplacementNamed(context, homeRoute);
            },
          ),
          ListTile(
            title: Text('Teste'),
            onTap: () {
              Navigator.pushReplacementNamed(context, testeRoute);
            },

          ),
          ListTile(
            title: Text('Logout'),
            onTap: () {
              Navigator.pushReplacementNamed(context, loginRoute);
            },

          ),
        ],
      ),
    );
  }
}
