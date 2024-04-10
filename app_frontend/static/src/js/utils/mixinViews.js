import View from '../contracts/view.js';
class MixinViews extends View {
  constructor(html, views) {
    const start = this.#createStart(views);
    super(html, start)
  }

  #createStart(views) {
    return () => {
      for (const view of views) {
        view.start();
      }
    }
  }
}

export default MixinViews;