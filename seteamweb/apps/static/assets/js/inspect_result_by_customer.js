async function loadCustomerList(){
    try {
        const response = await fetch('/customer-name-list');
        const customerList = await response.json();

        const customerPicker = document.getElementById('inspection-customer-picker');
        customerPicker.innerHTML = '<option selected>Choose Customer</option>';

        customerList.forEach(customer => {
            const option = document.createElement('option');
            option.value = customer.name; // 고객 ID
            option.textContent = customer.name; // 고객 이름
            customerPicker.appendChild(option);
        });
    } catch (e){
        console.log(e.message)
    }
}


document.addEventListener('DOMContentLoaded', () => {
    loadCustomerList()
    const customerPicker = document.getElementById('inspection-customer-picker');
    customerPicker.addEventListener('change', (event) => {
        fetchAndRenderData(event.target.value)
    });
});


async function fetchAndRenderData(customer_name) {
    // API 호출
    document.getElementById("inspection-customer").textContent = `${customer_name} 정기 점검 결과`;

    function renderTable(pageData) {
        // 테이블에 데이터 추가
        const tableBody = document.getElementById("table-body-by-customer");
        tableBody.innerHTML = '';  // 기존 데이터를 초기화

        pageData.forEach(item => {
            const row = `
                <tr>
                    <td>${new Date(item.inspection_date).toLocaleDateString()}</td>
                    <td>${item.name}</td>
                    <td>${item.name}</td>
                    <td>${item.name}</td>
                    <td>${item.name}</td>
                    <td>${item.name}</td>
                    <td>${item.name}</td>
                    <td>${item.manager}</td>
                    <td>${item.inspect_result}</td>
                    <td>${new Date(item.inspection_date).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-info pdf-view-btn" data-name="${item.name}" pdf-view-url="/inspection-report/view">View</button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    let data_response = await fetch(`/inspection-result-by-customer/${customer_name}`)
    let data = await data_response.json();
    renderTable(data)
}
