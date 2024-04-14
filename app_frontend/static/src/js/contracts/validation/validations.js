class Validator {
  #type
  constructor(type) {
    this.#type = type;
  }

  createValidation(isValid, message = 'Ok') {
    return { isValid, type: this.#type, message };
  }

   validate(value, name = 'This field') {
    throw new Error('Method not implemented.');
  }
}

export class RequiredValidator extends Validator {
  constructor() {
    super('required');
  }
  validate(value, name = 'This field') {
    if (!value) {
      return this.createValidation(
        false,
        `${name} is required`);
    }
    return this.createValidation(true, 'ok');
  }
}

export class MinLengthValidator extends Validator {
  constructor(minLength) {
    super('minLength');
    this.minLength = minLength;
  }
  validate(value, name = 'This field') {
    if (value.length < this.minLength) {
      return this.createValidation(
        false,
        `${name} must be at least ${this.minLength} characters long`);
    }
    return this.createValidation(true, 'ok');
  }
}

export class MaxLengthValidator extends Validator {
  constructor(maxLength) {
    super('maxLength');
    this.maxLength = maxLength;
  }
  validate(value, name = 'This field') {
    if (value.length > this.maxLength) {
      return this.createValidation(
        false,
        `${name} must be at most ${this.maxLength} characters long`);
    }
    return this.createValidation(true, 'ok');
  }
}

export class UpperCaseValidation extends Validator {
  constructor(minQty) {
    super('upperCase');
    this.minQty = minQty;
  }
  validate(value, name = 'This field') {
    const upperCase = value.match(/[A-Z]/g) || [];
    if (upperCase.length < this.minQty) {
      return this.createValidation(
        false,
        `${name} must have at least ${this.minQty} uppercase characters`);
    }
    return this.createValidation(true, 'ok');
  }
}

export  class LowerCaseValidation extends Validator {
  constructor(minQty) {
    super('lowerCase');
    this.minQty = minQty;
  }
  validate(value, name = 'This field') {
    const upperCase = value.match(/[a-z]/g) || [];
    if (upperCase.length < this.minQty) {
      return this.createValidation(
        false,
        `${name} must have at least ${this.minQty} lowerCase characters`);
    }
    return this.createValidation(true, 'ok');
  }
}

export class EmailValidator extends Validator {
  constructor() {
    super('email');
  }
  validate(value, name = 'This field') {
    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailRegex.test(value)) {
      return this.createValidation(
        false,
        `${name} must be a valid email`);
    }
    return this.createValidation(true, 'ok');
  }
}

export class AllDigitValidator extends Validator {
  constructor() {
    super('digit');
  }
  validate(value, name = 'This field') {
    const digitRegex = /\d/;
    const isAllDigit = value.split('').every(char => digitRegex.test(char));
    if (!isAllDigit) {
      return this.createValidation(
        false,
        `${name} must be all digits (0-9)`);
    }
    return this.createValidation(true, 'ok');
  }
}