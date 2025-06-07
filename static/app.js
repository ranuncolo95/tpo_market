// Initialize chart
const ctx = document.getElementById('stockChart').getContext('2d');
const stockChart = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [] },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: { y: { beginAtZero: false } }
    }
});

// Set default dates (last 30 days)
function setDefaultDates() {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setMonth(endDate.getMonth() - 1);
    
    document.getElementById('startDate').valueAsDate = startDate;
    document.getElementById('endDate').valueAsDate = endDate;
}

// Fetch data from API
async function fetchData() {
    const ticker = document.getElementById('ticker').value.trim();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;

    if (!ticker || !startDate || !endDate) {
        alert('Please enter all fields');
        return;
    }

    try {
        const response = await fetch('/api/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                ticker: ticker,
                start_date: startDate,
                end_date: endDate
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to fetch data');
        }

        const data = await response.json();
        stockChart.data.labels = data.labels;
        stockChart.data.datasets = data.datasets;
        stockChart.update();

    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', setDefaultDates);
document.getElementById('fetchData').addEventListener('click', fetchData);