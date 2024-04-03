import Router from "../contracts/Router.js";
import {
  pathRoutes as routes
} from "./routes.js";
/**
* Class representing a router.
*/
class PathRouter extends Router {

  /**
   * Create a router.
   * @param {Object.<string, {title: string, render: function, description: string}>} routes - The routes the router should handle.
   */
  constructor(routes) {
    super(routes);
  }
  /**
   * Route to a view based on the current location.
   * If no matching route is found, redirects to the root ("/").
   */
  route() {
    let pathName = location.pathname;
    if (pathName === "") {
      pathName = "/";
    }
    const view = this.routes?.[pathName] ?? this.routes["/404"];
    super.render(view);
  }
  /**
   * Handles click events on elements with a `data-link` attribute.
   * Prevents the default action, updates the browser's history, and routes to the clicked link.
   * @param {MouseEvent} e - The click event.
   */
  routeClick(e) {
    if (e.target.matches("[data-link]")) {
      e.preventDefault();
      history.pushState("", "", e.target.href);
      this.route();
    }
  }

  /**
   * Start the router.
   */
  start() {
    window.addEventListener("click", this.routeClick.bind(this));
    window.addEventListener("popstate", () => {
        this.route();
    });
    window.addEventListener("DOMContentLoaded", () => {
        this.route();
    });
  }
}

export default new PathRouter(routes);