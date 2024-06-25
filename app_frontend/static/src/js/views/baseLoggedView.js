import View, { ViewOptions } from "../contracts/view.js";
import NavHandler from "../router/navigation/navHandler.js";
import { NavItems } from "../router/navigation/navItem.js";

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
    const navHandler = new NavHandler(navItems);
    super(new ViewOptions(html, start, navHandler));
  }
}

export default BaseLoggedView;
