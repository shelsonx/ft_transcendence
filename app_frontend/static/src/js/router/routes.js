import notFound from "../views/404.js";
import authRegisterTempView from "../views/auth/authRegisterTempView.js";
import forgotPassword from "../views/auth/forgotPassword.js";
import login from "../views/auth/login.js";
import signup from "../views/auth/signup.js";
import twoFactorAuth from "../views/auth/validate2Factor.js";
import GameInfoView from "../views/game-info/game_info.js";
import NewGameView from "../views/game/new_game.js";
import PongGameView from "../views/game/pong.js";
import TournamentDetailView from "../views/game/tournament-detail.js";
import TournamentsView from "../views/game/tournaments.js";
import home from "../views/home.js";
import userProfile from "../views/user_management/user-profile.js";
import userSettings from "../views/user_management/user-settings.js";
import userManagement from "../views/user_management/user_management.js";


/**
 * An object representing the routes in the application.
 * Each key is a path, and the value is an object with a title and a render function.
 * @type {Object.<string, {title: string, render: function}>}
 */
const pathRoutes = {
  "/": { title: "Login", render: login, description: "Login to your account."},
  "/login": { title: "Login", render: login, description: "Login to your account."},
  "/404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
};

const hashRoutes = {
  "/": { title: "Home", render: home, description: "Pong games", isProtected: true },
  "login": { title: "Login", render: login, description: "Login to your account."},
  "sign-up": { title: "Signup", render: signup, description: "Create an account." },
  "404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
  "two-factor-auth": { title: "Two Factor Auth", render: twoFactorAuth, description: "Two Factor Authentication."},
  "auth-register-temp": { title: "Register Auth 42", render: authRegisterTempView, description: "Register 42."},
  "forgot-password": { title: "Forgot Password", render: forgotPassword, description: "Forgot Password."},
  "user-profile": { title: "User Profile", render: userProfile, description: "View user profile."},
  "user-settings": { title: "Settings", render: userSettings, description: "Change user settings."},
  "game-info": { title: "Game info", render: GameInfoView, description: "Game info page."},
  "play": { title: "Play Pong", render: NewGameView, description: "Play pong", isProtected: true },
  "pong": { title: "Play Pong", render: PongGameView, description: "Play pong", isProtected: true },  // posso receber um id da match...?
  "user-management": { title: "User Management", render: userManagement, description: "Manage users."},
  "tournaments": { title: "Tournaments", render: TournamentsView, description: "Game info page.", isProtected: true },
  "tournament": { title: "Tournament Detail", render: TournamentDetailView, description: "Game info page.", isProtected: true },
};

export {
  hashRoutes,
  pathRoutes
};
