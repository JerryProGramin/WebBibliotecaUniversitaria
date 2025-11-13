// web/static/web/js/loans.js

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

const loansApiUrl = "/api/loans/";
const studentsApiUrl = "/api/students/";
const bookDetailsApiUrl = "/api/book-details/";

document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.getElementById("loans-tbody");
    const globalError = document.getElementById("loans-global-error");

    const modal = document.getElementById("loan-modal");
    const form = document.getElementById("loan-form");
    const modalTitle = document.getElementById("loan-modal-title");
    const formError = document.getElementById("loan-form-error");

    const inpId = document.getElementById("loan-id");
    const inpStudent = document.getElementById("inp-loan-student");
    const inpBookDetail = document.getElementById("inp-loan-bookdetail");
    const inpStart = document.getElementById("inp-loan-start");
    const inpEnd = document.getElementById("inp-loan-end");
    const inpComments = document.getElementById("inp-loan-comments");

    const btnAdd = document.getElementById("btn-add-loan");
    const btnCancel = document.getElementById("btn-loan-cancel");

    let studentsCache = [];
    let bookDetailsCache = [];

    // -------- helpers UI ----------
    function openModal(loan = null) {
        formError.style.display = "none";
        form.reset();
        inpId.value = "";

        if (loan) {
            modalTitle.textContent = "Editar préstamo";
            inpId.value = loan.id;
            inpStudent.value = loan.estudiante;
            inpBookDetail.value = loan.libro;
            inpStart.value = loan.fecha_inicio;
            inpEnd.value = loan.fecha_fin;
            inpComments.value = loan.comentarios || "";
        } else {
            modalTitle.textContent = "Nuevo préstamo";

            // setear fecha inicio = hoy
            const today = new Date().toISOString().slice(0, 10);
            inpStart.value = today;
        }

        modal.classList.add("show");
    }

    function closeModal() {
        modal.classList.remove("show");
    }

    // -------- cargar combos ----------
    async function loadStudents() {
        try {
            const res = await fetch(studentsApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });
            if (!res.ok) return;
            studentsCache = await res.json();
            inpStudent.innerHTML = '<option value="">-- Selecciona estudiante --</option>';
            studentsCache.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s.id;
                opt.textContent = `${s.nombres} ${s.apellidos} (${s.dni})`;
                inpStudent.appendChild(opt);
            });
        } catch (_) { }
    }

    async function loadBookDetails() {
        try {
            const res = await fetch(bookDetailsApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });
            if (!res.ok) return;
            bookDetailsCache = await res.json();
            inpBookDetail.innerHTML = '<option value="">-- Selecciona ejemplar disponible --</option>';

            // solo ejemplares no prestados
            bookDetailsCache
                .filter(bd => !bd.estado_prestamo)
                .forEach(bd => {
                    const opt = document.createElement("option");
                    opt.value = bd.id;
                    opt.textContent = `${bd.libro_titulo} - ${bd.codigo_isbn}`;
                    inpBookDetail.appendChild(opt);
                });
        } catch (_) { }
    }

    // -------- listar préstamos ----------
    async function loadLoans() {
        globalError.style.display = "none";
        tbody.innerHTML = "";

        try {
            const res = await fetch(loansApiUrl, {
                method: "GET",
                credentials: "same-origin",
            });

            if (!res.ok) {
                let msg = "Error al cargar préstamos";
                try {
                    const d = await res.json();
                    if (d.detail) msg += ": " + d.detail;
                } catch (_) { }
                throw new Error(msg);
            }

            const data = await res.json();

            data.forEach(loan => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${loan.estudiante_nombre || ""}</td>
                    <td>${loan.libro_titulo || ""}</td>
                    <td>${loan.libro_codigo || ""}</td>
                    <td>${loan.fecha_inicio || ""}</td>
                    <td>${loan.fecha_fin || ""}</td>
                    <td>${loan.comentarios || ""}</td>
                    <td>
                        <div class="actions">
                            <button class="btn-sm btn-delete" data-id="${loan.id}">Finalizar / Eliminar</button>
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

    // -------- eventos ----------
    btnAdd?.addEventListener("click", () => openModal());
    btnCancel?.addEventListener("click", () => closeModal());

    // eliminar (finalizar préstamo)
    tbody.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (!id) return;

        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Finalizar (eliminar) este préstamo?")) return;

            try {
                const res = await fetch(loansApiUrl + id + "/", {
                    method: "DELETE",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": csrftoken,
                    },
                });
                if (!res.ok) {
                    alert("Error al eliminar préstamo");
                } else {
                    loadBookDetails(); // vuelve a haber ejemplar disponible
                    loadLoans();
                }
            } catch (_) {
                alert("Error al eliminar préstamo");
            }
        }
    });

    // submit form (crear / editar)
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        formError.style.display = "none";

        const payload = {
            estudiante: inpStudent.value ? Number(inpStudent.value) : null,
            libro: inpBookDetail.value ? Number(inpBookDetail.value) : null,
            fecha_inicio: inpStart.value,
            fecha_fin: inpEnd.value,
            comentarios: inpComments.value.trim(),
        };

        const id = inpId.value;
        const url = id ? loansApiUrl + id + "/" : loansApiUrl;
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
                let msg = "Error al guardar préstamo";
                try {
                    const data = await res.json();
                    msg = JSON.stringify(data);
                } catch (_) { }
                formError.textContent = msg;
                formError.style.display = "block";
                return;
            }

            closeModal();
            loadBookDetails();
            loadLoans();
        } catch (err) {
            formError.textContent = "Error al guardar préstamo.";
            formError.style.display = "block";
        }
    });

    // -------- init ----------
    Promise.all([loadStudents(), loadBookDetails()]).then(loadLoans);
});
