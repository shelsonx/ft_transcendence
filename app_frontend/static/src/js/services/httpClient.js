import { AuthConstants } from "../constants/auth-constants.js";
import { ApiError } from "../contracts/apiError.js";
import { ApiResonse } from "../contracts/apiResponse.js";
import languageHandler from "../locale/languageHandler.js";
import { getCookie } from "../utils/getCookie.js";
import { replaceCookieTokenToStorage } from "../utils/replaceLocalStorageByCookie.js";

/**
 * Class representing the data for an HTTP client request.
 */
export class HttpClientRequestData {
  #defaultHeaders;

  /**
   * Create a new HttpClientRequestData.
   * @param {string} method - The HTTP method.
   * @param {string} endpoint - The endpoint URL.
   * @param {Object} data - The data to send in the request.
   * @param {Object} headers - The headers for the request.
   */
  constructor(method, endpoint, data, headers) {
    this.method = method;
    this.endpoint = endpoint;
    this.data = data;
    this.#defaultHeaders = {
      'Content-Type': 'application/json'
    }
    this.headers = !headers ? this.#defaultHeaders : {
      ...this.#defaultHeaders,
      ...headers
    };
  }
}

/**
 * Class representing an HTTP client.
 */
export class HttpClient {

  /**
   * Create a new HttpClient.
   * @param {string} baseUrl - The base URL for the HTTP client.
   */
  constructor(baseUrl, shouldAppendLanguage = true) {
    this.baseUrl = baseUrl;
    this.baseUrlWithLanguage = baseUrl;
    this.languageHandler = languageHandler;
    this.shouldAppendLanguage = shouldAppendLanguage;
  }

  /**
   * Change the base URL of the HTTP client.
   * @param {string} url - The new base URL.
   */
  changeBaseUrl(url) {
    this.baseUrl = url;
  }

  addJwtToken(httpClientRequestData) {
    const jwtToken = localStorage.getItem(AuthConstants.AUTH_TOKEN);
    if (jwtToken) {
      httpClientRequestData.headers['Authorization'] = `Bearer ${jwtToken}`;
    }
  }

  addCsrfToken(httpClientRequestData) {
    const csrftoken = getCookie('csrftoken');
    if (csrftoken) {
      httpClientRequestData.headers['X-CSRFToken'] = csrftoken;
    }
  }

  getFormUrlencodedBody(data) {
    const params = [];
    for (const property in data) {
      const encodedKey = encodeURIComponent(property);
      let encodedValue = encodeURIComponent(data[property]);
      if (!data[property]) encodedValue = encodeURIComponent("");
      params.push(encodedKey + "=" + encodedValue);
    }

    return params.join("&");
  }

  async #toResponse(response) {
    if (response.ok) {
      const content_type = response.headers.get("content-type")
      if (content_type.includes("text/html")) {
        return await response.text();
      }
      return await response.json();
    } else if (response.status >= 300 && response.status < 400) {
      return new ApiResonse(null, "Redirect", false);
    }

    let apiError = null;
    try {
      const error = await response.json()
      apiError = new ApiError(error?.message ?? JSON.stringify(error) , response.status);
      // if (response.status === 401) {
      //   localStorage.removeItem(AuthConstants.AUTH_TOKEN);
      //   window.location.href = '/#login';
      // }
    } catch(err) {
      apiError = new ApiError(
        'An error occurred while processing your request',
        response.status
      );
    }
    throw apiError;
  }

  /**
   * Make a POST request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #post(httpClientRequestData) {
    let body = JSON.stringify(httpClientRequestData.data);
    if (
      httpClientRequestData.headers["Content-Type"] ===
      "application/x-www-form-urlencoded"
    )
      body = this.getFormUrlencodedBody(httpClientRequestData.data);

    const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
      method: 'POST',
      headers: httpClientRequestData.headers,
      body: body
    });
    return await this.#toResponse(response);
  }

  /**
   * Make a GET request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #get(httpClientRequestData) {
    const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
      method: 'GET',
      headers: httpClientRequestData.headers,
    });
    return await this.#toResponse(response);
  }

  /**
 * Make a PUT request.
 * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
 * @returns {Promise<Object>} The response data.
 */
  async #put(httpClientRequestData) {
    let body = JSON.stringify(httpClientRequestData.data);
    if (
      httpClientRequestData.headers["Content-Type"] ===
      "application/x-www-form-urlencoded"
    )
      body = this.getFormUrlencodedBody(httpClientRequestData.data);

    const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
      method: 'PUT',
      headers: httpClientRequestData.headers,
      body: body
    });
    return await this.#toResponse(response);
  }
  /**
   * Make a DELETE request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #delete(httpClientRequestData) {
    const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
      method: 'DELETE',
      headers: httpClientRequestData.headers,
    });
    return await this.#toResponse(response);

  }

  /**
   * Make a PATCH request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   * @throws {Error} If the HTTP method is invalid.
   */
  async #patch(httpClientRequestData) {
    const contentTypes = ["application/x-www-form-urlencoded", "default"];
    const contentType = httpClientRequestData.headers["Content-Type"];

    if (contentTypes.includes(contentType)) {
      let body;

      if (contentType === "default") {
        httpClientRequestData.headers["Content-Type"] = "application/json";
        body = JSON.stringify(httpClientRequestData.data);
      }
      else body = this.getFormUrlencodedBody(httpClientRequestData.data);

      const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
        method: 'PATCH',
        headers: httpClientRequestData.headers,
        body: body,
      });
      return await this.#toResponse(response);
    }

    let formData = new FormData();

    for (const key in httpClientRequestData.data) {
      if (httpClientRequestData.data[key] !== null && httpClientRequestData.data[key] !== undefined) {
        formData.append(key, httpClientRequestData.data[key]);
      }
    }

    try {
      const response = await fetch(this.baseUrlWithLanguage + httpClientRequestData.endpoint, {
        method: 'PATCH',
        body: formData,
        headers: new Headers({
          'Authorization': 'Bearer ' + localStorage.getItem(AuthConstants.AUTH_TOKEN),
        }),
      });

      return await this.#toResponse(response);
    } catch (error) {
      throw error;
    }
  }


  /**
   * Make an HTTP request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   * @throws {Error} If the HTTP method is invalid.
   */
  //lalala => lalala/pt-br
  //lalala/

  appendLanguage() {
    if (this.languageHandler.getLocale() === "en") {
      this.baseUrlWithLanguage = this.baseUrl;
      return ;
    }
    const locale = languageHandler.getLocale();
    const baseUrl = this.baseUrl;
    if (baseUrl.endsWith('/')) {
      this.baseUrlWithLanguage = `${baseUrl}${locale}/`;
    } else {
      this.baseUrlWithLanguage = `${baseUrl}/${locale}`;
    }
  }

  async makeRequest(httpClientRequestData) {
    if (!httpClientRequestData) {
      throw new Error('Request data is required');
    }
    const httpVerb = { 'GET': this.#get.bind(this), 'POST': this.#post.bind(this), 'PUT': this.#put.bind(this), 'DELETE': this.#delete.bind(this), 'PATCH': this.#patch.bind(this) };
    this.addCsrfToken(httpClientRequestData);
    const httpRequest = httpVerb?.[httpClientRequestData.method?.toUpperCase()];
    if (!httpRequest) {
      throw new Error('Invalid HTTP method');
    }
    if (this.shouldAppendLanguage) {
      this.appendLanguage();
    }
    replaceCookieTokenToStorage(AuthConstants.AUTH_TOKEN);
    this.addJwtToken(httpClientRequestData);
    const response = await httpRequest(httpClientRequestData);
    return response;
  }
}

