async function loadManagerList(){
    try {
        const response = await fetch('/manager/name-list');
        const customerList = await response.json()

        const customerPicker = document.getElementById('manager-picker');
        customerPicker.innerHTML = '<option></option>'; // 초기화

        customerList.forEach(customer => {
            const option = document.createElement('option');
            option.value = customer.name; // 고객 ID
            option.textContent = customer.name; // 고객 이름
            customerPicker.appendChild(option);
        });
    } catch (e){
        console.log(e.message)
    }
}