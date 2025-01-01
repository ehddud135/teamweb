

document.addEventListener('DOMContentLoaded', () => {

    flatpickr("#inspection-month-picker", {
        dateFormat: "Y-m",  // 년-월 형식
        plugins: [
            new monthSelectPlugin({
                shorthand: true,  // 월 이름을 간단히 표시
                dateFormat: "Y-m", // 결과 형식
                altFormat: "F Y",  // 화면에 표시될 형식 (예: February 2025)
            })
        ]
    });
    // const month_picker = document.getElementById("inspection-month-picker")
    // console.log(month_picker)
    // const datepicker = new Datepicker(month_picker, {
    //     format: 'mm/yyyy',
    //     autohide: true,
    //     startView: 1,
    //     minViewMode: 1,
    //     pickLevel: 1   
    // });

    // month_picker.value = '01/2024';
});


async function fetchAndRenderData() {
    // API 호출
    const monthly_response = await fetch('/inspection-list-api/monthly');
    const quarter_response = await fetch('/inspection-list-api/quarter');
    const half_response = await fetch('/inspection-list-api/half');
    const monthly_data = await monthly_response.json();
    const quarter_data = await quarter_response.json();
    const half_data = await half_response.json();
    
    function renderTable(pageData, id) {
        // 테이블에 데이터 추가
        const tableBody = document.getElementById(id);
        tableBody.innerHTML = '';  // 기존 데이터를 초기화
        

        pageData.forEach(item => {
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
    renderTable(monthly_data, "monthly-table-body")
    renderTable(quarter_data, "quarter-table-body")
    renderTable(half_data, "half-table-body")

}

// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData;