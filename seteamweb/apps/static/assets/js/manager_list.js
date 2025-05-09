let apiUrl = '/manager/list-api'
function dataRowFormat(item, item_id) {
    row = `
                <tr>
                    <td>${item_id}</td>
                    <td>${item.name}</td>
                    <td>${item.email}</td>
                    <td>${item.customer_count}</td>
                    <td>${new Date(item.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-delete-url="/manager/delete/${item.name}">Delete</button>
                    </td>
                </tr>
            `;
    return row
}


// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData(apiUrl, dataRowFormat);
