
import { EmailValidator, IsEqualInputValidator, LowerCaseValidation, MaxLengthValidator, MinLengthValidator, RequiredValidator, UpperCaseValidation } from './validations.js';

export class ValidatorInput {
  #id
  #displayName
  #validators
  #displayGroup
  #input
  constructor(id, displayGroup = null, displayName = null, validators = []) {
    this.#id = id;
    this.#input = document.getElementById(id)
    this.#displayGroup = this.#setDisplayGroup(displayGroup);
    this.#displayName = displayName ?? id;
    this.#validators = validators;
    this.errors = [];
  }

  #setDisplayGroup(displayGroup) {
    if (!displayGroup) {
      return this.#input.parentElement;
    } 
    return document.getElementById(this.#displayGroup);
  }

  setDisplayName(displayName) {
    this.#displayName = displayName;
  }

  #createError(error) {
    const errorElement = document.createElement('div');
    errorElement.classList.add('invalid-feedback');
    errorElement.textContent = error.message;
    return errorElement;
  }

  #createSuccess() {
    const successElement = document.createElement('div');
    successElement.classList.add('valid-feedback', 'text-center');
    successElement.textContent = 'Ok';
    return successElement;
  }

  #clearFeedback() {
    this.#input.classList.remove('is-invalid');
    this.#input.classList.remove('is-valid');
    const allFeedback = this.#displayGroup.querySelectorAll('.invalid-feedback, .valid-feedback');
    allFeedback.forEach(fdb => {
      fdb.remove();
    });
  }

  #appendErrors() {
    this.#input.classList.add('is-invalid');
    this.errors.forEach(error => {
      this.#displayGroup.appendChild(this.#createError(error));
    });
  }

  #appendSuccess() {
    this.#input.classList.add('is-valid');
   this.#displayGroup.appendChild(this.#createSuccess());
  }

  validate() {
    const value = this.#input.value;
    this.#validators.forEach(validator => {
      const result = validator.validate(value, this.#displayName);
      if (!result.isValid) {
        this.errors.push(result);
      }
    });
    this.#clearFeedback();
    if (this.errors.length > 0) {
      this.#appendErrors();
      return false;
    }
    this.#appendSuccess();
    return true;
  }
}

export class RequiredInputValidator extends ValidatorInput {
  constructor(id, inputName) {
    super(id, null, inputName, [
      new RequiredValidator(),
    ]);
  }

}

export class PasswordInputValidator extends ValidatorInput {
  constructor(id) {
    super(id, null, 'Password', [
      new RequiredValidator(),
      new UpperCaseValidation(1),
      new LowerCaseValidation(1),
      new MinLengthValidator(8),
      new MaxLengthValidator(100),
    ]);
  }
}

export class EmailValidatorInput extends ValidatorInput {
  constructor(id) {
    super(id, null, 'Email', [
      new RequiredValidator(),
      new EmailValidator(),
    ]);
  }
}

export class TwoFactorCodeValidatorInput extends ValidatorInput {
  constructor(id) {
    super(id, null, 'Two Factor Code', [
      new RequiredValidator(),
      new MinLengthValidator(6),
      new MaxLengthValidator(6),
    ]);
  }
}

export class ConfirmPasswordInputValidator extends ValidatorInput {
  constructor(id, compareId) {
    super(id, null, 'Confirm Password', [
      new IsEqualInputValidator(compareId)
    ]);
  }
}

export class UsernameValidatorInput extends ValidatorInput {
  constructor(id) {
    super(id, null, 'Username', [
      new RequiredValidator(),
      new MinLengthValidator(4),
      new MaxLengthValidator(100),
    ]);
  }
}