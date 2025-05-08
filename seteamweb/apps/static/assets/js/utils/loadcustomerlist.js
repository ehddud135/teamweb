async function loadCustomerList(){
    try {
        const response = await fetch('/customer/name-list');
        const customerList = await response.json()

        const customerPicker = document.getElementById('customer-picker');
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