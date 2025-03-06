const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-gray'
    },
    buttonsStyling: false
});

document.addEventListener('DOMContentLoaded', function (){

    const modal = new bootstrap.Modal(document.getElementById('inspect-result-modal-form'))
    const form = document.getElementById('resultAppendForm');
    const inspection_months = document.getElementById('inspection-month').textContent.split(' ');
    let inspection_month = inspection_months[0] + " " + inspection_months[1]
    document.getElementById('inspection-month-picker').addEventListener('changeDate', function (event) {
        let picked_month = event.target.value.split('-')[1]
        let picked_year = event.target.value.split('-')[0]
        inspection_month = convertToYYYYMM(picked_month)
        inspection_month = picked_year + "년 " + inspection_month + "월"
    })
    
    if (form) {
        document.addEventListener('click', function (event) {
            if (event.target.classList.contains('append-btn')){
                const customer_name = event.target.dataset.name;
                document.getElementById("customer-name-label").textContent = `고객사 명 : ${customer_name}`;
                document.getElementById("customer-name").value = customer_name
                document.getElementById("inspect-month-label").textContent = `점검 월 : ${inspection_month}`;
                document.getElementById("inspect-month").value = inspection_month
                modal.show();
            }
        })

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            for (const [key, value] of formData) {
              }
            const customer_name = document.getElementById('customer-name').value;
            const report_file_name = `${inspection_month}_${customer_name}_정기점검_확인서_STEALIEN`
            formData.append('title', report_file_name)
            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                });
                const data = await response.json();

                if (response.ok) {
                    swalWithBootstrapButtons.fire({
                        icon: 'success',
                        title: 'Success alert',
                        text: 'Your work has been saved',
                        showConfirmButton: true,
                        timer: 1500
                    }).then(() => {
                        // SweetAlert 종료 후 모달 닫기
                        const modal = bootstrap.Modal.getInstance(document.getElementById('inspect-result-modal-form'));
                        if (modal) {
                            modal.hide();
                        }
                        console.log('Modal closed');
                        form.reset();
                    });
                    console.log('Success:', data);
                } else {
                    swalWithBootstrapButtons.fire(
                        'Warning alert',
                        data['error'],
                        'warning'
                    )
                    console.error('Error:', response.statusText);
                }
            } catch (err) {
                console.error('Network Error:', err);
            }
        });
    } else {
        console.error('Form not found!');
    }

})