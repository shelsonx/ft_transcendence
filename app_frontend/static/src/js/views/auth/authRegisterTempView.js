
import authService from '../../services/authService.js';
import wrapperLoadingService from '../../services/wrapperService.js';
import BaseAuthView from './baseAuthView.js';

class AuthRegisterTempView extends BaseAuthView {
    constructor(html, start) {
        super({ html, start });
    }
}


const html = /*html*/`
  <div class="container-fluid d-flex justify-content-center position-absolute top-50 start-50 translate-middle">
      <img class="space-man" src="static/src/img/transcendence-journey.svg" />
      <p>temp</p>
  </div>
`;

function start() {
  window.addEventListener('load', async () => {
    await wrapperLoadingService.execute(
        authService,
        authService.register42,
    );
    window.location.href = '/#';
  });
}

export default new AuthRegisterTempView(html, start);
