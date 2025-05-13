const apiUrl = '/customer/list-api';
function dataRowFormat(item, item_id) {
    inspection = item.inspection ? 'O': 'X'
    if (item.manager == null) {
        item.manager = '미정'
    }
    if (item.inspect_schedule == null) {
        item.inspect_schedule = '미진행'
    }
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

const isInsepctTrue = document.getElementById('inspection_modify_true') 
const isInsepctFalse = document.getElementById('inspection_modify_false')

isInsepctTrue.addEventListener('change', () => {
    setDisabledState(false);
});

isInsepctFalse.addEventListener('change', () => {
    setDisabledState(true);
});

function setDisabledState(disabled) {
    document.getElementById('inspection-period').disabled = disabled;
    document.querySelectorAll('.month-check').forEach(cb => {
        cb.disabled = disabled;
    });
}

const searchList = ['name', 'manager']
// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData(apiUrl, dataRowFormat, searchList);
document.addEventListener('', function () {})
const appendFormElement = document.getElementById('appendForm');
const modifyFormElement = document.getElementById('modifyForm');
appendFormElement.addEventListener('submit', ()=> {
    fetchAndRenderData(apiUrl, dataRowFormat, searchList);
})
modifyFormElement.addEventListener('submit', ()=> {
    fetchAndRenderData(apiUrl, dataRowFormat, searchList);
})