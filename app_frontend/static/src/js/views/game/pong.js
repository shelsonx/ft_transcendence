import BaseLoggedView from '../baseLoggedView.js';


class PongGameView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <h1 class="text-bg-dark">Play pong view</h1>
`

const start = () => {
  console.log('Pong Game View')
}

export default new PongGameView(html, start);
