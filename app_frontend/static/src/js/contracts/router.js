class Router {
  /**
   * Create a router.
   * @param {Object.<string, {title: string, render: function, start: function, description: string}>} routes - The routes the router should handle.
   */
  constructor(routes) {
    this.routes = routes;
    this.user = null;
  }
  /**
   * Render a view.
   * @param {{title: string, render: function, start: function, description: string}} view - The view to render.
   */
  render(view) {
    const app = document.getElementById("app");
    document.title = view.title;
    app.innerHTML = view.render.renderHtml();
    view.render.start(this.user);
  }

  start() {
    throw new Error("render method not implemented");
  }
}

export default Router;
