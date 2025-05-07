const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
        confirmButton: 'btn btn-primary',
        cancelButton: 'btn btn-gray'
    },
    buttonsStyling: false
});


document.addEventListener('DOMContentLoaded', function (){
    const customerPicker = document.getElementById('inspection-customer-picker');
    const modalElement = document.getElementById('inspect-result-modal-form')
    let modal = new bootstrap.Modal(modalElement)
    let customer_name = ""
    customerPicker.addEventListener('change', (event) => {
        customer_name = event.target.value
    });

    document.querySelectorAll('.open-modal').forEach(btn =>{
        btn.addEventListener('click', function(){
            let formElement = modalElement.querySelector('#resultAppendForm');
            const select_packages = formElement.querySelector('#select_packages');
            platform = this.getAttribute('data-target')
            if (formElement) {
                formElement.action = "/inspection/result-by-app-append"
                formElement.method = "POST"
                if (customer_name === "") {
                    swalWithBootstrapButtons.fire(
                        'Warning alert',
                        '고객사를 선택해주세요.',
                        'warning'
                    );
                } else {
                    formElement.querySelector("#customer-name-label").textContent = `고객사 명 : ${customer_name}`;
                    formElement.querySelector("#select-platform-label").textContent = `OS : ${platform}`
                    formElement.querySelector("#select-platform").value = platform
                    formElement.querySelector("#customer-name").value = customer_name
                    loadPackageListByCustomer(customer_name, select_packages, platform)
                    createCheckBoxes(platform);
                    modal.show();
                }
            } else {
                console.error('Form not found!');
            }
        });
    });
    
    formElement.addEventListener('submit', async function (e) {
        e.preventDefault();
        modal = bootstrap.Modal.getInstance(formElement.closest('.modal'));
        const formData = new FormData(formElement);
        try {
            const response = await fetch(formElement.action, {
                method: formElement.method,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body:  formData
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
                    if (modal) {
                        modal.hide();
                        modalElement.querySelector('#resultAppendForm').reset();
                    }
                });
            } else {
                swalWithBootstrapButtons.fire(
                    'Warning alert',
                    data['error'],
                    'warning'
                )
                modalElement.querySelector('#resultAppendForm').reset();
                console.error('Error:', response.statusText);
            }   
            
        } catch (err) {
            console.error('Network Error:', err);
        }
    });

})

async function loadPackageListByCustomer(name, select_package, platform){
    try {
        const response = await fetch(`/package/list-by-cusomter-api/${name}/${platform}`);
        const package_list = await response.json();
        select_package.innerHTML = ''
        package_list.forEach(package =>{
            const option = document.createElement('option');
            option.value = package.name;
            option.textContent = package.name;
            select_package.appendChild(option);
        });
    } catch (e){
        console.log(e)
    }
}

function createCheckBoxes(os){
    const checkBoxes = document.getElementById('option-checkboxes');
    const ixp = document.getElementById('ios-library-version');
    if (ixp.firstChild){
        while (ixp.firstChild){
            ixp.removeChild(ixp.firstChild);
        }
    }
    if(checkBoxes){
        while (checkBoxes.firstChild) {
            checkBoxes.removeChild(checkBoxes.firstChild);
        }
    }
    options = getOptions(os)
    options.forEach(option => {
        const div = document.createElement('div');
        div.className = "form-check mb-2";
        const checkbox = document.createElement('input');
        const label = document.createElement('label');
        label.className = "form-check-label";
        label.textContent = option;
        label.htmlFor = option;
        checkbox.className = "form-check-input";
        checkbox.type = 'checkbox';
        checkbox.id = option;
        checkbox.value = option;
        checkbox.name = "options";
        checkbox.checked = false;
        checkbox.textContent = option
        div.appendChild(checkbox);
        div.appendChild(label);
        checkBoxes.appendChild(div);
    });

    if (os === 'iOS'){
        const label = document.createElement('label');
        const input = document.createElement('input');
        label.className = "my-1 me-2";
        label.htmlFor = "ios-library-version";
        label.textContent = "iOS Library Version";
        input.className = "form-control";
        input.type = 'text';
        input.id = "ios-library-version";
        input.name = "ios-library-version";
        input.placeholder = "iOS Library Version";
        ixp.appendChild(label);
        ixp.appendChild(input);                        
    }
}

function getOptions(os){
    if (os === 'iOS'){
        options = ['jailbreak_test', 'jailbreak', 'integrity', 'string_encrypt', 'symbol_del']
    }else if (os === 'android'){
        options = ['rooting_test', 'rooting', 'integrity', 'emulator', 'obfuscate', 'decompile']
    }
    return options
}