async function loadCategoryAndFsdata(filter = '', group = '') {
    try {
        // 1) 쿼리스트링 조합
        const params = [];
        if (filter) params.push(`ticker=${encodeURIComponent(filter)}`);
        if (group)  params.push(`group=${encodeURIComponent(group)}`);

        // 2) URL 생성
        let url = '/api/categoryandfsdata';
        if (params.length) {
            url += '?' + params.join('&');
        }

        // 3) 데이터 fetch
        const response = await fetch(url);
        if (!response.ok) throw new Error('결합된 데이터 로드 실패');
        const data = await response.json();

        // 4) 렌더링
        const container = document.getElementById('fsdataContainer');
        container.innerHTML = '';
        if (data.length === 0) {
            container.textContent = '검색 결과가 없습니다.';
            return;
        }

        // 5) 테이블 그리기 (기존 코드 유지)
        const displayColumns = [
            'kap_group', 'company', 'sector', 'industry', 'main_product' , 'PER','PSR','PBR'
        ];

        let html = '<table><thead><tr>';
        displayColumns.forEach(col => html += `<th>${col}</th>`);
        html += '</tr></thead><tbody>';
        data.forEach(row => {
            html += '<tr>';
            displayColumns.forEach(col => {
                html += `<td>${row[col] ?? ''}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table>';

        container.innerHTML = html;

    } catch (error) {
        alert(error.message);
    }
}


// 그룹 드롭다운 변경 시
document.getElementById('groupSelect').addEventListener('change', () => {
    const keyword = document.getElementById('searchInput').value.trim();
    const group   = document.getElementById('groupSelect').value;
    loadCategoryAndFsdata(keyword, group).then(r =>{} ).then(r =>{} ).then(r =>{} ).then(r =>{} ).then(r =>{} );
});



// 검색 버튼은 이 새 함수로 바인딩
document.getElementById('searchBtn').addEventListener('click', () => {
    const keyword = document.getElementById('searchInput').value.trim();
    const group   = document.getElementById('groupSelect').value;
    loadCategoryAndFsdata(keyword, group);
});


loadCategoryAndFsdata();




//
const selectBox = document.getElementById('discount-rate');
const customInput = document.getElementById('discount-rate-custom');

selectBox.addEventListener('change', () => {
    if (selectBox.value === 'custom') {
        customInput.style.display = 'inline-block';
    } else {
        customInput.style.display = 'none';
        customInput.value =''; //선택형으로 바꾸면 직접입력 초기화
    }
});

let discountValue;
if (selectBox.value === 'custom') {
    discountValue = parseFloat(customInput.value);
} else {
    discountValue = parseFloat(selectBox.value);
}


// 1) 선택 리스트에 행 추가 함수
function addToSelectedList(values) {
    const tbody = document.querySelector('#selectedTable tbody');
    const tr = document.createElement('tr');

    // 1) 포함용 체크박스 cell
    const tdCheck = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'include-checkbox';
    tdCheck.appendChild(checkbox);
    tr.appendChild(tdCheck);

    values.forEach(text => {
        const td = document.createElement('td');
        td.textContent = text;
        tr.appendChild(td);
    });
    tbody.appendChild(tr);
}

// 2) fsdataContainer 더블클릭 이벤트 리스너
document.getElementById('fsdataContainer').addEventListener('dblclick', e => {
    // 클릭된 위치에서 가장 가까운 <tr>을 찾는다
    const tr = e.target.closest('tr');
    if (!tr) return;
    // 헤더(<th>)가 아니라, 실제 데이터가 있는 <td>가 있어야 추가
    const tds = Array.from(tr.querySelectorAll('td'));
    if (tds.length === 0) return;

    // 각 <td>의 텍스트 값을 배열로 추출
    const values = tds.map(td => td.textContent.trim());

    // 선택 리스트에 추가
    addToSelectedList(values);
});

async function loadGroupOptions() {
    const res = await fetch('/api/groupnames');
    if (!res.ok) throw new Error('그룹명 로드 실패');
    const groups = await res.json();

    const sel = document.getElementById('groupSelect');
    // 중복 방지: 기본 옵션만 남기고 지우기
    sel.innerHTML = '<option value="">--전체--</option>';

    // 브라우저의 TextDecoder 를 사용, euc-kr 인코딩 지원하는 최신 브라우저에서 동작
    const decoder = new TextDecoder('euc-kr');

    groups.forEach(g => {
        let name = g.group_name;
        // Buffer 객체 형태인 경우: { type:'Buffer', data:[…] }
        if (name && typeof name === 'object' && Array.isArray(name.data)) {
            const uint8 = new Uint8Array(name.data);
            name = decoder.decode(uint8);
        }
        // 그렇지 않으면 이미 string 이므로 그대로 사용

        const opt = document.createElement('option');
        opt.value       = name;
        opt.textContent = name;
        sel.appendChild(opt);
    });
}

// 페이지 로드시 한 번만
loadGroupOptions().then(r =>{} ).then(r =>{} );

