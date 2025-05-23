
// 1. 서버 초기화 & 미들웨어
const express = require('express')
const cors = require('cors')
const mysql = require('mysql2/promise') // promise 기반 사용 권장
const app = express()
const iconv = require('iconv-lite');

// CORS 설정
app.use(cors());
app.use(express.static(__dirname));


function decodeRow(row) {
    const out = {};
    for (const [key, val] of Object.entries(row)) {
        // val이 버퍼면 euc-kr로 디코딩, 아니면 그대로
        if (Buffer.isBuffer(val)) {
            out[key] = iconv.decode(val, 'euc-kr');
        } else {
            out[key] = val;
        }
    }
    return out;
}


// 1) MySql 연결 풀 생성 시 charset 지정
const pool = mysql.createPool({
    host:              '115.68.219.19',
    port:              3306,
    user:              'dwchae23',
    password:          'koreaap!123',
    database:          'dwchae23',     // ← 본인 스키마
    waitForConnections: true,
    connectionLimit:    10,
    charset:  'euckr',   // ← 여기를 추가!
    queueLimit:         0
});

// 3. API 라우터
app.get('/', function(requests, response){
    response.sendFile(__dirname +'/index.html')
})

app.get('/api/category_company', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM category_company');
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('category_company 데이터 조회 중 오류 발생');
    }
});

app.get('/api/fsdata', async (req, res) => {
    try {
        const company = req.query.company;
        let sql = 'SELECT * FROM fsdata';
        let params = [];
        if (company) {
            sql += ' WHERE ticker LIKE ?';
            params.push(`%${company}%`);
        }
        const [rows] = await pool.query(sql, params);
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('fsdata 데이터 조회 중 오류 발생');
    }
});



app.get('/api/price_long', async (req, res) => {
    try {
        const [rows] = await pool.query('SELECT * FROM price_long');
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('price_long 데이터 조회 중 오류 발생');
    }
});

app.get('/api/categoryandfsdata', async (req, res) => {
    try {
        let sql = `
            SELECT
                f.ticker             AS company,
                f.avg_price      AS avg_price,
                f.PER, f.PSR, f.PBR,
                f.EPS, f.SPS, f.BPS,
                c.sector,
                c.industry,
                c.industry_group     AS industry_group,
                c.kap_group,
                c.main_product,
                c.core_sales
            FROM fsdata AS f
                     INNER JOIN category_company AS c
                                ON f.ticker = c.ticker
        `;
        const params = [];

        if (req.query.ticker) {
            sql += ' WHERE f.ticker LIKE ?';
            params.push(`%${req.query.ticker}%`);
        }
        if (req.query.group) {
            sql += (params.length ? ' AND ' : ' WHERE ') + 'c.kap_group = ?';
            params.push(req.query.group);
        }

        // 필터: sector
        if (req.query.sector) {
            sql += (params.length ? ' AND ' : ' WHERE ') + 'c.sector = ?';
            params.push(req.query.sector);
        }

        // 필터: industry
        if (req.query.industry) {
            sql += (params.length ? ' AND ' : ' WHERE ') + 'c.industry = ?';
            params.push(req.query.industry);
        }

        // main_product_keywords(주요상품) 다중 키워드 검색 필터
        if (req.query.main_product_keywords) {
            const keywords = req.query.main_product_keywords
                .split(',')
                .map(k => k.trim())
                .filter(k => k);
            const pattern = keywords.join('|');
            sql += (params.length ? ' AND ' : ' WHERE ') + 'c.main_product REGEXP ?';
            params.push(pattern);
        }

        // 1) 쿼리 실행
        const [rows] = await pool.query(sql, params);
        // 2) euc-kr Buffer → UTF-8 문자열로 변환
        const decoded = rows.map(decodeRow);
        // 3) JSON 응답
        res.json(decoded);

    } catch (error) {
        console.error(error);
        res.status(500).send('테이블 결합 데이터 조회 중 오류 발생');
    }
});


// unique 그룹명 목록 가져오기
app.get('/api/groupnames', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT DISTINCT kap_group AS group_name
             FROM category_company
             ORDER BY kap_group`
        );
        res.json(rows);
    } catch (err) {
        console.error(err);
        res.status(500).send('그룹명 조회 중 오류 발생');
    }
});

// unique 섹터 목록 가져오기
app.get('/api/sectors', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT DISTINCT sector
         FROM category_company
        ORDER BY sector`
        );
        // rows는 [{ sector: '금융' }, { sector: '소비재' }, …]
        res.json(rows.map(r => r.sector));
    } catch (err) {
        console.error(err);
        res.status(500).send('섹터 목록 조회 중 오류 발생');
    }
});

// unique 업종 목록 가져오기
app.get('/api/industries', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT DISTINCT industry
         FROM category_company
        ORDER BY industry`
        );
        res.json(rows.map(r => r.industry));
    } catch (err) {
        console.error(err);
        res.status(500).send('업종 목록 조회 중 오류 발생');
    }
});





// 통계데이터(1) API
app.get('/api/groupstats', async (req, res) => {
    const sql = `SELECT
    c.kap_group,
    COUNT(*) AS 기업수,
    GROUP_CONCAT(
    c.ticker
    ORDER BY c.ticker
    SEPARATOR ', ' ) AS 기업목록,
        round(avg(f.psr), 2) AS PSR평균,
        min(f.psr) AS PSR최소,
        max(f.psr) AS PSR최대,
        round(stddev_pop(f.psr),2) AS PSR표준편차,
        round(avg(f.pbr), 2) AS PBR평균,
        min(f.pbr) AS PBR최소,
        max(f.pbr) AS PBR최대,
        round(stddev_pop(f.pbr), 2) AS PBR표준편차
    FROM dwchae23.category_company AS c
    LEFT JOIN dwchae23.fsdata AS f
    ON c.ticker = f.ticker
    GROUP BY c.kap_group ORDER BY 기업수 DESC`;

    try {
        const [rows] = await pool.query(sql);
        res.json(rows);
    } catch (err) {
        console.error(err);
        res.status(500).send('그룹 통계 데이터 조회 중 오류 발생');
    }
});





// 4. 서버 기동
app.listen(8080, () => {
    console.log('http://localhost:8080 에서 서버 실행중')
})
