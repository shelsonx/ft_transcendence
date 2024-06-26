import notFound from "../views/404.js";
import authRegisterTempView from "../views/auth/authRegisterTempView.js";
import forgotPassword from "../views/auth/forgotPassword.js";
import login from "../views/auth/login.js";
import signup from "../views/auth/signup.js";
import twoFactorAuth from "../views/auth/validate2Factor.js";
import home from "../views/home.js";
import userProfile from "../views/user_management/user-profile.js";
import searchUsers from "../views/user_management/search-users.js";
import userSettings from "../views/user_management/user-settings.js";
import GameInfoView from "../views/game-info/game_info.js";
import MyGamesView from "../views/game/my_games.js";
import SeeUserGamesView from "../views/game/view_user_games.js";
import NewGameView from "../views/game/new_game.js";
import ValidateGameView from "../views/game/validate_game.js";
import PongGameView from "../views/game/pong.js";
import TournamentsView from "../views/game/tournaments.js";
import MyTournamentsView from "../views/game/my_tournaments.js";
import NewTournamentView from "../views/game/new_tournament.js";
import ValidateTournamentView from "../views/game/validate_tournament.js";
import TournamentDetailView from "../views/game/tournament.js";

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
  "login": { title: "Login", render: login, description: "Login to your account."},
  "sign-up": { title: "Signup", render: signup, description: "Create an account." },
  "404": { title: "Not Found", render: notFound, description: "The page you are looking for does not exist."},
  "two-factor-auth": { title: "Two Factor Auth", render: twoFactorAuth, description: "Two Factor Authentication."},
  "auth-register-temp": { title: "Register Auth 42", render: authRegisterTempView, description: "Register 42."},
  "forgot-password": { title: "Forgot Password", render: forgotPassword, description: "Forgot Password."},
  "/": { title: "Home", render: home, description: "Pong games", isProtected: true },
  "user-profile": { title: "User Profile", render: userProfile, description: "View user profile.", isProtected: true},
  "search-users": { title: "Search Users", render: searchUsers, description: "Search for users.", isProtected: true},
  "user-settings": { title: "Settings", render: userSettings, description: "Change user settings.", isProtected: true},
  "game-info": { title: "Game info", render: GameInfoView, description: "Game info page.", isProtected: true},
  "play": { title: "Play Pong", render: NewGameView, description: "Play pong", isProtected: true },
  "verify-player": { title: "Verify player", render: ValidateGameView, description: "Verify", isProtected: true },
  "pong": { title: "Play Pong", render: PongGameView, description: "Play pong", isProtected: true },
  "my-games": { title: "My Games", render: MyGamesView, description: "My games", isProtected: true },
  "view-user-games": { title: "View user Games", render: SeeUserGamesView, description: "View user games", isProtected: true },
  "tournaments": { title: "Tournaments", render: TournamentsView, description: "Tournaments", isProtected: true },
  "my-tournaments": { title: "My Tournaments", render: MyTournamentsView, description: "My Tournaments", isProtected: true },
  "add-tournament": { title: "Create a Tournament", render: NewTournamentView, description: "Create a Tournament", isProtected: true },
  "verify-players": { title: "Verify players", render: ValidateTournamentView, description: "Verify", isProtected: true },
  "tournament": { title: "Tournament detail", render: TournamentDetailView, description: "Tournament detail", isProtected: true },
};

export {
  hashRoutes,
  pathRoutes
};
