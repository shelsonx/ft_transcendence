import { ElementDisplay } from "../components/elementDisplay.js";
import Toast from "../components/toast.js";
import { ApiError } from '../contracts/apiError.js';
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
    let apiResult;
    try {
      this.#loader.display();
      const result = await (serviceFunction.bind(service))(...args);
      apiResult = new ApiResonse(result?.data ?? result, result?.message ?? 'OK', true);
    } catch (error) {
      if (error instanceof ApiError) {
        apiResult = new ApiResonse(null, `Status: ${error.status} - ${error.message}`, false);
      } else {
        apiResult = new ApiResonse(null, error?.message ?? "Something went wrong!", false);
      }
    } finally {
      this.#loader.remove();
      const isError = !apiResult.is_success;
      this.#toast.display(
        isError ? 'Error' : 'Success',
        apiResult.message,
        isError ? 'danger' : 'success'
      );
    }
    return apiResult;
  }
}

export default new WrapperLoadingService(loader, toast);
