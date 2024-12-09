console.log(Swal)

const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-gray'
    },
    buttonsStyling: false
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('appendForm');
    console.log("Test Logging")
    if (form) {
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            console.log('Form submitted!');

            const formData = new FormData(form);

            try {
                const response = await fetch(form.action, {
                    method: form.method,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: formData
                });
                console.log(response)

                if (response.ok) {
                    const data = await response.json();
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
                        'You clicked the button!',
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
});
