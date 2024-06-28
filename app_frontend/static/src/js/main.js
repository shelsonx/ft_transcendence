import Router from "./router/hashRouter.js";
import { UserInformationService } from "./services/userManagementService.js";
import GameInfoService from "./services/gameInfoService.js";

const mainStart = () => {
    
  const getUserId = () => {
    try {
      const jwt = localStorage.getItem('transcendence-auth_token');
      if (!jwt) {
        return null;
      }

      const payloadBase64 = jwt.split('.')[1];
      const decodedPayload = JSON.parse(atob(payloadBase64));
      return decodedPayload.sub;
    } catch (error) {
      console.error('Error getting user ID:', error);
      return null;
    }
  };

  const userIdExists = getUserId();
  if (!userIdExists) {
    return ;
  }

  const throttleTime = 5000;
  let lastUpdate = 0;

  const updateUserStatus = async () => {
    const userId = getUserId();
      if (!userId) return;

    const userInformationService = new UserInformationService();
    const data = {
      status: 'active'
    };

    await userInformationService.updateUserStatus(data);

    const gameInfoData = {
      id_msc: userId,
      status: true
    }
    await GameInfoService.updateUserStatus(gameInfoData);
  }

  const updateUserStatusWithTimer = async () => {
    const currentTime = Date.now();
    if (currentTime - lastUpdate >= throttleTime) {
      lastUpdate = currentTime;

    await updateUserStatus();
    }
  };

  const updateUserToOffline = async () => {
    const userId = getUserId();
    if (!userId) return;

    const userInformationService = new UserInformationService();
    const data = {
      status: 'inactive'
    };
    await userInformationService.updateUserStatus(data)
      .then((response) => {
        console.log(`User status updated to offline for ${userId}:`, response);
      })
      .catch((error) => {
        console.error('Error updating status to offline:', error);
      });

      const gameInfoData = {
      id_msc: userId,
      status: false
    }
    await GameInfoService.updateUserStatus(gameInfoData);
  };

  window.addEventListener('load', updateUserStatus);
  window.addEventListener('focus', updateUserStatusWithTimer);

  window.addEventListener('beforeunload', function (e) {
    this.navigator.sendBeacon(`https://localhost:8006/user/${getUserId()}/status/`, JSON.stringify({ status: 'inactive' }));
    this.navigator.sendBeacon(`https://localhost:8003/dash/set_status_user/`, JSON.stringify({ status: false, id_msc: getUserId() }));
  });

  document.getElementById('logout-button').addEventListener('click', updateUserToOffline);

}


Router.start();
mainStart();

export default Router;