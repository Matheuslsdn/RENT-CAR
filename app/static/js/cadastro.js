function validateRegisterForm() {
    let nome = document.getElementById('nome').value;
    let senha = document.getElementById('senha').value;
    let email = document.getElementById('email').value;

    let isValid = true;

    clearErrors();

    if (nome.length < 3) {
        showError('usernameError', 'O nome de usuário deve ter pelo menos 3 caracteres.');
        isValid = false;
    }

    if (senha.length < 6) {
        showError('passwordError', 'A senha deve ter pelo menos 6 caracteres.');
        isValid = false;
    }

    if (!validateEmail(email)) {
        showError('emailError', 'Por favor, insira um email válido.');
        isValid = false;
    }

    return isValid;
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(error => {
        error.style.display = 'none';
    });
}

function showError(elementId, message) {
    let errorElement = document.getElementById(elementId);
    errorElement.innerHTML = message;
    errorElement.style.display = 'block';
}

function validateEmail(email) {
    let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

