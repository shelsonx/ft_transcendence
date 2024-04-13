import Router from "../contracts/router.js";
import {
  hashRoutes as routes
} from "./routes.js"; /**
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

  /**
   * Route to a view based on the current location.
   * If no matching route is found, redirects to the root ("/").
   */
  route() {
    let location = window.location.hash.replace(/^#/, "").split("?")[0];
    if (location.length === 0) {
      location = "/";
    }
    const route = this.routes[location] || this.routes["404"];
    this.render(route);
  }

  start() {
    window.addEventListener("hashchange", () => {
      this.route();
    });
    window.addEventListener("DOMContentLoaded", () => {
      this.route();
    });
    this.route();
  }
}

export default new HashRouter(routes);