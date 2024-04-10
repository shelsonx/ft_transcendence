// New component
class Counter extends HTMLElement {
    constructor() {
        super();
        this.count = 0;
        this.innerHTML = /*html*/`
            <button>Clicks : ${this.count}</button>
        `;

        let btn = this.querySelector("button");

        // State
        btn.onclick = () => {
            btn.innerHTML = "Clicks : " + ++this.count;
        };
    }
}

customElements.define("click-counter", Counter);