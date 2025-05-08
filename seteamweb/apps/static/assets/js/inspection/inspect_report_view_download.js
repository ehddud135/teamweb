document.addEventListener('DOMContentLoaded', function (){
    document.addEventListener('click', function (event) {
        let url = event.target.getAttribute('pdf-url')
        eventData = event.target.dataset
        if (event.target.classList.contains('pdf-view-btn')){
            fetch(url, {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ "customer_name": eventData.name, "inspection_month": eventData.inspectionMonth })
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
            let downalod_file_name = `${eventData.inspectionMonth}_${eventData.dataset.name}_정기점검_확인서.pdf`

            fetch(url, {
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ "customer_name": eventData.name, "inspection_month": eventData.inspectionMonth })

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

function pdfViewOrDownload(bodyData) {

}