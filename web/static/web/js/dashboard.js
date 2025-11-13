
document.addEventListener('DOMContentLoaded', function () {
    const data = window.DASHBOARD_DATA || {
        catLabels: [],
        catCounts: [],
        monthLabels: [],
        monthCounts: [],
    };

    // ====== COLORES BASE ======
    const mainColor = '#b13860';
    const softColor = '#f9e0ea';

    // ====== GRÁFICO 1: PRÉSTAMOS POR MES ======
    const monthCanvas = document.getElementById('loansByMonth');
    if (monthCanvas) {
        const ctx1 = monthCanvas.getContext('2d');
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: data.monthLabels,
                datasets: [{
                    label: 'Préstamos',
                    data: data.monthCounts,
                    backgroundColor: softColor,
                    borderColor: mainColor,
                    borderWidth: 2,
                    borderRadius: 8,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,   // dejamos que el alto fijo del canvas mande
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#fff',
                        titleColor: '#333',
                        bodyColor: '#333',
                        borderColor: mainColor,
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#555' }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f2d8e3' },
                        ticks: { color: '#555', precision: 0 }
                    }
                }
            }
        });
    }

    // ====== GRÁFICO 2: LIBROS POR CATEGORÍA ======
    const catCanvas = document.getElementById('booksByCategory');
    if (catCanvas) {
        const ctx2 = catCanvas.getContext('2d');
        new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: data.catLabels,
                datasets: [{
                    label: 'Libros',
                    data: data.catCounts,
                    backgroundColor: softColor,
                    borderColor: mainColor,
                    borderWidth: 2,
                    borderRadius: 8,
                }]
            },
            options: {
                indexAxis: 'y',  // barras horizontales
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#fff',
                        titleColor: '#333',
                        bodyColor: '#333',
                        borderColor: mainColor,
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: { color: '#f2d8e3' },
                        ticks: { color: '#555', precision: 0 }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#555' }
                    }
                }
            }
        });
    }
});