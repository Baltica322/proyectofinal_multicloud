document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form.formulario");

    form.addEventListener("submit", (e) => {
        // Limpia mensajes anteriores
        document.querySelectorAll(".error").forEach(el => el.textContent = "");

        // Tomamos los campos
        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const email = document.getElementById("email").value.trim();
        const nombre = document.getElementById("nombre").value.trim();
        const apellido = document.getElementById("apellido").value.trim();

        let tieneError = false;

        if (username.length === 0) {
            mostrarError("username_error", "El nombre de usuario es requerido.");
            tieneError = true;
        }

        if (password.length < 8) {
            mostrarError("password_error", "La contraseña debe tener al menos 8 dígitos.");
            tieneError = true;
        }

        if (email.length === 0) {
            mostrarError("email_error", "El correo electrónico es requerido.");
            tieneError = true;
        } else if (!validateEmail(email)) {
            mostrarError("email_error", "Ingrese un correo electrónico válido.");
            tieneError = true;
        }

        if (nombre.length === 0) {
            mostrarError("nombre_error", "El nombre es requerido.");
            tieneError = true;
        }

        if (apellido.length === 0) {
            mostrarError("apellido_error", "El apellido es requerido.");
            tieneError = true;
        }

        if (tieneError) {
            e.preventDefault();
        }
    });

    function mostrarError(id, mensaje) {
        document.getElementById(id).textContent = mensaje;
    }

    function validateEmail(email) {
        return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
    }
});
