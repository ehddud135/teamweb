document.addEventListener('click', function (event) {
    // 모든 삭제 버튼에 대해 클릭 이벤트 처리
    if (event.target.classList.contains('upload-btn')){
        const button = event.target;
        const uploadUrl = button.getAttribute('data-upload-url'); // 버튼의 URL 가져오기
        // SweetAlert2 팝업 표시
        Swal.fire({
            title: 'Confirm',
            html: `
                    <div class="mb-3">
                        <textarea id="significant" class="form-control" rows="4" placeholder="특이사항을 입력하세요"></textarea>
                    </div>
                    <div class="form-check text-start">
                        <input class="form-check-input" type="checkbox" id="isobfuscate">
                        <label class="form-check-label" for="isobfuscate">난독화 여부</label>
                    </div>
                `,
            icon: 'success',
            showCancelButton: true,
            confirmButtonText: 'Yes, upload it!',
            cancelButtonText: 'Cancel',
            preConfirm: () => {
                const container = Swal.getHtmlContainer();
                return {
                    significant: container.querySelector("#significant").value.trim(),
                    isobfuscate: container.querySelector("#isobfuscate").checked,
                };
            },
        }).then(result => {
            if (result.isConfirmed) {
                // SweetAlert2 확인 버튼 클릭 시 HTMX 요청 실행
                const { significant, isobfuscate } = result.value;
                fetch(uploadUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'), // CSRF 토큰 추가
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ significant, isobfuscate }) // 특이사항 전송
                })
                .then(response => {
                    console.log(response)
                    if (response.ok) {
                        Swal.fire('Upload!', 'The data has been saved to the database', 'success');
                        button.closest('tr').remove();
                    } else {
                        return response.json().then((data) => {
                            throw new Error(data.message || "Failed to upload the item.");
                        });
                    }
                })
                .catch(error => {
                    Swal.fire('Error!', error.message, 'error');
                });
            }
        });
    }
});

// CSRF 토큰 가져오기
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
    return cookieValue || '';
}
