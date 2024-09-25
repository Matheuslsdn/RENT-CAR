// script.js
function validateForm() {
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let emailError = document.getElementById('emailError');
    let passwordError = document.getElementById('passwordError');
    let isValid = true;

    // Limpa as mensagens de erro
    emailError.style.display = 'none';
    passwordError.style.display = 'none';

    // Validação de email
    if (!validateEmail(email)) {
        emailError.innerHTML = "Por favor, insira um email válido.";
        emailError.style.display = 'block';
        isValid = false;
    }

    // Validação de senha
    if (password.length < 6) {
        passwordError.innerHTML = "A senha deve ter pelo menos 6 caracteres.";
        passwordError.style.display = 'block';
        isValid = false;
    }

    return isValid; // Retorna true se o formulário for válido
}

function validateEmail(email) {
    let regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Adiciona efeito de foco nos campos de input
document.querySelectorAll('.input-group input').forEach(input => {
    input.addEventListener('focus', () => {
        input.style.borderColor = '#4CAF50';
    });
    input.addEventListener('blur', () => {
        input.style.borderColor = '#ccc';
    });
});
