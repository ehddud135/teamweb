
let platform = document.getElementById('platform')
let apiUrl = `/devices/list-api/${platform.value}`
function dataRowFormat(item) {
    rooting = item.rooting ? 'O': 'X'
            row = `
            <tr>
            <td>${item.number} </td>
            <td>${item.name} </td>
            <td>${item.version} </td>
            <td>${item.architecture} </td>
            <td>${rooting} </td>
            </tr> `
    return row
}
// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData(apiUrl, dataRowFormat);

// 디바이스 리스트 OS 변경 시 데이터 가져오기
document.getElementById('platform').addEventListener('change', () => {
    apiUrl = `/devices/list-api/${platform.value}`
    fetchAndRenderData(apiUrl, dataRowFormat)
});
