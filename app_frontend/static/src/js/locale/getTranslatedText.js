export const getTranslatedText = (id, text, context) => {
  document.getElementById(id).addEventListener('custom:onLanguageChange', (e) => {
    const selectedLanguage = e.detail.language;
    e.target.textContent = context[selectedLanguage][text];
  });
}