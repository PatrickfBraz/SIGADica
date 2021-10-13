import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/widgets/main_appbar.dart';
import 'package:SigaCrud/ui/widgets/main_drawer.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: MainAppBar(
          appBarTitle: 'Home',
        ),
        drawer: MainDrawer(),
        body: Center(
          child: SingleChildScrollView(
              child: Column(
            children: <Widget>[
              Container(
                padding: EdgeInsets.all(50),
                child: Center(),
              ),
              Text(
                  'A ideia e aqui ficar a pesquisa de disciplinas que será implementada',
                  style: TextStyle(fontSize: 50)),
              Container(),
            ],
          )),
        ));
  }

  Widget _search(Function search) {
    return Container(
      width: 200,
      child: TextField(
        onChanged: (value) {
          search(value);
        },
        style: TextStyle(fontSize: 16, color: Colors.grey[600]),
        decoration: InputDecoration(
          enabledBorder: OutlineInputBorder(
            borderSide: BorderSide(
              color: Colors.green,
            ),
          ),
          suffixIcon: Icon(Icons.search),
          border: InputBorder.none,
          hintText: "Buscar",
          contentPadding: const EdgeInsets.only(
            left: 16,
            right: 20,
            top: 14,
            bottom: 14,
          ),
        ),
      ),
    );
  }
}
