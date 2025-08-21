
document.addEventListener('DOMContentLoaded', function (){
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
    })
})
