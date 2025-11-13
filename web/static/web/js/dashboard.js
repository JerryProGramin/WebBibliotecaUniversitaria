// web/static/web/js/dashboard.js

document.addEventListener("DOMContentLoaded", () => {
    const data = window.DASHBOARD_DATA || {
        catLabels: [],
        catCounts: [],
        monthLabels: [],
        monthCounts: [],
    };

    // --- GRÁFICO 1: Préstamos por mes (línea / barras) ---
    const loansCanvas = document.getElementById("loansByMonthChart");
    if (loansCanvas) {
        const ctx1 = loansCanvas.getContext("2d");
        new Chart(ctx1, {
            type: "bar",
            data: {
                labels: data.monthLabels,
                datasets: [
                    {
                        label: "Préstamos",
                        data: data.monthCounts,
                        backgroundColor: "rgba(123, 17, 56, 0.25)",
                        borderColor: "rgba(123, 17, 56, 1)",
                        borderWidth: 2,
                        borderRadius: 8,
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: { color: "#555" },
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 1, color: "#555" },
                    },
                },
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        enabled: true,
                    },
                },
            },
        });
    }

    // --- GRÁFICO 2: Libros por categoría (doughnut) ---
    const booksCanvas = document.getElementById("booksByCategoryChart");
    if (booksCanvas) {
        const ctx2 = booksCanvas.getContext("2d");
        const baseColors = [
            "#c14667",
            "#7b1138",
            "#f3a3b8",
            "#ffcc80",
            "#81c784",
            "#64b5f6",
            "#ba68c8",
        ];

        const bgColors = data.catLabels.map((_, i) => {
            return baseColors[i % baseColors.length];
        });

        new Chart(ctx2, {
            type: "doughnut",
            data: {
                labels: data.catLabels,
                datasets: [
                    {
                        data: data.catCounts,
                        backgroundColor: bgColors,
                        borderWidth: 1,
                        borderColor: "#ffffff",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            boxWidth: 12,
                        },
                    },
                },
            },
        });
    }
});
