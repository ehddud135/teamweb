const apiUrl = '/customer/list-api';
function dataRowFormat(item, item_id) {
    inspection = item.inspection ? 'O': 'X'
    row = `
            <tr>
                <td>${item_id}</td>
                <td>${item.name}</td>
                <td>${item.manager}</td>
                <td>${item.package_count}</td>
                <td>${new Date(item.created_at).toLocaleDateString()}</td>
                <td>${inspection}</td>
                <td>${item.inspect_schedule}</td>
                <td>
                    <button class="btn btn-danger delete-btn" data-delete-url="/customer/delete/${item.name}">Delete</button>
                    <button class="btn btn-danger modify-btn" data-name="${item.name}">Modify</button>
                </td>
            </tr>
            `;
    return row
}

// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData(apiUrl, dataRowFormat);

const modalElement = document.getElementById('append-modal-form');
 
 modalElement.addEventListener('submit', ()=> {
     fetchAndRenderData(apiUrl, dataRowFormat);
 })
