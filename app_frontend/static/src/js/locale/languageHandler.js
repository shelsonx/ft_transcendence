import { AuthConstants } from "../constants/auth-constants.js";
import { CustomEvents } from "../constants/custom-events.js";
import { UserInformationService } from "../services/userManagementService.js";
import { getUserId } from "../utils/getUserId.js";

class LanguageHandler {
  #locale;
  #defaultLocale;
  constructor() {
    this.#defaultLocale = 'en';
    this.#locale = localStorage.getItem(AuthConstants.AUTH_LOCALE) || 'en';
    this.dropDownMenu = document.getElementById('change-language-menu');
    this.hasSetup = false;
    this.translations = {};
    this.buttonsRef = [];
    this.supportedLanguages = {
        'English': {
          code: 'en',
          fullCode: 'en-US',
          name: 'English',
        },
        'French': {
          code: 'fr',
          fullCode: 'fr-FR',
          name: 'French',
        },
        'Portuguese (BR)': {
          code: 'pt-br',
          fullCode: 'pt-BR',
          name: 'Portuguese (BR)',
        }
      }
    };

  getLocaleDetails() {
    return Object.values(this.supportedLanguages).find(sl => sl.code === this.#locale) || this.supportedLanguages['English'];
  }

  setLocale(locale) {
    const langSelected = Object.values(this.supportedLanguages).find(lg => lg.code === locale);
    if (!langSelected) {
      locale = 'en';
    }
    this.#locale = locale;
    localStorage.setItem(AuthConstants.AUTH_LOCALE, locale);
  }

  getLocale() {
    return this.#locale;
  }

  setDefaultLocale(locale) {
    const langSelected = Object.values(this.supportedLanguages).find(lg => lg.code === locale);
    if (!langSelected) {
      locale = 'en';
    }
    this.#defaultLocale = locale;
    localStorage.setItem(AuthConstants.AUTH_LOCALE, locale);
  }

  getDefaultLocale() {
    return this.#defaultLocale;
  }


  addLanguagesToDropdown() {
    if (this.hasSetup) {
      return;
    }
    Object.keys(this.supportedLanguages).forEach((language) => {
      const li = document.createElement('li');
      const button = document.createElement('button', { type: 'button' });
      button.classList.add('dropdown-item', 'rounded', 'text-white');
      if (language === this.getLocaleDetails().name) {
        button.classList.add('active');
      }
      button.textContent = language;
      button.addEventListener('click', async (e) => await this.onLanguageChange(e));
      this.buttonsRef.push(button);
      li.appendChild(button);
      this.dropDownMenu.appendChild(li);
    })
    this.hasSetup = true;
  }


  formatNumber(value) {
    if (typeof value === "object" && value.number) {
      const { number, ...options } = value;
      const fullyQualifiedLocaleDefaults = this.getLocaleDetails().fullCode;
      return new Intl.NumberFormat(
        fullyQualifiedLocaleDefaults,
        options,
      ).format(number);
    } else {
      return value;
    }
  }

  formatDate(value) {
    if (typeof value === "object" && value.date) {
      let { date, ...options } = value;

      if (typeof date === "string" && !date.includes("T")) {
        date += "T00:00:00";
      }

      const parsedDate =
        typeof date === "string" ? Date.parse(date) : date;

      const fullyQualifiedLocaleDefaults = this.getLocaleDetails().fullCode;
      return new Intl.DateTimeFormat(
        fullyQualifiedLocaleDefaults,
        options,
      ).format(parsedDate);
    } else {
      return value;
    }
  }


  pluralFormFor(forms, count) {
    const matchingForm = new Intl.PluralRules(this.#locale).select(
      count,
    );

    return forms[matchingForm];
  }


  interpolate(message, interpolations) {
    return Object.keys(interpolations).reduce(
      (interpolated, key) => {
        const value = this.formatDate(
          this.formatNumber(interpolations[key]),
        );

        return interpolated.replace(
          new RegExp(`{\s*${key}\s*}`, "g"),
          value,
        );
      },
      message,
    );
  }


  translate(key, interpolations = {}) {
    const message = this.translations[key];

    if (key.endsWith("-plural")) {
      return this.interpolate(
        this.pluralFormFor(message, interpolations.count),
        interpolations,
      );
    }

    return this.interpolate(message, interpolations);
  }

  translateElement(element) {
    const key = element.getAttribute("data-i18n-key");

    const tooltip = element.getAttribute("data-i18n-tooltip");

    const options =
      JSON.parse(element.getAttribute("data-i18n-opt")) || {};

    element.innerText = this.translate(key, options);
    if (tooltip) {
      element.setAttribute("title", this.translate(tooltip, options));
    }
  }

  translatePage() {
    document
      .querySelectorAll("[data-i18n-key]")
      .forEach((el) => this.translateElement(el));
  }

  async fetchTranslationsFor(newLocale) {
    const response = await fetch(`static/src/js/locale/languages/${newLocale}.json`);
    return await response.json();
  }

  async handleLocation(newLocale) {
    this.setLocale(newLocale);
    const newTranslations = await this.fetchTranslationsFor(
      newLocale,
    );

    this.translations = newTranslations;
    document.documentElement.lang = newLocale;
    this.translatePage();
  }

  setActive(target) {
    this.buttonsRef.forEach((eachBtn) => {
      if (eachBtn !== target) {
        eachBtn.classList.remove('active');
      }
    });
    target.classList.add('active');
  }

  async onLanguageChange(e) {
    const language = e.target.textContent;
    this.setActive(e.target);
    const newLanguageSelected = this.supportedLanguages[language] || this.supportedLanguages['English'];
    this.handleLocation(newLanguageSelected.code);
    window.dispatchEvent(new CustomEvent(CustomEvents.LANGUAGE_CHANGE_EVENT, { detail: {lang: newLanguageSelected.code} }));
    try {
      const userInfoService = new UserInformationService();
      const { user: {
        name,
        nickname,
        two_factor_enabled,
        avatar,
        chosen_language,
        user_uuid,
        email,
        avatar_name,
      } } = await userInfoService.getUserData();

      await userInfoService.updateUserData({
        name,
        nickname,
        two_factor_enabled,
        avatar,
        user_uuid,
        email,
        avatar_name,
        chosen_language: newLanguageSelected.code
       });
    } catch  {

    }
  }

  changeLanguage(locale) {
    const langSelected = Object.values(this.supportedLanguages).find(lg => lg.code === locale);
    if (!langSelected) {
      return ;
    }
    const { name } = langSelected;
    for (const button of this.buttonsRef) {
      if (button.textContent === name) {
        button.click();
      }
    }
  }

  onInit(isFirstLoad = false) {
    this.addLanguagesToDropdown();
    const localeToUpdate = isFirstLoad ? this.getDefaultLocale() : this.getLocale();
    this.handleLocation(localeToUpdate);
  }
}

export default new LanguageHandler();
