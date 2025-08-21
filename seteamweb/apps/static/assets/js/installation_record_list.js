let apiUrl = '/customer/list-api/record';
function dataRowFormat(item, item_id) {
    significant_btn = '';
    data = `data-model-id="${item.id}"`;
    if (item.significant) {
        significant_btn += `<td>
                        <button class="btn btn-info signifi-btn" url="/customer/view-significant/installation-record"
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
                        <button class="btn btn-info pdf-view-btn" ${data} file-url="/customer/file-fetch/installation-cert">View</button>
                        <button class="btn btn-info download-btn" ${data} file-url="/customer/file-fetch/installation-cert">Download</button>
                    </td>
                    <td>
                        <button class="btn btn-danger delete-btn" ${data} file-url="/customer/delete/installation-record/${item.id}">Delete</button>
                    </td>
                </tr>
            `;
    return row;
}


function bodyDataFormat(data) {
    return {
        id: data.modelId,
    }
}

const searchList = ['customer', 'manager']

// 페이지 로드 시 데이터 가져오기
document.addEventListener('DOMContentLoaded', async () => {
    tbody = document.querySelectorAll('tbody[id="table-body"]')
    fetchAndRenderData(apiUrl, dataRowFormat, searchList);
    viewSignificant(bodyDataFormat, tbody);
    pdfViewOrDownload(bodyDataFormat, tbody);
    const modalElement = document.getElementById('append-modal-form');

    modalElement.addEventListener('hidden.bs.modal', ()=> {
        fetchAndRenderData(apiUrl, dataRowFormat, searchList);
        viewSignificant(bodyDataFormat, tbody);
        pdfViewOrDownload(bodyDataFormat, tbody);
    })

})

