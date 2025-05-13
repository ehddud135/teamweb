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
        let filename = null
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
                const disposition = response.headers.get('Content-Disposition');
                filename = getFileNameFromDisposition(disposition);
                return response.blob(); // 서버로부터 받은 파일 데이터를 Blob으로 변환
            }).then(blob => {
                if (event.target.classList.contains('pdf-view-btn')){ 
                    const pdfUrl = URL.createObjectURL(blob);
                    window.open(pdfUrl, '_blank'); // 새로운 탭에서 PDF 열기
                } else if (event.target.classList.contains('download-btn')) {
                    const pdfUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = pdfUrl;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                }
            }).catch(error => console.error('Error fetching PDF:', error));
        })    
    })
}

function getFileNameFromDisposition(headerValue) {
    if (!headerValue) return null;

    // filename*=utf-8''%EA%B0%80%EC%9E%A5.pdf 형식
    const filenameStarMatch = headerValue.match(/filename\*\=([^;]+)/i);
    if (filenameStarMatch) {
        const encoded = filenameStarMatch[1].replace(/^UTF-8''/i, '');
        return decodeURIComponent(encoded);
    }

    // fallback to regular filename=
    const filenameMatch = headerValue.match(/filename=\"?([^\";]+)\"?/i);
    return filenameMatch ? filenameMatch[1] : null;
}