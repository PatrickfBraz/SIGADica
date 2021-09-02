import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/router.dart';
import 'package:provider/provider.dart';

import 'controllers/login_provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MultiProvider(
        providers: [
      ChangeNotifierProvider<LoginProvider>(
        create: (_) => LoginProvider(),
      ),
    ],
      child:MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SigaCrud',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      onGenerateRoute: Routers.generateRoute,
      initialRoute: loginRoute,
    ));
  }
}
