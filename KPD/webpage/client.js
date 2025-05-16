
async function loadFsdata(filter = '') {
    try {
        let url = '/api/fsdata';
        if (filter) url += `?company=${encodeURIComponent(filter)}`

        const response = await fetch(url);
        if (!response.ok) throw new Error('데이터 로드 실패');
        const data = await response.json();

        const container = document.getElementById('fsdataContainer');
        container.innerHTML = '';

        if (data.length === 0) {
            container.textContent = '검색 결과가 없습니다.';
            return;
        }

        // 표시할 열 이름을 배열로 설정 (예: ticker, name, price)
        const displayColumns = ['ticker', '평균주가','per', 'psr','pbr', 'EPS','SPS','BPS']; // 실제 열 이름으로 변경 필요

        // 1) thead 만들기
        let html = '<table>';
        html += '<thead><tr>'
        displayColumns.forEach(col => {
            html += `<th>${col}</th>`;
        });
        html += '</tr></thead>';

        // 2) tbody 만들기
        html += '<tbody>';
        data.forEach(row => {
            html += '<tr>';
            displayColumns.forEach(col => {
                html += '<td>' + (row[col]) + '</td>';
            });
            html += '</tr>'
        });
        html += '</tbody></table>';

        container.innerHTML = html;
    } catch (error) {
        alert(error.message);
    }
}


// 검색 버튼 클릭시
document.getElementById('searchBtn').addEventListener('click', () => {
    const keyword = document.getElementById('searchInput').value.trim();
    loadFsdata(keyword);
});

// 초기 데이터 로드
loadFsdata();

