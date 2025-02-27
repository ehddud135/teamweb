document.addEventListener('DOMContentLoaded', function (){
    const inspection_months = document.getElementById('inspection-month').textContent.split(' ');
    const inspection_month = inspection_months[0] + " " + inspection_months[1]
    document.addEventListener('click', function (event) {
        if (event.target.classList.contains('pdf-view-btn')){
            const viewUrl = event.target.getAttribute('pdf-view-url')
            const customer_name = event.target.getAttribute('data-name')
            fetch(viewUrl, {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ "customer_name": customer_name, "inspection_month": inspection_month })
            }).then(response => {
                if (!response.ok) {
                    swalWithBootstrapButtons.fire(
                        'Warning alert',
                        data['error'],
                        'warning'
                    )
                    throw new Error('Failed to fetch the PDF');
                }
                return response.blob(); // 서버로부터 받은 파일 데이터를 Blob으로 변환
            }).then(blob => {
                const pdfUrl = URL.createObjectURL(blob);
                window.open(pdfUrl, '_blank'); // 새로운 탭에서 PDF 열기
            }).catch(error => console.error('Error fetching PDF:', error));
        }
        else if (event.target.classList.contains('download-btn')){
            console.log("click download btn")
            const downloadUrl = event.target.getAttribute('pdf-download-url')
            const customer_name = event.target.getAttribute('data-name')
            let downalod_file_name = `${inspection_month}_${customer_name}_정기점검_확인서.pdf`

            fetch(downloadUrl, {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ "customer_name": customer_name, "inspection_month": inspection_month })

            }).then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch the PDF');
                }
                return response.blob().then(blob => ({ blob, downalod_file_name })); // 서버로부터 받은 파일 데이터를 Blob으로 변환
            }).then(({ blob, downalod_file_name }) => {
                const pdfUrl = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = pdfUrl;
                a.download = downalod_file_name;
                document.body.appendChild(a);
                a.click();
                a.remove();
            }).catch(error => console.error('Error fetching PDF:', error));

        };
    })
})