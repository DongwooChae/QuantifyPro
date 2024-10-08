SELECT
	코멘트,
    평가의뢰기관,
    평가의뢰종목,
	평가종류,
    strftime('%Y-%m-%d', 기준일) AS 기준일,
    strftime('%Y-%m-%d', 평가값송부일) AS 평가값송부일,
    strftime('%Y-%m-%d', 보고서송부일) AS 보고서송부일,
    평가담당자,
    RM,
	공수,
    구분,
	printf('%,d', `보유주식수`) AS `보유주식수`,
    printf('%,d', `주당단가`) AS `주당단가`,
	printf('%,d', `투자금액`) AS `투자금액`,
    printf('%,d', `평가금액`) AS `평가금액`,
	평가여부
	
From 종목관리대장
WHERE 평가담당자 = "채동우"
	AND 보고서송부일 > DATE('now', '-1 day')
	AND 기준일 = "2024-09-30"
	ORDER BY 보고서송부일 asc;