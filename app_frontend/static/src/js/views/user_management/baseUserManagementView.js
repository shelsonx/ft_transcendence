import View, { ViewOptions } from '../../contracts/view.js';
import NavHandler from '../../router/navigation/navHandler.js';
import { NavItems } from '../../router/navigation/navItem.js';

class userManagementView extends View {
  constructor({
    html,
    start
  }) {
    const navItems = [
      new NavItems('#user-profile', 'Profile', { 'data-i18n-key': 'user-management--profile',}),
      new NavItems('#user-settings', 'Settings', { 'data-i18n-key': 'user-management--settings',}),
      new NavItems('#search-users', 'Search', { 'data-i18n-key': 'user-management--search',}),
    ];
    const addStart = () => {
      start();
    };

    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, addStart, navHandler));
  }
}

export default userManagementView;