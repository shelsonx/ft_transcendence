import LanguageHandler from '../locale/languageHandler.js';
import { HttpClient } from './httpClient.js';

export class LanguageService {
  constructor(baseUrl) {
    this.languageHandler = LanguageHandler;
    this.baseApi = baseUrl;
    this.httpClient = new HttpClient(baseUrl, false);
  }

  addLanguageQueryString(httpClientRequestData){
    if (this.languageHandler.getLocale() === this.languageHandler.getDefaultLocale()) {
      return ;
    }
    httpClientRequestData.endpoint += '?language=' + this.languageHandler.getLocale();
  }

  async makeRequest(httpClientRequestData) {
    this.addLanguageQueryString(httpClientRequestData);
    const response = await this.httpClient.makeRequest(httpClientRequestData);
    return response;
  }
}
