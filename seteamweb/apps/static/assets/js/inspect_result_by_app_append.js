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
    const btn = document.getElementById('inspection_result_append_btn')
    const customerPicker = document.getElementById('inspection-customer-picker');
    customerPicker.addEventListener('change', (event) => {
        customer_name = event.target.value
    });

    btn.addEventListener('click', function (event) {
        if (form) {
            if (typeof customer_name === 'undefined') {
                console.log('customer_name is not defined');
                // 원하는 처리를 추가하세요
            } else {
                document.getElementById("customer-name-label").textContent = `고객사 명 : ${customer_name}`;
                document.getElementById("customer-name").value = customer_name
                const package_name = document.getElementById('package_name')
                const platforms = document.getElementById('platform')
                platforms.addEventListener('change', (event) =>{
                    console.log("test")
                    loadPakcageListByCustomer(customer_name, package_name, event.target.value)
                })
            }
            
            

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
                    console.log(data)

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

})

async function loadPakcageListByCustomer(name, package_name, platform){
    try {
        const response = await fetch(`/package-list-by-cusomter-api/${name}/${platform}`)
        const package_list = await response.json();
        package_name.innerHTML = ''
        package_list.forEach(package =>{
            const option = document.createElement('option');
            option.value = package.name;
            option.textContent = package.name;
            package_name.appendChild(option);
        });

    } catch (e){
        console.log(e)
    }
}

