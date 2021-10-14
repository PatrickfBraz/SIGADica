class User {
  late String name;
  late String registration;
  late String id;
  late String email;
  late bool active;
  late String profilePictureUrl;

  //Usuario para salvar as informações no banco local futuramente

  User(
      {required this.name,
      required this.registration,
      required this.id,
      required this.email,
      required this.active,
      required this.profilePictureUrl});

  User.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    registration = json['registration'];
    id = json['id'];
    email = json['email'];
    active = json['active'];
    profilePictureUrl = json['image_path'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    data['registration'] = this.registration;
    data['id'] = this.id;
    data['email'] = this.email;
    data['active'] = this.active;
    data['image_path'] = this.profilePictureUrl;

    return data;
  }
}
