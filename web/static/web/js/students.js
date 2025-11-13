// web/static/web/js/students.js

// Sacar CSRF desde la cookie (recomendado por Django)
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
const apiUrl = "/api/students/";

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("students-tbody");
    const globalError = document.getElementById("global-error");

    const modal = document.getElementById("student-modal");
    const form = document.getElementById("student-form");
    const modalTitle = document.getElementById("modal-title");
    const formError = document.getElementById("form-error");

    const inpId = document.getElementById("student-id");
    const inpNombres = document.getElementById("inp-nombres");
    const inpApellidos = document.getElementById("inp-apellidos");
    const inpDni = document.getElementById("inp-dni");

    const btnAdd = document.getElementById("btn-add-student");
    const btnCancel = document.getElementById("btn-cancel");

    function openModal(student = null) {
        formError.style.display = "none";
        form.reset();

        if (student) {
            modalTitle.textContent = "Editar estudiante";
            inpId.value = student.id;
            inpNombres.value = student.nombres;
            inpApellidos.value = student.apellidos;
            inpDni.value = student.dni;
        } else {
            modalTitle.textContent = "Nuevo estudiante";
            inpId.value = "";
        }

        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
    }

    // Cargar lista
    async function loadStudents() {
        globalError.style.display = "none";
        tbody.innerHTML = "";

        try {
            const res = await fetch(apiUrl, {
                method: "GET",
                credentials: "same-origin",        // 🔹 manda cookies
            });

            if (!res.ok) {
                let msg = "Error al cargar estudiantes";
                try {
                    const data = await res.json();
                    if (data.detail) msg += ": " + data.detail;
                } catch (_) { }
                throw new Error(msg);
            }

            const data = await res.json();

            data.forEach(st => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${st.nombres}</td>
                    <td>${st.apellidos}</td>
                    <td>${st.dni}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-sm btn-edit" data-id="${st.id}">Editar</button>
                            <button class="btn-sm btn-delete" data-id="${st.id}">Eliminar</button>
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

    // Clicks en la tabla
    tbody.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (!id) return;

        // Editar
        if (e.target.classList.contains("btn-edit")) {
            const res = await fetch(apiUrl + id + "/", {
                method: "GET",
                credentials: "same-origin",    // 🔹
            });
            const st = await res.json();
            openModal(st);
        }

        // Eliminar
        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Eliminar estudiante?")) return;

            await fetch(apiUrl + id + "/", {
                method: "DELETE",
                credentials: "same-origin",    // 🔹
                headers: {
                    "X-CSRFToken": csrftoken,
                },
            });

            loadStudents();
        }
    });

    // Crear / actualizar
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";

        const payload = {
            nombres: inpNombres.value.trim(),
            apellidos: inpApellidos.value.trim(),
            dni: inpDni.value.trim(),
        };

        const id = inpId.value;
        const url = id ? apiUrl + id + "/" : apiUrl;
        const method = id ? "PUT" : "POST";

        try {
            const res = await fetch(url, {
                method,
                credentials: "same-origin",    // 🔹 MUY IMPORTANTE
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
            loadStudents();
        } catch (err) {
            formError.textContent = "Error al guardar estudiante.";
            formError.style.display = "block";
        }
    });

    loadStudents();
});
