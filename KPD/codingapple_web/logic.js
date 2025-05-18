const evalSelect = document.getElementById("eval-date");
const multipleSelect = document.getElementById("multiple-date");

// 평가기준일 -> 배수기준일 리스트 매핑
const 기준일맵 = {
    "2024-12-31": ["2024-05-31 ~ 2025-10-31", "2024-07-31 ~ 2024-12-31"],
    "2025-03-31": ["2024-08-31 ~ 2025-01-31", "2024-10-31 ~ 2025-03-31"],
    "2025-06-30": ["2024-11-30 ~ 2025-04-30", "2025-01-31 ~ 2025-06-30"],
    "2025-09-30": ["2024-02-28 ~ 2025-07-31", "2025-04-30 ~ 2025-09-30"],
    "2025-12-31": ["2024-05-31 ~ 2025-10-31", "2025-07-30 ~ 2025-12-31"]
};

// 이벤트 핸들러 : 평가기준일이 바꾸리 때마다 배수기준일 목록 갱신
evalSelect.addEventListener("change", function () {
    const 선택값 = this.value;

    // 기존 옵션 초기화
    multipleSelect.innerHTML = '<option value="">--선택 --</option>';

    // 선택한 기준일에 따라 새로운 옵션 삽입
    if (기준일맵[선택값]) {
        기준일맵[선택값].forEach(function (기간) {
            const option = document.createElement("option");
            option.value = 기간;
            option.textContent = 기간;
            multipleSelect.appendChild(option);

        });
    }
});

