let apiUrl = '/customer/record-list-api';
function dataRowFormat(item, item_id) {
    significant_btn = '';
    data = `data-installation-date="${item.installation_date}" data-customer-name="${item.customer}"`;
    if (item.significant) {
        significant_btn += `<td>
                        <button class="btn btn-info signifi-btn" url="/customer/view-significant"
                        ${data}>View</button>
                    </td>`;
    }
    else {
        significant_btn += `<td></td>`;
    }
    row =   `
                <tr>
                    <td>${item_id}</td>
                    <td>${item.customer}</td>
                    <td>${item.manager}</td>
                    <td>${new Date(item.installation_date).toLocaleDateString()}</td>
                    ${significant_btn}
                    <td>
                        <button class="btn btn-info pdf-view-btn" ${data} pdf-view-url="/customer/installation-cert/view">View</button>
                        <button class="btn btn-info download-btn" ${data} pdf-download-url="/customer/installation-cert/download">Download</button>
                    </td>
                </tr>
            `;
    return row;
}


function bodyDataFormat(data) {
    return {
        installation_date: data.installationDate,
        customer_name: data.customerName,
    }
}

// 페이지 로드 시 데이터 가져오기
document.addEventListener('DOMContentLoaded', async () => {
    tbody = document.querySelectorAll('tbody[id="table-body"]')
    fetchAndRenderData(apiUrl, dataRowFormat);
    viewSignificant(bodyDataFormat, tbody);
    const modalElement = document.getElementById('append-modal-form');

    modalElement.addEventListener('hidden.bs.modal', ()=> {
        fetchAndRenderData(apiUrl, dataRowFormat);
        viewSignificant(bodyDataFormat, tbody);
    })

})

