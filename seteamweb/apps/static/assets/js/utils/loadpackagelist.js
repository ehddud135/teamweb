async function loadPakcageListByCustomer(name, package_name, platform){
    try {
        const response = await fetch(`/package/list-by-cusomter-api/${name}/${platform}`);
        const package_list = await response.json();
        package_name.innerHTML = '<option></option>'
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