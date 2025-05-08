function viewSignificant(bodyDataFormat, tableBody=null) {
    tbodyList = document.querySelectorAll('tbody[id$="-table-body"]')
    if (tableBody) {
        tbodyList = tableBody
    }
    tbodyList.forEach(tbody => {
        tbody.addEventListener('click', async function(event) {
            tbodyId = tbody.id
            bodyData = bodyDataFormat(event.target.dataset)
            jsonData = JSON.stringify(bodyData)
            const modal = new bootstrap.Modal(document.getElementById('significantModal'))
            if (event.target.classList.contains('signifi-btn')) {
                const url = event.target.getAttribute('url');
                const response = await fetch(`${url}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: jsonData
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
}