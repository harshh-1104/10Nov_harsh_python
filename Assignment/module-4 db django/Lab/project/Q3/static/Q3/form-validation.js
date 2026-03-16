// Simple client-side form validation for the Q3 form.

const form = document.getElementById('contactForm');
const successMessage = form.querySelector('.success');

const validators = {
  name: (value) => value.trim().length >= 2,
  email: (value) => /\S+@\S+\.\S+/.test(value),
  message: (value) => value.trim().length >= 10,
};

const errorMessages = {
  name: 'Please enter a name (at least 2 characters).',
  email: 'Please enter a valid email address.',
  message: 'Please enter a message (at least 10 characters).',
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
  const inputs = Array.from(form.querySelectorAll('input, textarea'));
  const results = inputs.map((input) => validateField(input));
  return results.every(Boolean);
}

form.addEventListener('submit', (event) => {
  event.preventDefault();

  if (validateForm()) {
    successMessage.textContent = 'Form is valid! (In a real app, this would be submitted.)';
    form.reset();
  } else {
    successMessage.textContent = '';
  }
});

form.addEventListener('input', (event) => {
  if (['name', 'email', 'message'].includes(event.target.name)) {
    validateField(event.target);
  }
});
