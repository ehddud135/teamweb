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
            options = optionsByPlatform(item.platform, item)
            if (item.significant) {
                options += `<td>
                                <button class="btn btn-info pdf-view-btn" data-name="${item.name}" pdf-view-url="/inspection-report/view">View</button>
                            </td>`;
            }
            const row = `
                <tr>
                    <td>${new Date(item.inspection_date).toLocaleDateString()}</td>
                    <td>${item.package_name}</td>
                    <td>${item.platform}</td>
                    <td>${item.app_name}</td>
                    <td>${item.app_version}</td>
                    ${options}
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    let data_response = await fetch(`/inspection-result-by-customer/${customer_name}`)
    let data = await data_response.json();
    renderTable(data)
}

function optionsByPlatform(platform, item){
    const booleanToSymbol = (value) => value ? 'O' : 'X';
    let options = '';
    if (platform === 'Android') {
        options = `
            <td>${booleanToSymbol(item.rooting)}</td>
            <td>${booleanToSymbol(item.integrity)}</td>
            <td>${booleanToSymbol(item.emulator)}</td>
            <td>${booleanToSymbol(item.obfuscate)}</td>
            <td>${booleanToSymbol(item.decompile)}</td>
        `;
    } else if (platform === 'iOS') {
        options = `
            <td>${booleanToSymbol(item.jailbreak)}</td>
            <td>${booleanToSymbol(item.integrity)}</td>
            <td>${booleanToSymbol(item.string_encrypt)}</td>
            <td>${booleanToSymbol(item.symbol_del)}</td>
            <td>${item.library_version}</td>
        `;
    }
    return options
}