import { AuthConstants } from "../constants/auth-constants.js";
import { getCookie } from "../utils/getCookie.js";
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
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
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

  /**
   * Make a POST request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #post(httpClientRequestData) {
    const response = await fetch(this.baseUrl + httpClientRequestData.endpoint, {
      method: 'POST',
      headers: httpClientRequestData.headers,
      body: JSON.stringify(httpClientRequestData.data)
    });
    return await response.json();
  }


  /**
   * Make a GET request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #get(httpClientRequestData) {
    const response = await fetch(this.baseUrl + httpClientRequestData.endpoint);
    return await response.json();
  }

    /**
   * Make a PUT request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #put(httpClientRequestData) {
    const response = await fetch(this.baseUrl + httpClientRequestData.endpoint, {
      method: 'PUT',
      headers: httpClientRequestData.headers,
      body: JSON.stringify(httpClientRequestData.data)
    });
    return await response.json();
  }
  /**
   * Make a DELETE request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   */
  async #delete(httpClientRequestData) {
    const response = await fetch(this.baseUrl + httpClientRequestData.endpoint, {
      method: 'DELETE',
      headers: httpClientRequestData.headers,
    });
    return await response.json();
  }
  /**
   * Make an HTTP request.
   * @param {HttpClientRequestData} httpClientRequestData - The data for the request.
   * @returns {Promise<Object>} The response data.
   * @throws {Error} If the HTTP method is invalid.
   */

  async makeRequest(httpClientRequestData) {
    if (!httpClientRequestData) {
      throw new Error('Request data is required');
    }
    const httpVerb = {'GET': this.#get.bind(this), 'POST': this.#post.bind(this), 'PUT': this.#put.bind(this), 'DELETE': this.#delete.bind(this)};
    this.addCsrfToken(httpClientRequestData);
    const httpRequest = httpVerb?.[httpClientRequestData.method?.toUpperCase()];
    if (!httpRequest) {
      throw new Error('Invalid HTTP method');
    }
    this.addJwtToken(httpClientRequestData);
    const response = await httpRequest(httpClientRequestData);
    return response;
  }
}

