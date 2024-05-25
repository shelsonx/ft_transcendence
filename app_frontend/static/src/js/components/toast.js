import { ElementDisplay } from './elementDisplay.js';

class Toast extends ElementDisplay {
  #types
  constructor(className, html) {
    super(className, html);
    this.#types = {
      success: {
        bg: 'bg-success',
        icon: 'bi-check-circle',
      },
      danger: {
        bg: 'bg-danger',
        icon: 'bi-x-circle',
      },
      warning: {
        bg: 'bg-warning',
        icon: 'bi-exclamation-circle',
      },
    }
  }
  display(title, message, type, duration = 5000) {
    const types = this.#types[type] ?? this.#types['success'];
    super.display(
      /*html*/`<div class="toast bg-dark fade show" role="alert" aria-live="assertive" aria-atomic="true" >
      <div class="toast-header ${types.bg} text-white flex justify-content-between align-items-center">
        <i style="font-size: 24px;line-height: 24px;"class="bi ${types.icon ?? ''} p-0 border-0 m-0"></i>
        <strong>${title}</strong>
        <button type="button" class="btn-close text-white" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body text-center">
        ${message}
      </div>`
    );
    setTimeout(() => {
         super.remove();
    }, type === 'danger' ? duration * 2 : duration);
  }
}

export default Toast;
