export class FormValidation {

  constructor(validators = []) {
    this.validators = validators;
  }

  isValid() {
    let isFormValid = true;
    if (this.validators.length === 0) {
      return false;
    }
    this.validators.forEach(validator => {
      if (!validator.validate()) {
        isFormValid = false;
      }
    })
    return isFormValid;
  }
}