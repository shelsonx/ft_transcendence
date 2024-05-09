export class ApiResonse {
  constructor(data, message, is_success) {
    this.data = data;
    this.message = message;
    this.is_success = is_success;
  }
}
