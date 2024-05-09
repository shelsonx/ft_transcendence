import View from '../contracts/view.js';
class NotFoundView extends View {
    constructor(html, start) {
       super({html, start});
    }
}

const html = /*html*/`
    <h1
      data-i18n-key="page-not-found--title"
    >Page Not Found</h1>
`;


export default new NotFoundView(html, () => {});
