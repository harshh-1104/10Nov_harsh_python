// JavaScript form validation for user registration.

const form = document.getElementById('registrationForm');

const validators = {
  username: (value) => value.trim().length >= 3,
  email: (value) => /\S+@\S+\.\S+/.test(value),
  password: (value) => value.length >= 6,
  confirm_password: (value) => {
    const password = document.getElementById('id_password').value;
    return value === password;
  },
};

const errorMessages = {
  username: 'Username must be at least 3 characters.',
  email: 'Please enter a valid email address.',
  password: 'Password must be at least 6 characters.',
  confirm_password: 'Passwords do not match.',
};

function setFieldError(input, message) {
  const errorEl = input.closest('.field').querySelector('.error');
  if (!errorEl) return;
  if (message) {
    errorEl.textContent = message;
    input.classList.add('invalid');
  } else {
    errorEl.textContent = '';
    input.classList.remove('invalid');
  }
}

function validateField(input) {
  const name = input.name;
  const value = input.value;
  const isValid = validators[name]?.(value);

  setFieldError(input, isValid ? '' : errorMessages[name]);
  return Boolean(isValid);
}

function validateForm() {
  const inputs = Array.from(form.querySelectorAll('input'));
  const results = inputs.map((input) => validateField(input));
  return results.every(Boolean);
}

form.addEventListener('submit', (event) => {
  if (!validateForm()) {
    event.preventDefault();
  }
});

form.addEventListener('input', (event) => {
  if (['username', 'email', 'password', 'confirm_password'].includes(event.target.name)) {
    validateField(event.target);
  }
});
