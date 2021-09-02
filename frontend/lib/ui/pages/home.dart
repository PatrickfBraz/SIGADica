import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/widgets/main_appbar.dart';
import 'package:SigaCrud/ui/widgets/main_drawer.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MainAppBar(appBarTitle: 'Home',),
      drawer: MainDrawer(),
      body: Center(
        child: SingleChildScrollView(
        child: Column(
        children: <Widget>[
          Container(
            padding: EdgeInsets.all(50),
            child: Center(
              child: Image(
                image: AssetImage('assets/images/Claudio.jpg'),
                fit: BoxFit.fill,
              ),
            ),
          ),
          Text('Miceli, imagine aqui o inicio da aplicação',style: TextStyle(fontSize: 50)),
          Container(),
    ],
    )),
    ));
  }
}
