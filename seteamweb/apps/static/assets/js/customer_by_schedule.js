async function fetchAndRenderData() {
    // API 호출
    const response = await fetch('/customer-list-api');
    const data = await response.json();
    
    function renderTable(pageData) {
        // 테이블에 데이터 추가
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';  // 기존 데이터를 초기화
        

        data.forEach(item => {
            const row = `
                <tr>
                    <td>${item.name}</td>
                    <td>${item.manager}</td>
                    <td>${item.package_count}</td>
                    <td>${new Date(item.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-delete-url="/manager-delete/${item.name}">Delete</button>
                        <button class="btn btn-danger modify-btn" data-name="${item.name}">Modify</button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }


    renderTable(data)

}

// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData;