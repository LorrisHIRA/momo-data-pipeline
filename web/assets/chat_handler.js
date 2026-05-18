const DASHBOARD_JSON = './data/processed/dashboard.json';

async function loadDashboardData() {
    try {
        const response = await fetch(DASHBOARD_JSON);
        if (!response.ok) {
            throw new Error('Failed to load dashboard data');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        return null;
    }
}

function updateSummaryCards(data) {
    document.getElementById('stat-total').textContent = data.total_transactions;

    const totalAmount = data.total_amount_rwf.toLocaleString();
    document.getElementById('stat-amount').textContent = totalAmount + ' RWF';

    const categories = data.by_category;
    const topCategory = Object.entries(categories).sort((a, b) => b[1].count - a[1].count)[0];
    document.getElementById('stat-category').textContent = topCategory[0];
}

function renderCategoryChart(data) {
    const ctx = document.getElementById('categoryChart').getContext('2d');
    const categories = data.by_category;

    const labels = Object.keys(categories);
    const counts = labels.map(label => categories[label].count);
    const colors = ['#FFCC00', '#FF6384', '#36A2EB', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'];

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: counts,
                backgroundColor: colors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function renderTimelineChart(data) {
    const ctx = document.getElementById('timelineChart').getContext('2d');
    const months = data.by_month || [];

    const labels = months.map(m => m.month);
    const counts = months.map(m => m.count);

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Transactions',
                data: counts,
                borderColor: '#FFCC00',
                backgroundColor: 'rgba(255, 204, 0, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function renderTransactionsTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    const transactions = data.recent_transactions || [];

    for (const tx of transactions) {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tx.date || 'N/A'}</td>
            <td>${tx.amount ? tx.amount.toLocaleString() : 'N/A'}</td>
            <td>${tx.category || 'N/A'}</td>
            <td>${tx.phone || 'N/A'}</td>
        `;
        tbody.appendChild(row);
    }

    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No transactions found. Run the ETL pipeline first.</td></tr>';
    }
}

async function initDashboard() {
    const data = await loadDashboardData();
    if (!data) {
        document.getElementById('table-body').innerHTML = '<tr><td colspan="4">Failed to load data. Run the ETL pipeline first.</td></tr>';
        return;
    }
    updateSummaryCards(data);
    renderCategoryChart(data);
    renderTimelineChart(data);
    renderTransactionsTable(data);
}

document.addEventListener('DOMContentLoaded', initDashboard);