document.addEventListener('click', function (event) {
    // 모든 삭제 버튼에 대해 클릭 이벤트 처리
    if (event.target.classList.contains('delete-btn')){
        
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            
            button.addEventListener('click', function () {
                const deleteUrl = button.getAttribute('data-delete-url'); // 버튼의 URL 가져오기
                // SweetAlert2 팝업 표시
                Swal.fire({
                    title: 'Confirm',
                    text: '삭제 하시겠습니까?',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: 'Yes, delete it!',
                    cancelButtonText: 'Cancel'
                }).then(result => {
                    if (result.isConfirmed) {
                        // SweetAlert2 확인 버튼 클릭 시 HTMX 요청 실행
                        fetch(deleteUrl, {
                            method: 'DELETE',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'), // CSRF 토큰 추가
                                'Content-Type': 'application/json'
                            }
                        })
                        .then(response => {
                            if (response.ok) {
                                Swal.fire('Deleted!', 'Your item has been deleted.', 'success');
                                button.closest('tr').remove();
                            } else {
                                Swal.fire('Error!', 'Failed to delete the item.', 'error');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            Swal.fire('Error!', 'An unexpected error occurred.', 'error');
                        });
                    }
                });
            });
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
