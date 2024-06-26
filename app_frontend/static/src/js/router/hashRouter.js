import { AuthConstants } from "../constants/auth-constants.js";
import Router from "../contracts/router.js";
import { User } from "../contracts/user.js";
import languageHandler from "../locale/languageHandler.js";
import authService from "../services/authService.js";
import { replaceCookieTokenToStorage } from "../utils/replaceLocalStorageByCookie.js";
import {
  hashRoutes as routes
} from "./routes.js";
import { changeLanguageWhenLogin } from "../utils/changeLanguage.js";
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

  redirectUserToLogin() {
    this.user = null;
    window.location.href = '/#login';
    return false
  }

  async checkIsAuthenticated() {
    replaceCookieTokenToStorage(AuthConstants.AUTH_TOKEN);
    const token = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    if (!token) {
      return this.redirectUserToLogin();
    }
    if (this?.user?.token === token) {
      return true;
    }
    try {
      const response = await authService.getMe();
      if (response.is_success) {
        this.user = User.createUserFromObj({
          ...response.data,
          token,
        });
        return true;
      } else {
        return this.redirectUserToLogin();
      }
    } catch(e) {
     return this.redirectUserToLogin();
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
      languageHandler.onInit();
    });
    window.addEventListener("DOMContentLoaded", () => {
      this.route();
      languageHandler.onInit(true);
    });
    const logout = document.getElementById('logout-button');
    if (logout) {
      logout.addEventListener('click', async () => {
        await authService.logout();
      });
    }
  }
}

export default new HashRouter(routes);
