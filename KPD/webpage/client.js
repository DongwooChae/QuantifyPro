// client.js

// 전역 상태
let lastData = [];                              // 서버에서 받아온 최신 데이터
let currentSort = { key: null, asc: true };      // 정렬 상태
let main_product_keywords = [];                  // 주요상품 키워드 태그 배열

// ===== ① 숫자 / 퍼센트 포맷 함수 추가 =====
/** 정수 반올림 + 천단위 콤마 */
function formatKR(value) {
  if (value == null || isNaN(value)) return '-';
   return Math.round(value).toLocaleString('ko-KR');
 }

/** 0.10 → "10%", 소수점 버림 */
function formatPercent(value) {
  if (value == null || isNaN(value)) return '-';
    return value.toLocaleString('ko-KR', {
        style: 'percent',
            maximumFractionDigits: 0
           });
         }

/**
 * div.last-selected-company 안에
 * 포함된(체크된) 기업들의
 * kap_group, company, PER, PSR, PBR 테이블로 뿌린다.
 */
function updateLastSelectedCompanies() {
    const container = document.querySelector('.last-selected-company');
    // 헤더
    let html = `
    <table class="parameter-table">
      <thead>
        <tr>
          <th>kap_group</th>
          <th>company</th>
          <th>PER</th>
          <th>PSR</th>
          <th>PBR</th>
        </tr>
      </thead>
      <tbody>
  `;
    // body: selectedTable 에서 체크된 행들
    document.querySelectorAll('#selectedTable tbody tr').forEach(tr => {
        const cb = tr.querySelector('input.include-checkbox');
        if (!cb.checked) return;
        const cells = tr.querySelectorAll('td');
        const grp = cells[1].textContent.trim();
        const cmp = cells[2].textContent.trim();
        const per = cells[7].textContent.trim();
        const psr = cells[8].textContent.trim();
        const pbr = cells[9].textContent.trim();

        html += `
      <tr>
        <td>${grp}</td>
        <td>${cmp}</td>
        <td>${per}</td>
        <td>${psr}</td>
        <td>${pbr}</td>
      </tr>
    `;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;

    // ── 여기에 추가: 정렬 기능 활성화 ──
    const table = container.querySelector('table');
    const headers = table.querySelectorAll('th');
    const tbody   = table.querySelector('tbody');

    headers.forEach((th, colIdx) => {
        let asc = true;
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            // 1) 현재 행들 가져오기
            const rows = Array.from(tbody.querySelectorAll('tr'));
            // 2) 정렬
            rows.sort((a, b) => {
                const aText = a.cells[colIdx].textContent.trim();
                const bText = b.cells[colIdx].textContent.trim();
                const aNum  = parseFloat(aText.replace(/,/g, ''));
                const bNum  = parseFloat(bText.replace(/,/g, ''));
                const va = !isNaN(aNum) ? aNum : aText;
                const vb = !isNaN(bNum) ? bNum : bText;
                if (va < vb) return asc ? -1 : 1;
                if (va > vb) return asc ? 1 : -1;
                return 0;
            });
            // 3) 정렬된 순서로 다시 붙이기
            rows.forEach(r => tbody.appendChild(r));
            asc = !asc;
        });
    });
}





