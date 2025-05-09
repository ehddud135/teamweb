
document.addEventListener('DOMContentLoaded', function (){
    const modalElement = document.getElementById('append-modal-form')
    let modal = new bootstrap.Modal(modalElement)
    loadCustomerList()
    loadManagerList()
    let manager_name = ""
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
    })
    $('#manager-picker').select2({
        theme: 'bootstrap-5',
        width: '240',
        placeholder: $('#manager-picker').data('placeholder'),
        dropdownParent: $('#append-modal-form'),
        dropdownCssClass: 'select2--small',
        containerCssClass: 'select2--small',
    });
    $('#manager-picker').on('change', function() {
        customer_name = $(this).val()
    })

})
