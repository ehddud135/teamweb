async function fetchAndRenderData() {
    // API 호출
    const response = await fetch('/manager-list-api');
    const data = await response.json();
    
    // 페이지네이션 설정
    const itemsPerPage = 10; // 한 페이지에 표시할 항목 수
    let currentPage = 1;

    function getPaginatedData(page) {
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        return data.slice(start, end);
    }

    function renderTable(pageData) {
        // 테이블에 데이터 추가
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';  // 기존 데이터를 초기화
        let item_id = (currentPage - 1) * itemsPerPage;
        

        data.forEach(item => {
            item_id++;
            const row = `
                <tr>
                    <td>${item_id}</td>
                    <td>${item.name}</td>
                    <td>${item.email}</td>
                    <td>${item.customer_count}</td>
                    <td>${new Date(item.created_at).toLocaleDateString()}</td>
                    <td>
                        <button class="btn btn-danger delete-btn" data-delete-url="/manager-delete/${item.name}">Delete</button>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    // 페이지네이션 버튼 렌더링
    function renderPagination() {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = ''; // 기존 버튼 초기화
        const totalPages = Math.ceil(data.length / itemsPerPage); // 총 페이지 수

        // "Previous" 버튼
        const prevButton = `
            <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
            </li>
        `;
        pagination.innerHTML += prevButton;

        // 페이지 번호 버튼
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = `
                <li class="page-item ${i === currentPage ? 'active' : ''}">
                    <a class="page-link" href="#" data-page="${i}">${i}</a>
                </li>
            `;
            pagination.innerHTML += pageButton;
        }

        // "Next" 버튼
        const nextButton = `
            <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
            </li>
        `;
        pagination.innerHTML += nextButton;
    }

    // 페이지네이션 정보 업데이트
    function updatePaginationInfo() {
        const start = (currentPage - 1) * itemsPerPage + 1;
        const end = Math.min(currentPage * itemsPerPage, data.length);
        const paginationInfo = document.getElementById('pagination-info');
        paginationInfo.innerHTML = `Showing <b>${start}</b> to <b>${end}</b> out of <b>${data.length}</b> entries`;
    }

    // 페이지 변경 핸들러
    function handlePageChange(event) {
        event.preventDefault();
        const page = parseInt(event.target.getAttribute('data-page'));
        if (!isNaN(page)) {
            currentPage = page;
            updateTableAndPagination();
        }
    }

    // 테이블과 페이지네이션 갱신
    function updateTableAndPagination() {
        const pageData = getPaginatedData(currentPage);
        renderTable(pageData);
        renderPagination();
        updatePaginationInfo();

        // 페이지네이션 버튼 클릭 이벤트 추가
        document.querySelectorAll('#pagination .page-link').forEach(button => {
            button.addEventListener('click', handlePageChange);
        });
    }

    // 초기 렌더링
    updateTableAndPagination();
}

// 페이지 로드 시 데이터 가져오기
window.onload = fetchAndRenderData;