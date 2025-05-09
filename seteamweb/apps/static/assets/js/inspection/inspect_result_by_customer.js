const modalElement = document.getElementById('inspect-result-modal-form');

const formElement = modalElement.querySelector('#resultAppendForm');
let customer_name = "";
let initialFormHTML = '';

document.addEventListener('DOMContentLoaded', () => {
    loadCustomerList()
    cacheInitialFormState(formElement)
    $('#customer-picker').select2({
        theme: 'bootstrap-5',
        width: '240',
        placeholder: $('#customer-picker').data('placeholder'),
        dropdownCssClass: 'select2--small',
        containerCssClass: 'select2--small',
    });

    $('#customer-picker').on('change', function() {
        customer_name = $(this).val()
        fetchAndRenderData(customer_name)
        viewSignificant(bodyDataFormat)
    })
});

function bodyDataFormat(data) {
    return {
        inspection_date: data.inspectionDate,
        customer_name: data.customerName,
        platform : data.platform,
        package_name : data.packageName
    }
}

// Modal 종료 시 폼 초기화

modalElement.addEventListener('hidden.bs.modal', ()=> {
    restoreInitialFormState(formElement)
    fetchAndRenderData(customer_name)
})


function cacheInitialFormState(formElement) {
    initialFormHTML = formElement.innerHTML;
}

function restoreInitialFormState(formElement) {
    formElement.innerHTML = initialFormHTML;
    const dateInput = formElement.querySelector('#inspection_date');
    if (dateInput) {
        new Datepicker(dateInput, { format: 'mm/dd/yyyy' });
    }
}


async function fetchAndRenderData(customer_name) {
    // API 호출
    document.getElementById("inspection-customer").textContent = `${customer_name} 정기 점검 결과`;
    let data_response = await fetch(`/inspection/result-by-customer/${customer_name}`)
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

   
function renderTable(pageData) {
    // 테이블에 데이터 추가
    const tableBody = document.getElementById("customer-table-body");
    tableBody.innerHTML = '';  // 기존 데이터를 초기화

    pageData.forEach(item => {
        options = optionsByPlatform(item.platform, item)
        if (item.significant) {
            options += `<td>
                            <button class="btn btn-info signifi-btn" url="/inspection/significant-per-app"
                            data-package-name="${item.package_name}" data-inspection-date="${item.inspection_date}"
                            data-customer-name="${customer_name}" data-platform="${item.platform}">View</button>
                        </td>
                        <td>
                            <button class="btn btn-danger modify-btn">Modify</button>
                        </td>`;
        }
        else {
            options += `<td></td>
                        <td>
                            <button class="btn btn-danger modify-btn">Modify</button>
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
