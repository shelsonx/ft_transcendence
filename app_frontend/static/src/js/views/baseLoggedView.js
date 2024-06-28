import View, { ViewOptions } from "../contracts/view.js";
import NavHandler from "../router/navigation/navHandler.js";
import { NavItems } from "../router/navigation/navItem.js";
import { UserInformationService } from "../services/userManagementService.js";
import GameInfoService from "../services/gameInfoService.js";

class BaseLoggedView extends View {
  constructor({ html, start }) {
    const navItems = [
      new NavItems("#user-profile", "Profile", {
        "data-i18n-key": "user-management--profile",
      }),
      new NavItems("#search-users", "Search", {
        "data-i18n-key": "user-management--search",
      }),
      new NavItems("#user-settings", "Settings", {
        "data-i18n-key": "user-management--settings",
      }),
      new NavItems("#game-info", "Ranking", {
        "data-i18n-key": "game-info-menu",
      }),
      new NavItems("#play", "Play", { "data-i18n-key": "play-pong-menu" }),
      new NavItems("#tournaments", "Tournaments", {
        "data-i18n-key": "tournaments-menu",
      }),
    ];

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

    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, start, navHandler));

  }
}

export default BaseLoggedView;
