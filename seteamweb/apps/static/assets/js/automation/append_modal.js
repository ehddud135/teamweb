const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-gray'
    },
    buttonsStyling: false
});

document.addEventListener('DOMContentLoaded', function (){
    const customerSelect = document.getElementById("customer-picker");
    const packageSelect = document.getElementById("package-picker"); // 패키지 셀렉트 id에 맞게 수정
    const form = document.getElementById("appendForm");
    loadCustomerList()
    let customer_name = ""
    $('#customer-picker').select2({
        theme: 'bootstrap-5',
        width: '240',
        placeholder: $('#customer-picker').data('placeholder'),
        dropdownParent: $('#append-modal-form'),
        dropdownCssClass: 'select2--small',
        containerCssClass: 'select2--small',
    });
    $('#customer-picker').on('change', function() {
        customer_name = $(this).val()
        loadPakcageListByCustomer(customer_name, packageSelect, "android")
    })

    $('#package-picker').select2({
        theme: 'bootstrap-5',
        width: '240',
        placeholder: $('#package-picker').data('placeholder'),
        dropdownParent: $('#append-modal-form'),
        dropdownCssClass: 'select2--small',
        containerCssClass: 'select2--small',
    });
    $('#package-picker').on('change', function() {
        package_name = $(this).val()
    })

    function toggleMode(mode) {
        const isSingle = mode === "single";

        customerSelect.disabled = !isSingle;
        packageSelect.disabled = !isSingle;
        customerSelect.required = isSingle;
        packageSelect.required = isSingle;
    }

    document.querySelectorAll('input[name="inspection_mode"]').forEach((radio) => {
        radio.addEventListener("change", (event) => 
            toggleMode(event.target.value));
    });
    
    const currentMode = document.querySelector('input[name="inspection_mode"]:checked').value;
    toggleMode(currentMode);
    if (form ){
        form.addEventListener("submit", async function (event){
            event.preventDefault();
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
                        text: 'Your inspect request has been success',
                        showConfirmButton: true,
                        timer: 3000
                    }).then(() => {
                        // SweetAlert 종료 후 모달 닫기
                        const modal = bootstrap.Modal.getInstance(document.getElementById('append-modal-form'));
                        if (modal) {
                            modal.hide();
                        }
                        form.reset();
                    });
                } else {
                    swalWithBootstrapButtons.fire(
                        'Warning alert',
                        data['error'],
                        'warning'
                    )
                    console.error('Error:', response.statusText);
                }
            } catch (e){
                console.log(e.message)
            }
        })
    }
})