// ── Input → Value/Apply/Aggregate/Final 계산 함수 ──
function updateValuation() {
    // 1) Input 값 파싱
    const eps = parseFloat(document.getElementById('company-eps').value) || 0;
    const bps = parseFloat(document.getElementById('company-bps').value) || 0;
    const sps = parseFloat(document.getElementById('company-sps').value) || 0;

    // 2) 주당 가치 셀 채우기
    document.getElementById('value-per').textContent  = formatKR(eps);
    document.getElementById('value-psr').textContent = formatKR(sps);
    document.getElementById('value-pbr').textContent = formatKR(bps);


    // 3) 평균값 읽어서 적용주가 계산
    const avgPer = parseFloat(document.getElementById('avg-per').textContent) || 0;
    const avgPsr = parseFloat(document.getElementById('avg-psr').textContent) || 0;
    const avgPbr = parseFloat(document.getElementById('avg-pbr').textContent) || 0;

    const applyPer = avgPer * eps;
    const applyPsr = avgPsr * sps;
    const applyPbr = avgPbr * bps;

    document.getElementById('apply-per').textContent  = formatKR(applyPer);
    document.getElementById('apply-psr').textContent = formatKR(applyPsr);
    document.getElementById('apply-pbr').textContent = formatKR(applyPbr);

    // 4) 체크박스에 따라 Aggregate 적용주가
    const perChk = document.getElementById('choose-per');
    const psrChk = document.getElementById('choose-psr');
    const pbrChk = document.getElementById('choose-pbr');
    let sum = 0, cnt = 0;
    if (perChk.checked && applyPer>0) { sum+=applyPer; cnt++; }
    if (psrChk.checked && applyPsr>0) { sum+=applyPsr; cnt++; }
    if (pbrChk.checked && applyPbr>0) { sum+=applyPbr; cnt++; }
    const agg = cnt ? sum/cnt : 0;
    document.getElementById('apply-aggregate').textContent = formatKR(agg);

    // 5) 할인율 읽고 Discount 셀, FinalPrice 계산
    const discSelect = document.getElementById('discount-rate');
    const discCustom = document.getElementById('discount-rate-custom');
    let disc = parseFloat(discSelect.value) || 0;
    if (discSelect.value==='custom') disc = parseFloat(discCustom.value)||0;
    document.getElementById('apply-discount-rate').textContent = formatPercent(disc);

    const finalPrice = agg * (1 - disc);
    document.getElementById('apply-final-price').textContent =
        (agg && disc<1) ? formatKR(finalPrice) : '-';
}

// Input field 변경 시
['company-eps','company-bps','company-sps'].forEach(id => {
    document.getElementById(id)
        .addEventListener('input', updateValuation);
});

// 할인율 select/custom
document.getElementById('discount-rate')
    .addEventListener('change', updateValuation);
document.getElementById('discount-rate-custom')
    .addEventListener('input', updateValuation);

// 포함 체크박스
['choose-per','choose-psr','choose-pbr'].forEach(id => {
    document.getElementById(id)
        .addEventListener('change', updateValuation);
});



// 평균 계산 전용 함수
/**
 * 선택된(selectedTable) 테이블에서
 * 체크된 행의 PER, PSR, PBR 값을 읽어
 * 평균을 계산한 뒤 화면에 뿌려준다.
 */
