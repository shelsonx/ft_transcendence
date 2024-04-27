
export class ElementDisplay {
  #id
  #className
  #html
  constructor(className, html) {
    const randomId = Math.random().toString(36).substring(2) + Date.now().toString(36) + Math.random().toString(36).substring(2);
    this.#id = randomId;
    this.#className = className;
    this.#html = html;
  }

  display(html = this.#html) {
    const app = document.querySelector('body');
    const displayDiv = document.createElement('div');
    displayDiv.innerHTML = html;
    displayDiv.setAttribute('id', this.#id);
    const classes = this.#className.split(' ').filter((c) => c !== '');
    displayDiv.classList.add(...classes);
    app.insertAdjacentElement('afterbegin', displayDiv);
  }

  remove() {
    const displayDiv = document.getElementById(this.#id);
    displayDiv.remove();
  }
}