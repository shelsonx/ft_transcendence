import View, { ViewOptions } from '../contracts/view.js';
import NavHandler from '../router/navigation/navHandler.js';
import { NavItems } from '../router/navigation/navItem.js';

class BaseLoggedView extends View {
  constructor({
    html,
    start
  }) {
    const navItems = [
      new NavItems('#user-profile', 'Profile'),
      new NavItems('#search-users', 'Search'),
      new NavItems('#user-settings', 'Settings'),
      new NavItems('#game-info', 'Ranking'),
      new NavItems('#play', 'Play'),
      new NavItems('#tournaments', 'Tournaments'),
    ];
    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, start, navHandler));
  }
}

export default BaseLoggedView;
