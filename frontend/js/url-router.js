import { fetchUserProfile } from "./profile.js";

document.addEventListener("click", (e) => {
    console.log(e);
    const { target } = e;

    if (!target.matches("nav a")) return;

    e.preventDefault();
    urlRoute();
});

const urlRoutes = {
    404: {
        template: "templates/404.html",
        title: "404 - Page Not Found",
        description: "The page you are looking for does not exist."
    },
    "/about": {
        template: "templates/about.html",
        title: "About",
        description: "Learn more about our website."
    },
    "/settings": {
        template: "templates/settings.html",
        title: "Settings",
        description: "Change your website settings."
    },
    "/profile": {
        template: "templates/profile.html",
        title: "Profile",
        description: "Your user profile."
    },
}

/**
 * Handles the URL routing and updates the browser's history.
 * @param {Event} event - The event object triggered by the URL change.
 */
const urlRoute = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.href);
    urlLocationHandler();
}

/**
 * Handles the URL location and updates the content of the webpage accordingly.
 * @returns {Promise<void>} A promise that resolves when the content is updated.
 */
const urlLocationHandler = async () => {
    let location = window.location.pathname;
    if (length === 1) location = "/";

    const route = urlRoutes[location] || urlRoutes[404];
    const html = await fetch(route.template)
        .then((response) => response.text());

    document.getElementById("content").innerHTML = html;

    if (location === "/profile") fetchUserProfile();

}

urlLocationHandler();