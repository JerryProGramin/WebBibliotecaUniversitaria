// web/static/web/js/categories.js

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
const catApiUrl = "/api/categories/";

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("categories-tbody");
    const globalError = document.getElementById("cat-global-error");

    const modal = document.getElementById("category-modal");
    const form = document.getElementById("category-form");
    const modalTitle = document.getElementById("cat-modal-title");
    const formError = document.getElementById("cat-form-error");

    const inpId = document.getElementById("category-id");
    const inpNombre = document.getElementById("inp-cat-nombre");

    const btnAdd = document.getElementById("btn-add-category");
    const btnCancel = document.getElementById("btn-cat-cancel");

    function openModal(cat = null) {
        formError.style.display = "none";
        form.reset();

        if (cat) {
            modalTitle.textContent = "Editar categoría";
            inpId.value = cat.id;
            inpNombre.value = cat.nombre;
        } else {
            modalTitle.textContent = "Nueva categoría";
            inpId.value = "";
        }

        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
    }

    async function loadCategories() {
        globalError.style.display = "none";
        tbody.innerHTML = "";

        try {
            const res = await fetch(catApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });

            if (!res.ok) {
                let msg = "Error al cargar categorías";
                try {
                    const d = await res.json();
                    if (d.detail) msg += ": " + d.detail;
                } catch (_) { }
                throw new Error(msg);
            }

            const data = await res.json();
            data.forEach(cat => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${cat.nombre}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-sm btn-edit" data-id="${cat.id}">Editar</button>
                            <button class="btn-sm btn-delete" data-id="${cat.id}">Eliminar</button>
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
            const res = await fetch(catApiUrl + id + "/", {
                method: "GET",
                credentials: "same-origin",
            });
            const cat = await res.json();
            openModal(cat);
        }

        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Eliminar categoría?")) return;

            await fetch(catApiUrl + id + "/", {
                method: "DELETE",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            });

            loadCategories();
        }
    });

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";

        const payload = {
            nombre: inpNombre.value.trim(),
        };

        const id = inpId.value;
        const url = id ? catApiUrl + id + "/" : catApiUrl;
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
            loadCategories();
        } catch (err) {
            formError.textContent = "Error al guardar categoría.";
            formError.style.display = "block";
        }
    });

    loadCategories();
});
