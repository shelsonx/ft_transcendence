import { getCookie } from './getCookie.js';
export function replaceCookieTokenToStorage(cookieName) {
  const jwtTokenFromCookie = getCookie(cookieName);
  if (jwtTokenFromCookie) {
    localStorage.setItem(cookieName, jwtTokenFromCookie.replaceAll('"', ""));
    document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
  }
}