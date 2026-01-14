document.addEventListener('DOMContentLoaded', function (){

    const modal = new bootstrap.Modal(document.getElementById('modify-modal-form'))
    const form = document.getElementById('modifyForm');
    const period = document.getElementById('inspection-period')
    const checkboxes = document.querySelectorAll('input[name="months"]');                

    loadManagerList()
    let manager_name = ""
    $('#manager-picker').select2({
        theme: 'bootstrap-5',
        width: '240',
        placeholder: $('#manager-picker').data('placeholder'),
        dropdownParent: $('#modify-modal-form'),
        dropdownCssClass: 'select2--small',
        containerCssClass: 'select2--small',
    });
    $('#manager-picker').on('change', function() {
        manager_name = $(this).val()
    })

    if (form) {
        document.addEventListener('click', function (event) {
            if (event.target.classList.contains('modify-btn')){
                const customer_name = event.target.dataset.name;
                document.getElementById("modify-customer-name-label").textContent = `Customer Name : ${customer_name}`;
                document.getElementById("modify-customer-name").value = customer_name
                modal.show();
            }
        })
        
        period.addEventListener("change", (e) => {
            const selected = e.target.value

            if (selected == "monthly") {
                checkboxes.forEach((checkbox) => {
                    checkbox.checked = true
                });
            } else{
                checkboxes.forEach((checkbox) => {
                    checkbox.checked = false
                });
            }
        })

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(form);
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
                        timer: 3000
                    }).then(() => {
                        // SweetAlert 종료 후 모달 닫기
                        const modal = bootstrap.Modal.getInstance(document.getElementById('modify-modal-form'));
                        if (modal) {
                            modal.hide();
                        }
                    });
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

