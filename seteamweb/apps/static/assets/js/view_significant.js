document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('table-body-by-customer').addEventListener('click', async function(event) {
        const modal = new bootstrap.Modal(document.getElementById('significantModal'))
        if (event.target.classList.contains('signifi-btn')) {
            console.log(event.target.dataset);
            const url = event.target.getAttribute('url');
            console.log(url);

            const response = await fetch(`${url}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    package_name: event.target.dataset.packageName,
                    inspection_date: event.target.dataset.inspectionDate,
                    customer_name: event.target.dataset.customerName,
                    platform: event.target.dataset.platform
                })
            });

            const data = await response.json();
            if (response.ok) {
                document.getElementById('significantContent').innerText = data.significant;
                modal.show();
            } else {
                alert(`Error: ${data.error}`);
            }
        }
    });
});