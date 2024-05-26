class LoginType {
  static AUTH_EMAIL = "email";
  static AUTH_42 = "42_auth";
  static loginTypes = [LoginType.AUTH_EMAIL, LoginType.AUTH_42];
  constructor(name) {
    if (!LoginType.loginTypes.includes(name)) {
      throw new Error(
        `Invalid login type: ${name}. Valid login types are: ${LoginType.loginTypes}`
      );
    }
    this.name = name;
  }
  static createLoginTypeFromObj(obj) {
    if ("name" in obj === false) {
      throw new Error(
        "Cannot create LoginType from object. The object must have a 'name' property."
      );
    }
    return new LoginType(obj.name);
  }
}

class User {
  constructor(
    id,
    userName,
    email,
    loginType,
    enable2fa,
    createdAt,
    updatedAt,
    isActive,
    isFirstLogin,
    token,
  ) {
    this.id = id;
    this.userName = userName;
    this.email = email;
    this.loginType = LoginType.createLoginTypeFromObj(loginType);
    this.enable2fa = enable2fa;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.isActive = isActive;
    this.isFirstLogin = isFirstLogin;
    this.token = token;
  }
  static createUserFromObj(obj) {
    const mustHaveKeys = {
      id: 0,
      user_name: 0,
      email: 0,
      login_type: 0,
      enable_2fa: 0,
      created_at: 0,
      updated_at: 0,
      is_active: 0,
      is_first_login: 0,
      token: 0,
    };
    for (let key in mustHaveKeys) {
      if (!obj.hasOwnProperty(key)) {
        throw new Error(`Cannot create User from object. The object must have a '${key}' property.`);
      }
    }
    return new User(
      obj.id,
      obj.user_name,
      obj.email,
      obj.login_type,
      obj.enable_2fa,
      obj.created_at,
      obj.updated_at,
      obj.is_active,
      obj.is_first_login,
      obj.token,
    );
  }
}

export { LoginType, User };
