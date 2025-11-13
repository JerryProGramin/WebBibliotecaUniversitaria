document.addEventListener("DOMContentLoaded", function () {
    const showRegister = document.getElementById("show-register");
    const backToLogin = document.getElementById("back-to-login");
    const loginBlock = document.getElementById("login-form-block");
    const registerBlock = document.getElementById("register-form-block");
    const heroImg = document.getElementById("hero-img");
    const cardTitle = document.getElementById("card-title");
    const toggleText = document.getElementById("toggle-text");

    // rutas que vienen del HTML (las puso Django)
    const loginImg = heroImg.dataset.loginImg;
    const registerImg = heroImg.dataset.registerImg;

    if (showRegister) {
        showRegister.addEventListener("click", function (e) {
            e.preventDefault();

            // mostrar registro, ocultar login
            loginBlock.classList.add("hidden");
            registerBlock.classList.remove("hidden");

            // cambiar título e imagen
            cardTitle.textContent = "Registrar";
            heroImg.src = registerImg;

            // cambiar texto de abajo
            toggleText.innerHTML =
                '¿Ya tienes una cuenta? <a href="#" id="back-inline">Inicia sesión</a>';

            // botón de volver desde el texto de abajo
            const backInline = document.getElementById("back-inline");
            backInline.addEventListener("click", function (e2) {
                e2.preventDefault();
                if (backToLogin) backToLogin.click();
            });
        });
    }

    if (backToLogin) {
        backToLogin.addEventListener("click", function () {
            // mostrar login, ocultar registro
            registerBlock.classList.add("hidden");
            loginBlock.classList.remove("hidden");

            // volver a título e imagen
            cardTitle.textContent = "Iniciar sesión";
            heroImg.src = loginImg;

            // volver a poner el link de registrar
            toggleText.innerHTML =
                'No tengo una cuenta. <a href="#" id="show-register">Registrar</a>';

            // hay que volver a enganchar el click porque lo reescribimos
            const newShowRegister = document.getElementById("show-register");
            if (newShowRegister) {
                newShowRegister.addEventListener("click", function (e3) {
                    e3.preventDefault();
                    if (showRegister) showRegister.click();
                });
            }
        });
    }
});
