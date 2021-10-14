import 'package:flutter/material.dart';
import 'package:SigaCrud/ui/widgets/register_forms.dart';

class SignUpScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    Widget baseLoginPage = Center(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        mainAxisAlignment: MainAxisAlignment.center,
        children: <Widget>[
          Flexible(
            flex: 4,
            child: Container(
              height: screenWidth >= 1920 ? null : 150,
              alignment: Alignment.centerLeft,
              padding: EdgeInsets.only(left: 50, right: 25),
              child: Image(
                image: AssetImage(
                    'assets/images/Minerva_Oficial_UFRJ_(Orientação_Horizontal).png'),
                fit: BoxFit.fitHeight,
              ),
            ),
          ),
          Flexible(
            flex: 3,
            child: Center(
              child: Container(
                height: screenHeight > 400 ? null : 400,
                alignment: Alignment.centerRight,
                decoration: BoxDecoration(
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black38,
                        offset: Offset(-5, 0),
                        blurRadius: 10,
                      )
                    ],
                    gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          Color(0xFF00304a),
                          Color(0xFF094563),
                          Color(0xFF4392b4),
                        ]),
                    borderRadius:
                        BorderRadius.horizontal(left: Radius.circular(5000))),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: <Widget>[
                    Padding(
                      padding: const EdgeInsets.symmetric(
                          horizontal: 60, vertical: 20),
                      child: Text(
                        "Registre - se",
                        textAlign: TextAlign.end,
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                      ),
                    ),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: <Widget>[
                        RegisterForms(),
                        SizedBox(
                          width: 50,
                        )
                      ],
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );

    Widget smallScreenLoginPage = Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Color(0xFF00304a),
            Color(0xFF094563),
            Color(0xFF4392b4),
          ],
        ),
      ),
      child: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Container(
              padding: EdgeInsets.symmetric(vertical: 50),
              child: Center(
                child: Image(
                  image: AssetImage(
                      'assets/images/Minerva_Oficial_UFRJ_(Orientação_Horizontal).png'),
                  fit: BoxFit.contain,
                ),
              ),
            ),
            RegisterForms(),
          ],
        ),
      ),
    );

    if (screenWidth >= 1150) {
      if (screenHeight > 400) {
        return Material(
          child: baseLoginPage,
        );
      } else {
        return Material(
          child: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            child: baseLoginPage,
          ),
        );
      }
    } else {
      return Material(
        child: smallScreenLoginPage,
      );
    }
  }
}
