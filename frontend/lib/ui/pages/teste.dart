import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/widgets/main_appbar.dart';
import 'package:SigaCrud/ui/widgets/main_drawer.dart';

class TestePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: MainAppBar(appBarTitle: 'Teste',),
      drawer: MainDrawer(),
      body: Center(
        child: Text('Teste'),
      ),
    );
  }
}
