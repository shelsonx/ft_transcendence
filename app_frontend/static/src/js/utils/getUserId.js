export function getUserId() {
    const jwt = localStorage.getItem('transcendence-auth_token');
    if (!jwt) {
      throw new Error('JWT not found in local storage');
    }
  
    const payloadBase64 = jwt.split('.')[1];
    const decodedPayload = JSON.parse(atob(payloadBase64));
    return decodedPayload.sub;
  }
  