class AuthenticationResult {
  bool status;
  String errorCode;
  String errorMessage;
  String uid;
}
// Utilizarei ele para o firebase por isso a classe está aqui
class AuthenticationServices {
  static Future<AuthenticationResult> emailSingIn(String username, String password) async {
    AuthenticationResult authResult = AuthenticationResult();
    try {
      return authResult;
    } catch (error) {
      authResult.errorCode = error.code;
      authResult.errorMessage = error.message;
      authResult.status = false;
      return authResult;
    }
  }

}
