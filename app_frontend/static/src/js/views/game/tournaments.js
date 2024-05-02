import BaseLoggedView from '../baseLoggedView.js';


class TournamentsView extends BaseLoggedView {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <h1 class="text-bg-dark">Tournaments View</h1>
`

const start = () => {
  console.log('Tournaments View')
}

export default new TournamentsView(html, start);
