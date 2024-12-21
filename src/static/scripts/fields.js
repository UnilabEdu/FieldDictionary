class Validator {
  constructor(input) {
    this.input = input;
    this.inputGroup = this.input.closest(".input-group");
    this.label = this.inputGroup.querySelector("label").textContent;
    this.errorEl = this.inputGroup.querySelector(".client-field-error");
    this.isValid = true;
  }

  required() {
    if (!this.shouldValidate()) return;

    const val = this.getValue();
    console.log(val);

    if (val.length === 0) {
      this.setError(`შეავსეთ ველი`);
      return;
    }

    this.removeError();

    return this;
  }

  validateLength(min, max) {
    if (!this.shouldValidate()) return;

    const val = this.getValue();

    if (val.length < min || val.length > max) {
      this.setError(`${this.label} უნდა იყოს ${min}-დან ${max} სიმბოლომდე`);
      return;
    }

    this.removeError();

    return this;
  }

  validateRegex(regex, errMsg, negate = false) {
    if (!this.shouldValidate()) return;

    const val = this.getValue();

    if ((negate && regex.test(val)) || (!negate && !regex.test(val))) {
      this.setError(errMsg);
      return;
    }

    this.removeError();

    return this;
  }

  setError(msg) {
    this.errorEl.textContent = msg;
    this.errorEl.classList.add("active");
    this.isValid = false;
  }

  removeError() {
    this.errorEl.classList.remove("active");
    this.isValid = true;
  }

  shouldValidate() {
    return this && this.input.classList.contains("touched");
  }

  getValue() {
    return this.input.value;
  }
}

const errorableInputs = document.querySelectorAll(
  ".errorable-field input, .errorable-field textarea",
);

errorableInputs.forEach((input) => {
  input.addEventListener("blur", () => input.classList.add("touched"));
  if (input.value.length > 0) {
    input.classList.add("touched");
  }
});

const contactFields = document.querySelectorAll(
  "#contact-form input, #contact-form textarea",
);
const contactSubmitBtn = document.querySelector(
  '#contact-form button[type="submit"]',
);

// const contactForm = document.querySelector("#contact-form");

function validateForm() {
  const firstNameValidator = new Validator(
    document.querySelector('#contact-form input[name="first_name"]'),
  );
  const lastNameValidator = new Validator(
    document.querySelector('#contact-form input[name="last_name"]'),
  );
  const emailValidator = new Validator(
    document.querySelector('#contact-form input[name="email"]'),
  );
  const subjectValidator = new Validator(
    document.querySelector('#contact-form input[name="subject"]'),
  );
  const textValidator = new Validator(
    document.querySelector('#contact-form textarea[name="text"]'),
  );

  const isFormValid = [
    firstNameValidator
      .required()
      ?.validateRegex(
        /^[A-Za-zა-ჰ]+$/,
        "მხოლოდ ქართული და ინლისური ასოებია ნებადართული",
      )
      ?.validateLength(2, 50),
    lastNameValidator
      .required()
      ?.validateRegex(
        /^[A-Za-zა-ჰ]+$/,
        "მხოლოდ ქართული და ინლისური ასოებია ნებადართული",
      )
      ?.validateLength(2, 50),
    emailValidator
      .required()
      ?.validateRegex(/[ა-ჰ]+/, "ქართული ასოები არ არის ნებადართული", true)
      ?.validateRegex(
        /^[A-Za-z0-9!#$%&'*+\-\/=?^_`{|}~."(),:;<>@[\\\]]+$/,
        "მხოლოდ ინგლისური ასოებია ნებადართული",
      )
      ?.validateRegex(/@/, 'ელ. ფოსტა უნდა შეიცავდეს "@" სიმბოლოს')
      ?.validateLength(5, 50)?.isValid,
    subjectValidator.required()?.validateLength(3, 100),
    textValidator.required(),
  ].every((x) => x);

  contactSubmitBtn.disabled = !isFormValid;
}

contactFields.forEach((field) => {
  field.addEventListener("blur", validateForm);
});

if (contactSubmitBtn) {
  validateForm();
}

const subjectField = document.querySelector(
  '#contact-form input[name="subject"]',
);

if (subjectField) {
  addInitialSubject();
}

function addInitialSubject() {
  const searchParams = new URLSearchParams(window.location.search);
  const initialSubject = searchParams.get("subject");

  if (!initialSubject) return;

  subjectField.value = initialSubject;
}
