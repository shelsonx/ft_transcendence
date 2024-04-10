export function loadImage(imagePath, callbackFunction) {
  fetch(`static/src/img/${imagePath}`)
  .then(response => response.text())
  .then(data => {
      callbackFunction(data);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}