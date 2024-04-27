import { HttpClient, HttpClientRequestData } from './httpClient.js';

class GameInfoService {

	constructor() {
		this.httpClient = new HttpClient('http://localhost:8003/dash/');
	}
	async gameInfo() {
		const home = new HttpClientRequestData('GET', 'home/');
		const response = await this.httpClient.makeRequest(home);
		return response;
	}
	async totalInfos() {
		const total_infos = new HttpClientRequestData('GET', 'total_infos/');
		const response = await this.httpClient.makeRequest(total_infos);
		return response;
	}
}

export default new GameInfoService();