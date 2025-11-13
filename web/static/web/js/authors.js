// web/static/web/js/authors.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");
const authApiUrl = "/api/authors/";

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("authors-tbody");
    const globalError = document.getElementById("auth-global-error");

    const modal = document.getElementById("author-modal");
    const form = document.getElementById("author-form");
    const modalTitle = document.getElementById("auth-modal-title");
    const formError = document.getElementById("auth-form-error");

    const inpId = document.getElementById("author-id");
    const inpNombre = document.getElementById("inp-auth-nombre");

    const btnAdd = document.getElementById("btn-add-author");
    const btnCancel = document.getElementById("btn-auth-cancel");

    function openModal(author = null) {
        formError.style.display = "none";
        form.reset();

        if (author) {
            modalTitle.textContent = "Editar autor";
            inpId.value = author.id;
            inpNombre.value = author.nombre;
        } else {
            modalTitle.textContent = "Nuevo autor";
            inpId.value = "";
        }

        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
    }

    async function loadAuthors() {
        globalError.style.display = "none";
        tbody.innerHTML = "";

        try {
            const res = await fetch(authApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });

            if (!res.ok) {
                let msg = "Error al cargar autores";
                try {
                    const d = await res.json();
                    if (d.detail) msg += ": " + d.detail;
                } catch (_) { }
                throw new Error(msg);
            }

            const data = await res.json();
            data.forEach(a => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${a.nombre}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-sm btn-edit" data-id="${a.id}">Editar</button>
                            <button class="btn-sm btn-delete" data-id="${a.id}">Eliminar</button>
                        </div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        } catch (err) {
            globalError.textContent = err.message;
            globalError.style.display = "block";
        }
    }

    btnAdd?.addEventListener("click", () => openModal());
    btnCancel?.addEventListener("click", () => closeModal());

    tbody.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (!id) return;

        if (e.target.classList.contains("btn-edit")) {
            const res = await fetch(authApiUrl + id + "/", {
                method: "GET",
                credentials: "same-origin",
            });
            const a = await res.json();
            openModal(a);
        }

        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Eliminar autor?")) return;

            await fetch(authApiUrl + id + "/", {
                method: "DELETE",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            });

            loadAuthors();
        }
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";

        const payload = {
            nombre: inpNombre.value.trim(),
        };

        const id = inpId.value;
        const url = id ? authApiUrl + id + "/" : authApiUrl;
        const method = id ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method,
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrftoken,
                },
                body: JSON.stringify(payload),
            });

            if (!res.ok) {
                const data = await res.json();
                formError.textContent = JSON.stringify(data);
                formError.style.display = "block";
                return;
            }

            closeModal();
            loadAuthors();
        } catch (err) {
            formError.textContent = "Error al guardar autor.";
            formError.style.display = "block";
        }
    });

    loadAuthors();
});
