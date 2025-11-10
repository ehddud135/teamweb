let apiUrl = '/automation/list-api';
function dataRowFormat(item, item_id) {
    const asOX = (value) => value ? 'O' : 'X';
    data = `data-model-id="${item.id}"`;
    row =   `
                <tr>
                    <td>${item.app_name}</td>
                    <td>${item.app_version}</td>
                    <td>${asOX(item.rooting)}</td>
                    <td>${asOX(item.integrity)}</td>
                    <td>${asOX(item.emulator)}</td>
                    <td>${asOX(item.decompile)}</td>
                    <td>${item.obfuscate}</td>
                    <td>${item.momo_size}</td>
                    <td>
                        <button class="btn btn-success upload-btn" ${data} data-upload-url="/automation/upload/${item.id}">Upload</button>
                        <button class="btn btn-danger delete-btn" ${data} data-delete-url="/automation/delete/${item.id}">Delete</button>
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

const searchList = ['app_name']

// 페이지 로드 시 데이터 가져오기
document.addEventListener('DOMContentLoaded', async () => {
    tbody = document.querySelectorAll('tbody[id="table-body"]')
    fetchAndRenderData(apiUrl, dataRowFormat, searchList);
    const modalElement = document.getElementById('append-modal-form');

    modalElement.addEventListener('hidden.bs.modal', ()=> {
        fetchAndRenderData(apiUrl, dataRowFormat, searchList);
    })

})

