// web/static/web/js/books.js

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

const booksApiUrl = "/api/books/";
const authorsApiUrl = "/api/authors/";
const categoriesApiUrl = "/api/categories/";

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("books-tbody");
    const globalError = document.getElementById("books-global-error");

    const modal = document.getElementById("book-modal");
    const form = document.getElementById("book-form");
    const modalTitle = document.getElementById("book-modal-title");
    const formError = document.getElementById("book-form-error");

    const inpId = document.getElementById("book-id");
    const inpTitulo = document.getElementById("inp-book-titulo");
    const inpAutor = document.getElementById("inp-book-autor");
    const inpAnio = document.getElementById("inp-book-anio");
    const inpCategories = document.getElementById("inp-book-categories");

    const btnAdd = document.getElementById("btn-add-book");
    const btnCancel = document.getElementById("btn-book-cancel");

    let authorsCache = [];
    let categoriesCache = [];

    // ------- helpers UI -------
    function openModal(book = null) {
        formError.style.display = "none";
        form.reset();

        // limpiar selección múltiple
        Array.from(inpCategories.options).forEach(opt => opt.selected = false);

        if (book) {
            modalTitle.textContent = "Editar libro";
            inpId.value = book.id;
            inpTitulo.value = book.titulo;
            inpAutor.value = book.autor || "";
            inpAnio.value = book.anio_publicacion || "";

            // category es una lista de IDs
            if (Array.isArray(book.category)) {
                const ids = book.category.map(String);
                Array.from(inpCategories.options).forEach(opt => {
                    if (ids.includes(opt.value)) {
                        opt.selected = true;
                    }
                });
            }
        } else {
            modalTitle.textContent = "Nuevo libro";
            inpId.value = "";
        }

        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
    }

    // ------- cargar listas (autores/categorías) -------
    async function loadAuthorsAndCategories() {
        // autores
        try {
            const resA = await fetch(authorsApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });
            if (resA.ok) {
                authorsCache = await resA.json();
                inpAutor.innerHTML = '<option value="">-- Selecciona autor --</option>';
                authorsCache.forEach(a => {
                    const opt = document.createElement("option");
                    opt.value = a.id;
                    opt.textContent = a.nombre;
                    inpAutor.appendChild(opt);
                });
            }
        } catch (_) { }

        // categorías
        try {
            const resC = await fetch(categoriesApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });
            if (resC.ok) {
                categoriesCache = await resC.json();
                inpCategories.innerHTML = "";
                categoriesCache.forEach(c => {
                    const opt = document.createElement("option");
                    opt.value = c.id;
                    opt.textContent = c.nombre;
                    inpCategories.appendChild(opt);
                });
            }
        } catch (_) { }
    }

    // ------- listar libros -------
    async function loadBooks() {
        globalError.style.display = "none";
        tbody.innerHTML = "";

        try {
            const res = await fetch(booksApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });

            if (!res.ok) {
                let msg = "Error al cargar libros";
                try {
                    const d = await res.json();
                    if (d.detail) msg += ": " + d.detail;
                } catch (_) { }
                throw new Error(msg);
            }

            const data = await res.json();

            data.forEach(book => {
                const tr = document.createElement("tr");
                const categoriasTexto = (book.categorias_nombres || []).join(", ");

                tr.innerHTML = `
                    <td>${book.titulo}</td>
                    <td>${book.autor_nombre || ""}</td>
                    <td>${book.anio_publicacion || ""}</td>
                    <td>${categoriasTexto}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-sm btn-edit" data-id="${book.id}">Editar</button>
                            <button class="btn-sm btn-delete" data-id="${book.id}">Eliminar</button>
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

    // ------- eventos -------
    btnAdd?.addEventListener("click", () => openModal());
    btnCancel?.addEventListener("click", () => closeModal());

    // editar / eliminar
    tbody.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (!id) return;

        // editar
        if (e.target.classList.contains("btn-edit")) {
            try {
                const res = await fetch(booksApiUrl + id + "/", {
                    method: "GET",
                    credentials: "same-origin",
                });
                if (!res.ok) return;
                const book = await res.json();
                openModal(book);
            } catch (_) { }
        }

        // eliminar
        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Eliminar libro?")) return;

            try {
                const res = await fetch(booksApiUrl + id + "/", {
                    method: "DELETE",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": csrftoken,
                    },
                });
                if (!res.ok) {
                    alert("Error al eliminar libro");
                } else {
                    loadBooks();
                }
            } catch (_) {
                alert("Error al eliminar libro");
            }
        }
    });

    // submit form
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";

        const selectedCategories = Array.from(inpCategories.options)
            .filter(opt => opt.selected)
            .map(opt => Number(opt.value));

        const payload = {
            titulo: inpTitulo.value.trim(),
            autor: inpAutor.value ? Number(inpAutor.value) : null,
            anio_publicacion: inpAnio.value ? Number(inpAnio.value) : null,
            category: selectedCategories,
        };

        const id = inpId.value;
        const url = id ? booksApiUrl + id + "/" : booksApiUrl;
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
                let msg = "Error al guardar libro";
                try {
                    const data = await res.json();
                    msg = JSON.stringify(data);
                } catch (_) { }
                formError.textContent = msg;
                formError.style.display = "block";
                return;
            }

            closeModal();
            loadBooks();
        } catch (err) {
            formError.textContent = "Error al guardar libro.";
            formError.style.display = "block";
        }
    });

    // ------- init -------
    loadAuthorsAndCategories().then(loadBooks);
});