function calculateAndDisplayAverages() {
    const tbody = document.querySelector('#selectedTable tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    const perList = [];
    const psrList = [];
    const pbrList = [];

    rows.forEach(tr => {
        const cb = tr.querySelector('input.include-checkbox');
        if (!cb || !cb.checked) return;
        const cells = tr.querySelectorAll('td');
        const per = parseFloat(cells[7].textContent.trim());
        const psr = parseFloat(cells[8].textContent.trim());
        const pbr = parseFloat(cells[9].textContent.trim());

    // PER 음수(<0)인 경우 제외
        if (!isNaN(per) && per > 0) perList.push(per);
        if (!isNaN(psr)) psrList.push(psr);
        if (!isNaN(pbr)) pbrList.push(pbr);
    });

    const mean = arr =>
        arr.length
            ? (arr.reduce((a,b) => a+b, 0) / arr.length).toFixed(2)
            : '-';

    document.getElementById('avg-per' ).textContent = mean(perList);
    document.getElementById('avg-psr').textContent = mean(psrList);
    document.getElementById('avg-pbr').textContent = mean(pbrList);

    updateValuation();
    updateLastSelectedCompanies();

}







// ① 툴팁용 실제 DOM 노드 하나만 body 에 추가
const tooltipBox = document.createElement('div');
tooltipBox.className = 'tooltip-box';
document.body.appendChild(tooltipBox);

// ② 툴팁 보이기/숨기기 함수
function showCoreTooltip(e) {
    const td = e.currentTarget;
    tooltipBox.textContent = td.textContent.trim();
    tooltipBox.style.display = 'block';
    const rect = td.getBoundingClientRect();
    tooltipBox.style.left = `${rect.left + window.scrollX + rect.width/2 - tooltipBox.offsetWidth/2}px`;
    tooltipBox.style.top  = `${rect.top + window.scrollY - tooltipBox.offsetHeight - 6}px`;
}
function hideCoreTooltip() {
    tooltipBox.style.display = 'none';
}


// DOM 참조
const keywordInput = document.getElementById('keywordInput');
const tagContainer = document.getElementById('tagContainer');

// 태그 렌더 함수
function renderTags() {
    tagContainer.innerHTML = '';
    main_product_keywords.forEach((kw, i) => {
        const span = document.createElement('span');
        span.className = 'tag';
        span.textContent = kw;
        span.addEventListener('click', () => {
            main_product_keywords.splice(i, 1);
            renderTags();
        });
        tagContainer.appendChild(span);
    });
}

// ③ initCoreSalesTooltip 함수 교체
function initCoreSalesTooltip() {
    document
        .querySelectorAll('#fsdataContainer td.core_sales, #selectedTable td.core_sales')
        .forEach(td => {
            td.removeEventListener('mouseenter', showCoreTooltip);
            td.removeEventListener('mouseleave', hideCoreTooltip);
            td.addEventListener('mouseenter', showCoreTooltip);
            td.addEventListener('mouseleave', hideCoreTooltip);
        });
}


// 콤마 입력 시 키워드 추가
keywordInput.addEventListener('keydown', e => {
    if (e.key === ',') {
        e.preventDefault();
        const val = keywordInput.value.trim();
        if (val) {
            main_product_keywords.push(val);
            renderTags();
            keywordInput.value = '';
        }
    }
});

// data-param 기반 쿼리스트링 생성
function buildQueryParams() {
    const params = new URLSearchParams();
    if (main_product_keywords.length) params.set('main_product_keywords', main_product_keywords.join(','));
    document.querySelectorAll('[data-param]').forEach(el => {
        const key = el.dataset.param;
        if (key === 'main_product_keywords') return;
        const val = el.value.trim();
        if (val) params.set(key, val);
    });
    return params.toString();
}

// 데이터 로드 및 저장
async function loadCategoryAndFsdata() {
    try {
        const qs = buildQueryParams();
        const url = window.location.origin + '/api/categoryandfsdata' + (qs ? `?${qs}` : '');
        const response = await fetch(url);
        if (!response.ok) throw new Error('결합된 데이터 로드 실패');
        lastData = await response.json();
        currentSort = { key: null, asc: true };
        renderTable();
    } catch (err) {
        alert(err.message);
    }
}

// 테이블 렌더링 및 정렬 (fsdataContainer)
// client.js

function renderTable() {
    const container = document.getElementById('fsdataContainer');
    if (!lastData.length) {
        container.innerHTML = '<p>검색 결과가 없습니다.</p>';
        return;
    }

    // 1) 데이터 복제 & 정렬
    const rows = [...lastData];
    if (currentSort.key) {
        rows.sort((a, b) => {
            let va = a[currentSort.key] ?? '';
            let vb = b[currentSort.key] ?? '';
            const na = parseFloat(va), nb = parseFloat(vb);
            if (!isNaN(na) && !isNaN(nb)) { va = na; vb = nb; }
            if (va < vb) return currentSort.asc ? -1 : 1;
            if (va > vb) return currentSort.asc ? 1 : -1;
            return 0;
        });
    }

    // 2) 컬럼 리스트 & HTML 생성
    const displayColumns = ['kap_group','company','sector','industry','main_product','core_sales','PER','PSR','PBR'];
    let html = '<table><thead><tr>';
    displayColumns.forEach(col => {
        html += `<th data-col="${col}">${col}</th>`;
    });
    html += '</tr></thead><tbody>';

    rows.forEach(r => {
        html += '<tr>';
        displayColumns.forEach(col => {
            if (col === 'core_sales') {
                html += `<td class="core_sales">${r[col] ?? ''}</td>`;
            } else {
                html += `<td>${r[col] ?? ''}</td>`;
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;

    // 3) 헤더 클릭 정렬 바인딩
    container.querySelectorAll('th[data-col]').forEach(th => {
        th.style.cursor = 'pointer';
        th.addEventListener('click', () => {
            const col = th.dataset.col;
            if (currentSort.key === col) currentSort.asc = !currentSort.asc;
            else { currentSort.key = col; currentSort.asc = true; }
            renderTable();
        });
    });

    // 4) core_sales 툴팁 초기화
    initCoreSalesTooltip();

// (renderTable 내부의) 5) 행 더블클릭 이벤트 바인딩 (중복 제거 버전)
    container.querySelectorAll('table tbody tr').forEach(tr => {
        tr.addEventListener('dblclick', () => {
            // 1) fsdataContainer 행의 셀값 배열
            const cells = Array.from(tr.cells).map(td => td.textContent.trim());
            const company = cells[1];  // fsdataContainer 에서는 1번 인덱스가 company

            // 2) selectedTable 에 이미 담긴 company 목록(3번째 열) 수집
            const existingCompanies = new Set(
                Array.from(
                    document.querySelectorAll('#selectedTable tbody tr td:nth-child(3)')
                ).map(td => td.textContent.trim())
            );

            // 3) 없을 때만 추가
            if (!existingCompanies.has(company)) {
                addToSelectedList(cells);
                enableSelectedTableSorting();
            }
        });
    });
}


// 정렬 기능 추가 (selectedTable)
function enableSelectedTableSorting() {
    const table = document.getElementById('selectedTable');
    const headers = table.querySelectorAll('th');
    headers.forEach((th, index) => {
        th.style.cursor = 'pointer';
        let asc = true;
        th.addEventListener('click', () => {
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[index].textContent.trim();
                const cellB = rowB.cells[index].textContent.trim();
                const numA = parseFloat(cellA), numB = parseFloat(cellB);
                let va = !isNaN(numA) ? numA : cellA;
                let vb = !isNaN(numB) ? numB : cellB;
                if (va < vb) return asc ? -1 : 1;
                if (va > vb) return asc ? 1 : -1;
                return 0;
            });
            asc = !asc;
            rows.forEach(r => tbody.appendChild(r));
        });
    });
}

// 옵션 로드 함수
async function loadGroupOptions() {
    const res = await fetch('/api/groupnames'); if (!res.ok) throw new Error('그룹명 로드 실패');
    const groups = await res.json(); const sel = document.getElementById('groupSelect');
    sel.innerHTML = '<option value="">--전체--</option>';
    groups.forEach(g => {
        const opt = document.createElement('option'); opt.value = g.group_name || g; opt.textContent = g.group_name || g; sel.appendChild(opt);
    });
}
async function loadSectorOptions() {
    const res = await fetch('/api/sectors'); if (!res.ok) throw new Error('섹터 로드 실패');
    const sectors = await res.json(); const sel = document.getElementById('sectorselect'); sel.innerHTML = '<option value="">--전체--</option>';
    sectors.forEach(s => { const opt = document.createElement('option'); opt.value = s; opt.textContent = s; sel.appendChild(opt); });
}
async function loadIndustryOptions() {
    const res = await fetch('/api/industries'); if (!res.ok) throw new Error('업종 로드 실패');
    const inds = await res.json(); const sel = document.getElementById('industryselect'); sel.innerHTML = '<option value="">--전체--</option>';
    inds.forEach(i => { const opt = document.createElement('option'); opt.value = i; opt.textContent = i; sel.appendChild(opt); });
}
async function loadGroupStats() {
    const res = await fetch('/api/groupstats'); if (!res.ok) throw new Error('그룹 통계 로드 실패');
    const stats = await res.json(); const container = document.getElementById('group-stats-container');
    let html = '<table><thead><tr>' + Object.keys(stats[0]).map(k => `<th>${k}</th>`).join('') + '</tr></thead><tbody>';
    stats.forEach(r => { html += '<tr>' + Object.values(r).map(v => `<td>${v}</td>`).join('') + '</tr>'; });
    html += '</tbody></table>'; container.innerHTML = html;
}

// 선택 리스트에 행 추가
function addToSelectedList(values) {
    const tbody = document.querySelector('#selectedTable tbody');
    const tr = document.createElement('tr');

    // 1) 체크박스 셀
    const tdCheck = document.createElement('td');
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.className = 'include-checkbox';
    // 체크 상태가 바뀔 때마다 평균 재계산
    cb.addEventListener('change', calculateAndDisplayAverages);
    tdCheck.appendChild(cb);
    tr.appendChild(tdCheck);

    // 2) 값들 셀
    values.forEach((t, idx) => {
        const td = document.createElement('td');
        td.textContent = t;

        // core_sales 컬럼(6번째 칸, idx===5)에만 클래스 붙이기
        if (idx === 5) {
            td.classList.add('core_sales');
        }

        tr.appendChild(td);
    });

    // 3) tbody에 tr 추가
    tbody.appendChild(tr);

    // ── 행 클릭 시 체크박스 토글 ──
    tr.addEventListener('click', () => {
        const cb = tr.querySelector('input.include-checkbox');
        if (!cb) return;
        cb.checked = !cb.checked;
        calculateAndDisplayAverages();
        updateLastSelectedCompanies();  // 3)번에서 만들 함수 호출
    });


    // 4) 새로 추가된 core_sales 셀에 tooltip 속성 붙이기
    initCoreSalesTooltip();
    calculateAndDisplayAverages();
}


// 이벤트 바인딩
['groupSelect','sectorselect','industryselect'].forEach(id =>
    document.getElementById(id).addEventListener('change', loadCategoryAndFsdata)
);
document.getElementById('searchBtn').addEventListener('click', loadCategoryAndFsdata);
document.getElementById('keywordBtn').addEventListener('click', loadCategoryAndFsdata);

// 전체 복사
const selectAllBtn = document.getElementById('select-all-displayed');
selectAllBtn.addEventListener('click', () => {
    // 1) 이미 selectedTable에 들어있는 company(3번째 열) 집합 생성
    const existing = new Set(
        Array.from(
            document.querySelectorAll('#selectedTable tbody tr td:nth-child(3)')
        ).map(td => td.textContent.trim())
    );

    // 2) fsdataContainer의 모든 행을 순회하며,
    //    cells[1] (company) 가 existing에 없으면 추가
    document
        .querySelectorAll('#fsdataContainer table tbody tr')
        .forEach(tr => {
            // fsdataContainer 쪽엔 체크박스가 없으니 cells[1]이 company!
            const cells = Array.from(tr.cells).map(td => td.textContent.trim());
            const company = cells[1];  // ← 여기 인덱스를 1로 바꿨습니다
            if (!existing.has(company)) {
                addToSelectedList(cells);
                existing.add(company);
            }
        });

    // 3) 정렬 기능 재활성화
    enableSelectedTableSorting();

    calculateAndDisplayAverages();
});


// 박스 초기화
const resetBtn = document.getElementById('list-reset');
resetBtn.addEventListener('click', () => {
    document.querySelector('#selectedTable tbody').innerHTML='';

    calculateAndDisplayAverages();
});







// 초기 로드
loadCategoryAndFsdata();
loadGroupOptions();
loadSectorOptions();
loadIndustryOptions();
loadGroupStats();
enableSelectedTableSorting();
