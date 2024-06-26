export const getFrontErrorMessage = (error) => {
  switch (error) {
    case 400:
      return "Bad Request";
    case 401:
      return "Unauthorized";
    case 403:
      return "Forbidden";
    case 404:
      return "Not Found";
    // case 405:
    //   return "Method Not Allowed";
    // case 408:
    //   return "Request Timeout";
    // case 500:
    //   return "Internal Server Error";
    // case 501:
    //   return "Not Implemented";
    // case 502:
    //   return "Bad Gateway";
    // case 503:
    //   return "Service Unavailable";
    // case 504:
    //   return "Gateway Timeout";
    default:
      return "Ooops! An error occured.<br>Try again later";
  }
};

export const loadErrorMessage = (error, elementId) => {
  if (error.status === undefined || error.status === null) {
    error.status = 500;
    error.message = getFrontErrorMessage(500);
  }
  const swapContainer = document.getElementById(elementId);
  swapContainer.innerHTML = /*html*/ `
    <h1 class="error-message text-center">
      ${error.status} <br> ${error.message}
    </h1>`;
};

export const pageNotFoundMessage = (elementId) => {
  const message = document.getElementById(elementId);
  message.innerHTML = /*html*/ `
    <h1 class="error-message" data-i18n-key="page-not-found--title">
      Page not Found
    </h1>`;
};
