import NavHandler from '../router/navigation/navHandler.js';

export class ViewOptions {
  /**
   * Create a new ViewOptions.
   * @param {string} html - The HTML for the view.
   * @param {Function} start - The start function for the view.
   * @param {NavHandler} navHandler - The navigation items for the view.
   */
  constructor(html, start = () => {}, navHandler = new NavHandler()) {
    this.html = html;
    this.start = start;
    this.navHandler = navHandler;
  }

}
/**
 * Class representing a view.
 */
export default class View {
  #html;
  #start;
  #navHandler;
  /**
   * Create a new View.
   * @param {ViewOptions} viewOptions - The options for the view.
   */
  constructor(viewOptions) {
    this.#html = viewOptions.html ?? '';
    this.#start = viewOptions.start ?? (() => {});
    this.#navHandler = viewOptions.navHandler ?? new NavHandler();
  }
    /**
   * Render the HTML for the view.
   * @returns {string} The HTML for the view.
   */
  renderHtml() {
    return this.#html;
  }

  /**
   * Start the view.
   */
  start() {
    this.#start();
    this.#navHandler.addToNavbar();
  }
}