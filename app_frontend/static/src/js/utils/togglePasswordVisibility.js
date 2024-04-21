export function togglePasswordVisibility(inputId, iconId) {
  const showPasswordIcon = document.getElementById(iconId);
  showPasswordIcon.addEventListener('click', () => {
      const passwordInput = document.getElementById(inputId);
      if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
          showPasswordIcon.classList.remove('bi-eye-slash');
          showPasswordIcon.classList.add('bi-eye');
      } else {
          passwordInput.type = 'password';
          showPasswordIcon.classList.remove('bi-eye');
          showPasswordIcon.classList.add('bi-eye-slash');
      }
  });
}