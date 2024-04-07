import View, { ViewOptions } from '../../contracts/view.js';
import NavHandler from '../../router/navigation/navHandler.js';
import { NavItems } from '../../router/navigation/navItem.js';

class BaseAuthView extends View {
  constructor({
    html,
    start
  }) {
    const navItems = [
      new NavItems('#login', 'Login'),
      new NavItems('#sign-up', 'Sign Up',),
    ];
    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, start, navHandler));
  }
}

export default BaseAuthView;