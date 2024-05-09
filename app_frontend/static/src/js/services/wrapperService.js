import { ElementDisplay } from "../components/elementDisplay.js";
import Toast from "../components/toast.js";
import { ApiResonse } from '../contracts/apiResponse.js';

const loader = new ElementDisplay(
  'loader-container',
  /*html*/`<div class="position-absolute top-50 start-50 translate-middle z-3">
    <div class="loader-inner position-relative d-flex flex-column justify-content-center align-items-center">
      <div class="loader"></div>
      <span>Loading</span>
  </div>
</div>`
);

const toast = new Toast(
  'toast-container position-absolute top-0 start-50 translate-middle-x p-3 z-3',
);

class WrapperLoadingService {
  #loader
  #toast

  constructor(loader, toast) {
    this.#loader = loader
    this.#toast = toast
  }
  async execute(service, serviceFunction, ...args) {
    let result;
    try {
      this.#loader.display();
      result = await (serviceFunction.bind(service))(...args);
    } catch (error) {
      result = new ApiResonse(null, error?.message ?? "Something went wrong!", false);
    } finally {
      this.#loader.remove();
      const isError = !result.is_success;
      this.#toast.display(
        isError ? 'Error' : 'Success',
        result.message,
        isError ? 'danger' : 'success'
      );
    }
    return result;
  }
}

export default new WrapperLoadingService(loader, toast);