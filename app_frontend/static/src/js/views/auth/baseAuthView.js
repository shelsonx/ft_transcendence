import View, { ViewOptions } from '../../contracts/view.js';
import NavHandler from '../../router/navigation/navHandler.js';
import { NavItems } from '../../router/navigation/navItem.js';
import { loadImage } from '../../utils/loadImage.js';

const createSpaceMan = (data) => {
  const svg = document.createElement('svg');
  svg.innerHTML = data;
  svg.classList.add('space-man')
  const div = document.querySelector('.space-man-container');
  div.appendChild(svg);
}

class BaseAuthView extends View {
  constructor({
    html,
    start
  }) {
    const navItems = [
      new NavItems('#login', 'Login'),
      new NavItems('#sign-up', 'Sign Up',),
    ];
    const addStart = () => {
      start();
      loadImage('transcendence-journey.svg', createSpaceMan);
    };
    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, addStart, navHandler));
  }
}

export default BaseAuthView;