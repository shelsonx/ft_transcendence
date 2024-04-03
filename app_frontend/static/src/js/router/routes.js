import notFound from "../views/404.js";
import login from "../views/login.js";
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
  "404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
};

export {
  hashRoutes,
  pathRoutes
};
