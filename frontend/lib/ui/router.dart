import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/pages/home.dart';
import 'package:SigaCrud/ui/pages/teste.dart';
import 'package:SigaCrud/ui/pages/loginScreen.dart';

const String homeRoute = '/';
const String loginRoute = '/login';
const String testeRoute = '/teste';

class Routers {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    WidgetBuilder builder;
    switch (settings.name) {
      case homeRoute:
        builder = (BuildContext _) => HomePage();
        break;
      case testeRoute:
        builder = (BuildContext _) => TestePage();
        break;
      case loginRoute:
        builder = (BuildContext _) => LoginScreen();
        break;


      default:
        return MaterialPageRoute(
          builder: (_) {
            return Scaffold(
              body: Center(
                child: Text('BUG: Rota não definida para ${settings.name}'),
              ),
            );
          },
        );
    }
    return MaterialPageRoute(builder: builder, settings: settings);
  }
}
