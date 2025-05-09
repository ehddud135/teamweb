// Function to handle PDF view or download
function pdfViewOrDownload(bodyDataFormat, tableBody) {
    tbodyList = document.querySelectorAll('tbody[id$="-table-body"]')
    if (tableBody) {
        tbodyList = tableBody
    }
    tbodyList.forEach(tbody => {
        tbody.addEventListener('click', async function(event) {
        let url = event.target.getAttribute('pdf-url')
        eventData = event.target.dataset
        bodyData = bodyDataFormat(eventData)
        jsonData = JSON.stringify(bodyData)
        fetch(url, {
            method: 'POST',
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: jsonData
            }).then(response => {
                if (!response.ok) {
                    console.log(response)
                    swalWithBootstrapButtons.fire(
                        'Warning alert',
                        data['error'],
                        'warning'
                    )
                    throw new Error('Failed to fetch the PDF');
                }
                return response.blob(); // 서버로부터 받은 파일 데이터를 Blob으로 변환
            }).then(blob => {
                if (event.target.classList.contains('pdf-view-btn')){ 
                    const pdfUrl = URL.createObjectURL(blob);
                    window.open(pdfUrl, '_blank'); // 새로운 탭에서 PDF 열기
                } else if (event.target.classList.contains('download-btn')) {
                    let downalod_file_name = `${eventData.inspectionMonth}_${eventData.dataset.name}_정기점검_확인서.pdf`
                    const pdfUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = pdfUrl;
                    a.download = downalod_file_name;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                }
            }).catch(error => console.error('Error fetching PDF:', error));
        })    
    })
}