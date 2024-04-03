export default class View {
  constructor(html, start = () => {}) {
    this.html = html;
    this.start = start;
  }
  renderHtml() {
    return this.html;
  }
  start() {
    this.start();
  }
}