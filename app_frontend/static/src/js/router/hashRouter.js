import { AuthConstants } from "../constants/auth-constants.js";
import Router from "../contracts/router.js";
import authService from "../services/authService.js";
import { replaceCookieTokenToStorage } from "../utils/replaceLocalStorageByCookie.js";
import {
  hashRoutes as routes
} from "./routes.js";
/**
* Class representing a router.
*/
class HashRouter extends Router {

  /**
   * Create a router.
   * @param {Object.<string, {title: string, render: function, start: function, description: string}>} routes - The routes the router should handle.
   */
  constructor(routes) {
    super(routes);
  }

  /**
   * Render a view.
   * @param {{title: string, render: function, description: string}} view - The view to render.
   */
  render(view) {
    super.render(view);
    document.querySelector('meta[name="description"]').setAttribute("content", view.description);
  }

  async checkIsAuthenticated() {
    replaceCookieTokenToStorage(AuthConstants.AUTH_TOKEN);
    const token = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    if (!token) {
      window.location.href = '/#login';
      return false;
    }
    const response = await authService.getMe();
    if (response.is_success) {
      return true;
    } else {
      window.location.href = '/#login';
      return false;
    }
  }

  /**
   * Route to a view based on the current location.
   * If no matching route is found, redirects to the root ("/").
   */
  route() {
    let location = window.location.hash.replace(/^#/, "");
    if (location.length === 0) {
      location = "/";
    }
    const route = this.routes[location] || this.routes["404"];
    if (route?.isProtected === true) {
      this.checkIsAuthenticated().then((isAuthenticated) => {
        if (isAuthenticated) {
          this.render(route);
        }
      });
    } else {
      this.render(route);
    }
  }

  start() {
    window.addEventListener("hashchange", () => {
      this.route();
    });
    window.addEventListener("DOMContentLoaded", () => {
      this.route();
    });
  }
}

export default new HashRouter(routes);