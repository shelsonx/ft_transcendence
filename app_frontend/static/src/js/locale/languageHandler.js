class LanguageHandler {
  #language;
  constructor() {
    this.#language = 'en';
    this.dropDownMenu = document.getElementById('change-language-menu');

    this.supportedLanguages = {
        'English': {
          code: 'en',
          name: 'English',
        },
        'French': {
          code: 'fr',
          name: 'French',
        },
        'Portuguese (BR)': {
          code: 'pt-br',
          name: 'Portuguese (BR)',
        }
      }
    };
  

  setLanguage(language) {
    this.#language = language;
  }

  getLanguage() {
    return this.#language;
  }

  addLanguagesToDropdown() {
    Object.keys(this.supportedLanguages).forEach((language) => {
      const li = document.createElement('li');
      const button = document.createElement('button', { type: 'button' });
      button.classList.add('dropdown-item', 'rounded', 'text-white');
      button.textContent = language;
      li.appendChild(button);
      this.dropDownMenu.appendChild(li);
    })
  }

  onLanguageChange() {
    this.addLanguagesToDropdown();
    const buttons = this.dropDownMenu.querySelectorAll('button');
 
    buttons.forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const language = e.target.textContent;
        buttons.forEach((eachBtn) => {
          if (eachBtn !== e.target) {
            eachBtn.classList.remove('active');
          }
        });
        e.target.classList.add('active');
        const newLanguageSelected = this.supportedLanguages[language] || this.supportedLanguages['English'];
        this.setLanguage(newLanguageSelected.code);
        const languageCustomEvent = new CustomEvent('custom:onLanguageChange', {
          detail: {
            language: this.getLanguage(),
          },
        });
        document.dispatchEvent(languageCustomEvent);
      });
    });
  }
}

export default new LanguageHandler();