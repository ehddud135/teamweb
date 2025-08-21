let apiUrl = '/customer/list-api/checklist';
function dataRowFormat(item, item_id) {
    significant_btn = '';
    isOnPremise = item.is_onpremise ? 'O': 'X'
    data = `data-model-id="${item.id}"`;
    if (item.significant) {
        significant_btn += `<td>
                        <button class="btn btn-info signifi-btn" url="/customer/view-significant/checklist"
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
                    <td>${isOnPremise}</td>
                    <td>${new Date(item.uploaded_at).toLocaleDateString()}</td>
                    ${significant_btn}
                    <td>
                        <button class="btn btn-info download-btn" ${data} file-url="/customer/file-fetch/checklist">Download</button>
                    </td>
                    <td>
                        <button class="btn btn-danger delete-btn" ${data} data-delete-url="/customer/delete/checklist/${item.id}">Delete</button>
                    </td>
                </tr>
            `;
    return row;
}


function bodyDataFormat(data) {
    return {
        id: data.modelId
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

