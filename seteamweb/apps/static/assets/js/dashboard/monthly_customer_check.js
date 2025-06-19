document.addEventListener('DOMContentLoaded', async function() {
    data = await monthlyCustomer();
    new Chart(
        document.getElementById('monthlyCustomersChart'),
        {
            type: 'line',
            data: {
                labels: Object.keys(data),
                datasets: [{
                    data: Object.values(data),
                    fill: true,
                    tension: 0.4,
                    borderColor: 'rgba(219, 151, 23, 0.2)',
                    backgroundColor: 'rgba(40, 65, 134, 0.2)',
                    pointRadius: 4,
                    pointBackgroundColor: 'rgba(240, 187, 88, 0.59)',
                }]
            },
            options: {
                responsive: true, 
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {display: false },
                        ticks: {display: false }
                    },
                    x: {
                        grid: { display: true, borderDash: [10, 50]},
                        ticks: {color: '#666'},
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    datalabels:{
                        anchor: 'end',
                        align: 'start',
                        offset: -20,
                        font:{
                            size : 13,
                            weight: 'bold'
                        },
                        formatter: value => value
                    }
                }
            },
            plugins:[ChartDataLabels]
        }
    )
});

async function monthlyCustomer() {
    url = 'dashboard/monthly-customer-count';
    let data = {};
    const response = await fetch(url)
    if (response.ok) {
        data = await response.json();
        return data;
    }
    else {
        console.error('Error fetching monthly customer data:', response.status_code);
        return {};
    }
}