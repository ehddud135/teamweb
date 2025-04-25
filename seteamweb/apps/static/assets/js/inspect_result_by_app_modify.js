function convertToDMY(dateStr) {
    const date = new Date(dateStr);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 0-indexed
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
}


document.addEventListener('DOMContentLoaded', function (){
    const modalElement = document.getElementById('inspect-result-modal-form')
    const modal = new bootstrap.Modal(modalElement)
    const customerPicker = document.getElementById('inspection-customer-picker');
    const formElement =  modalElement.querySelector('#resultAppendForm');

    if (formElement) {
        console.log(formElement)
        document.addEventListener('click', function (event) {
            if (event.target.classList.contains('modify-btn')){
                cells = event.target.closest('tr').querySelectorAll('td')
                formElement.action = "/inspection-result-by-app-modify"
                formElement.method = "POST"
                const select_packages = formElement.querySelector('#select_packages');
                const customer_name = customerPicker.value
                const select_data_dict = {
                    inspectionDate: cells[0].textContent.trim(),
                    packageName: cells[1].textContent.trim(),
                    platform: cells[2].textContent.trim(),
                    appName: cells[3].textContent.trim(),
                    appVersion: cells[4].textContent.trim()
                  };
                const platform = (select_data_dict.platform === 'Android') ? 'android' : 'iOS'
                formElement.querySelector("#customer-name-label").textContent = `고객사 명 : ${customer_name}`;
                formElement.querySelector("#customer-name").value = customer_name
                formElement.querySelector("#select-platform-label").textContent = `OS : ${platform}`
                formElement.querySelector("#select-platform").value = platform
                invisibleBlock("inspection_date_group", formElement)
                formElement.querySelector("#inspection_date_label").textContent = `점검일자 : ${select_data_dict.inspectionDate}`
                formElement.querySelector("#inspection_date").value = convertToDMY(select_data_dict.inspectionDate)
                loadPackageListByCustomer(customer_name, select_packages, platform)
                formElement.querySelector("#select_packages_label").textContent = `Package Name : ${select_data_dict.packageName}`
                selectToInput(select_packages, select_data_dict.packageName)
                formElement.querySelector("#app_name").value = select_data_dict.appName
                formElement.querySelector("#app_version").value = select_data_dict.appVersion
                createCheckBoxes(platform);
                formElement.querySelector(".modal-footer").appendChild(insertDeleteButton(formElement, platform, modal))
                modal.show();
            }
        })
    } else {
        console.error('Form not found!');
    }
})

function invisibleBlock(block_id, formElement){
    block = formElement.querySelector(`#${block_id}`)
    block.style.position = 'absolute';
    block.style.left = '-9999px';
}

function selectToInput(selectElement, value){
    const inputElement = document.createElement('input');
    inputElement.type = 'hidden';
    inputElement.id = selectElement.id;
    inputElement.name = selectElement.name;
    inputElement.value = value;
    selectElement.parentNode.replaceChild(inputElement, selectElement);
}

function insertDeleteButton(formElement, platform, modal){
    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.className = 'btn btn-danger delete-btn';
    deleteButton.textContent = 'Delete';
    deleteButton.addEventListener('click', function() {
        const packageName = formElement.querySelector('#select_packages').value;
        const customerName = formElement.querySelector('#customer-name').value;
        const inspectionDate = formElement.querySelector('#inspection_date').value;
        const url = `/inspection-result-by-app-delete?platform=${platform}&packageName=${packageName}&customerName=${customerName}&inspectionDate=${inspectionDate}`;
        Swal.fire({
            title: 'Confirm',
            text: '삭제 하시겠습니까?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Yes, delete it!',
            cancelButtonText: 'Cancel'
        }).then(result => {
            if (result.isConfirmed) {
                // SweetAlert2 확인 버튼 클릭 시 HTMX 요청 실행
                fetch(url, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        swalWithBootstrapButtons.fire({
                            icon: 'success',
                            title: 'Deleted!',
                            text: 'Your item has been deleted.',
                            showConfirmButton: true,
                            timer: 1500
                        }).then(() => {
                            // SweetAlert 종료 후 모달 닫기
                            if (modal) {
                                modal.hide();
                                formElement.reset(); // 폼 초기화
                            }
                        });
                    } else {
                        Swal.fire('Error!', 'Failed to delete the item.', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire('Error!', 'An unexpected error occurred.', 'error');
                });
            }
        });
    });
    return deleteButton;
}