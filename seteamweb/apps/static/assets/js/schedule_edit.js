document.addEventListener('DOMContentLoaded', function (){

    const modal = new bootstrap.Modal(document.getElementById('modify-modal-form'))
    const form = document.getElementById('modifyForm');
    const period = document.getElementById('inspection-period')
    const checkboxes = document.querySelectorAll('input[name="months"]');

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
            for (const [key, value] of formData) {
                console.log(`${key}: ${value}`);
              }
            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                });
                const data = await response.json();
                console.log(data)

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