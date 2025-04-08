function convertToYYYYMM(dateString) {
    const months = {January: '01', February: '02', March: '03', April: '04', May: '05', June: '06', July: '07', August: '08', September: '09', October: '10', November: '11', December: '12'};
    const month = months[dateString];
    if (!month) {
        throw new Error(`Invalid month: ${dateString}`);
    }
    return month
}

document.addEventListener('DOMContentLoaded', () => {
    let date = new Date;
    let year = date.getFullYear();
    // month = String(date.getMonth() + 1).padStart(2, '0');
    month = date.toLocaleString('en-US', { month: 'long'});
    const month_picker = document.getElementById("inspection-month-picker")
    const month_pickers = new Datepicker(month_picker, {
        format: 'yyyy-MM',
        autohide: true,
        startView: 1,
        minViewMode: 1,
        pickLevel: 1,
    });
    month_picker.value = year + "-" + month;

    month_picker.addEventListener('changeDate', (event) => {
        fetchAndRenderData(event.target.value)
    });


    fetchAndRenderData(month_picker.value)
});


async function fetchAndRenderData(month) {
    // API 호출
    date = month.split('-');
    picked_year = date[0]
    picked_month = date[1]
    month = convertToYYYYMM(picked_month)
    picked_date = picked_year + "년 " + month + "월"
    document.getElementById("inspection-month").textContent = `${picked_date} 정기 점검 결과`;

    function renderTable(pageData, id) {
        // 테이블에 데이터 추가
        const tableBody = document.getElementById(id);
        tableBody.innerHTML = '';  // 기존 데이터를 초기화
        let item_id = 0;

        pageData.forEach(item => {
            significatn_btn = ``;
            item_id++;
            if (item.inspect_significant) {
                significatn_btn += `<button class="btn btn-info signifi-btn" url="/inspection-significant-per-monthly-result"
                                data-inspection-date=${item.inspection_date} data-customer-name=${item.name}>View</button>`;
            }
            console.log(item);
            const row = `
                <tr>
                    <td>${item_id}</td>
                    <td>${item.name}</td>
                    <td>${item.manager}</td>
                    <td>${item.inspect_result}</td>
                    <td>${new Date(item.inspection_date).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-outline-success append-btn" data-name="${item.name}">등 록</button>
                    </td>
                    <td>
                    ${significatn_btn}
                    </td>
                    <td>
                        <button class="btn btn-info pdf-view-btn" data-name="${item.name}" pdf-view-url="/inspection-report/view">View</button>
                        <button class="btn btn-info download-btn" data-name="${item.name}" pdf-download-url="/inspection-report/download">Download</button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    const period_list = ['monthly', 'quarter', 'half']
    
    for (let period of period_list){
        let data_response = await fetch(`/inspection-list-api/${period}/${picked_month}`)
        let data = await data_response.json();
        renderTable(data, `${period}-table-body`)
    }

}
