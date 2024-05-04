/**
 * Class representing a navigation item.
 */
export class NavItems {

  /**
   * Create a new NavItems.
   * @param {string} href - The href for the navigation item.
   * @param {string} text - The text for the navigation item.
   */
  constructor(href, text, attributes = {}) {
    this.href = href;
    this.text = text;
    this.attributes = attributes;
  }

  /**
   * Create a new navigation item element.
   * @returns {HTMLElement} The navigation item element.
   */
  createNavItem() {
    const navItem = document.createElement('li');
    navItem.classList.add('nav-item', 'custom-nav-item');
    const navLink = document.createElement('a', this.attributes);
    Object.keys(this.attributes).forEach((key) => {
      navLink.setAttribute(key, this.attributes[key]);
    });
    navLink.classList.add('nav-link', 'text-white');
    navLink.href = this.href;
    navLink.textContent = this.text;
    navItem.appendChild(navLink);
    return navItem;
  }
}
