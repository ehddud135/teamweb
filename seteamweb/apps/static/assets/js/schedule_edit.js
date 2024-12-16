document.addEventListener('DOMContentLoaded', function (){

    const modal_2 = new bootstrap.Modal(document.getElementById('modify-modal-form'))
    const form = document.getElementById('modifyForm');

    if (form) {
        document.addEventListener('click', function (event) {
            if (event.target.classList.contains('modify-btn')){
                const customer_name = event.target.dataset.name;
                document.getElementById("modify-customer-name").textContent = `Customer Name : ${customer_name}`;
                modal_2.show();
            }
        })

        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            console.log(formData)
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
                        const modal = bootstrap.Modal.getInstance(document.getElementById('modal-form'));
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