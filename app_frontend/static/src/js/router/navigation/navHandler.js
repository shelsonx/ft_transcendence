class NavHandler {

  constructor(navItems = []) {
    this.navItems = navItems;
  }

  #hasNavItems() {
    return this.navItems && this.navItems.length > 0;
  }

  addToNavbar() {
    const mainNav = document.querySelector('#main-nav .navbar-nav');
    if (!mainNav || this.#hasNavItems() === false) {
      return;
    }
    const customNavItems = mainNav.querySelectorAll('.custom-nav-item');
    if (customNavItems.length > 0) {
      customNavItems.forEach(item => item.remove());
    }
    for (const navItem of this.navItems) {
      mainNav.appendChild(navItem.createNavItem());
    }
  }
}

export default NavHandler;