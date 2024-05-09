import notFound from "../views/404.js";
import login from "../views/auth/login.js";
import signup from "../views/auth/signup.js";
import userProfile from "../views/user_management/user-profile.js";
import userSettings from "../views/user_management/user-settings.js";

/**
 * An object representing the routes in the application.
 * Each key is a path, and the value is an object with a title and a render function.
 * @type {Object.<string, {title: string, render: function}>}
 */
const pathRoutes = {
  "/": { title: "Login", render: login, description: "Login to your account."},
  "/login": { title: "Login", render: login, description: "Login to your account."},
  "/404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
};

const hashRoutes = {
  "/": { title: "Login", render: login, description: "Login to your account."},
  "login": { title: "Login", render: login, description: "Login to your account."},
  "sign-up": { title: "Signup", render: signup, description: "Create an account." },
  "404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
  "user-profile": { title: "User Profile", render: userProfile, description: "View user profile."},
  "user-settings": { title: "Settings", render: userSettings, description: "Change user settings."},
};

export {
  hashRoutes,
  pathRoutes
};
