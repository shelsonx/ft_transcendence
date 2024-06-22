import { HttpClient, HttpClientRequestData } from './httpClient.js';
import { BlockingService } from './userManagementService.js';
class GameInfoService {

	constructor() {
		this.httpClient = new HttpClient('https://localhost:8003');
	}
	async gameInfo() {
		const home = new HttpClientRequestData('GET', '/dash/home/');
		const response = await this.httpClient.makeRequest(home);
		return response;
	}
	async totalInfos() {
		const total_infos = new HttpClientRequestData('GET', '/dash/total_infos/');
		const response = await this.httpClient.makeRequest(total_infos);
		return response;
	}
	async get_user(id){
		const user = new HttpClientRequestData('GET', `/dash/user/${id}/`);
		const response = await this.httpClient.makeRequest(user);
		return response;
	}
	async getUsersBlocks(user_id){
    const blockingService = new BlockingService();
		return await blockingService.getBlockedUsers();
	}
}

export default new GameInfoService();
