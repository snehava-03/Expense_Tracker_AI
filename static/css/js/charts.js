// charts.js
// Chart.js helper functions used in charts.html
// All chart data is passed from Flask via Jinja2 into the HTML page
// and then this file's functions are called from charts.html

const CHART_COLORS = [
    "#2563eb", "#dc2626", "#059669", "#d97706",
    "#7c3aed", "#0891b2", "#db2777", "#65a30d",
    "#ea580c", "#0284c7", "#84cc16", "#f43f5e"
];

/**
 * Creates a Pie Chart showing expense breakdown by category
 * @param {string} canvasId - ID of the canvas element
 * @param {object} categories - { "Food": 3500, "Petrol": 1200, ... }
 */
function createPieChart(canvasId, categories) {
    const labels = Object.keys(categories);
    const values = Object.values(categories);

    new Chart(document.getElementById(canvasId), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: CHART_COLORS.slice(0, labels.length),
                borderWidth: 2,
                borderColor: "#ffffff"
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { font: { size: 12 }, padding: 16 }
                },
                tooltip: {
                    callbacks: {
                        // Show rupee symbol in tooltip
                        label: function(context) {
                            return " ₹" + context.parsed.toLocaleString("en-IN");
                        }
                    }
                }
            }
        }
    });
}

/**
 * Creates a Bar Chart showing category-wise spending
 * @param {string} canvasId - ID of the canvas element
 * @param {object} categories - { "Food": 3500, "Petrol": 1200, ... }
 */
function createBarChart(canvasId, categories) {
    const labels = Object.keys(categories);
    const values = Object.values(categories);

    new Chart(document.getElementById(canvasId), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Amount (₹)",
                data: values,
                backgroundColor: CHART_COLORS.slice(0, labels.length),
                borderRadius: 6,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        // Show rupee symbol on Y axis
                        callback: function(value) {
                            return "₹" + value.toLocaleString("en-IN");
                        }
                    }
                },
                x: {
                    ticks: { font: { size: 12 } }
                }
            }
        }
    });
}

/**
 * Creates a Line Chart showing income vs expenses over last 6 months
 * @param {string} canvasId - ID of the canvas element
 * @param {Array} monthlyTrend - [{ month: "Jan", income: 40000, expenses: 25000 }, ...]
 */
function createTrendChart(canvasId, monthlyTrend) {
    const labels   = monthlyTrend.map(m => m.month);
    const incomes  = monthlyTrend.map(m => m.income);
    const expenses = monthlyTrend.map(m => m.expenses);

    new Chart(document.getElementById(canvasId), {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Income",
                    data: incomes,
                    borderColor: "#059669",
                    backgroundColor: "rgba(5, 150, 105, 0.1)",
                    borderWidth: 2,
                    pointBackgroundColor: "#059669",
                    pointRadius: 5,
                    tension: 0.3,
                    fill: true
                },
                {
                    label: "Expenses",
                    data: expenses,
                    borderColor: "#dc2626",
                    backgroundColor: "rgba(220, 38, 38, 0.1)",
                    borderWidth: 2,
                    pointBackgroundColor: "#dc2626",
                    pointRadius: 5,
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            interaction: {
                mode: "index",
                intersect: false
            },
            plugins: {
                legend: {
                    position: "top",
                    labels: { font: { size: 13 } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return " " + context.dataset.label +
                                   ": ₹" + context.parsed.y.toLocaleString("en-IN");
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return "₹" + value.toLocaleString("en-IN");
                        }
                    }
                }
            }
        }
    });
}