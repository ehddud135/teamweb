let apiUrl = '/package/list-api'
function dataRowFormat(item, item_id) {
    row = `
                <tr>
                    <td>${item_id}</td>
                    <td>${item.name}</td>
                    <td>${item.customer}</td>
                    <td>${item.platform}</td>
                    <td>${new Date(item.license_expire_date).toLocaleDateString()}</td>
                    <td>${new Date(item.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-delete-url="/package/delete/${item.name}/${item.platform}">Delete</button>
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