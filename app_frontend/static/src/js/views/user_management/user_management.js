import View from "../../contracts/view.js";
class UserManagementView extends View {
  constructor(html, start) {
    super({
      html,
      start
    },
  );
  }
}

const html = /*html*/`
  <h1 class="text-bg-dark">Hello World!</h1>
` 

const start = () => {
  console.log('User Management View')
}

export default new UserManagementView(html, start);