
// 1. 서버 초기화 & 미들웨어
const express = require('express')
const cors = require('cors')
const mysql = require('mysql2/promise') // promise 기반 사용 권장
const app = express()
const iconv = require('iconv-lite');

// CORS 설정 - cafe24 도메인만 허용
app.use(cors());

app.use(express.static(__dirname))


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



// 정적 파일 서비스 루트 지정 //
app.use(express.static(__dirname));


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

// const pool = mysql.createPool({
//     host: 'localhost',
//     user: 'root',
//     password: 'coehddn!0104',
//     database: 'price',
//     waitForConnections: true,
//     connectionLimit: 10,
//     queueLimit: 0
// }) ;


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





// 4. 서버 기동
app.listen(8080, () => {
    console.log('http://localhost:8080 에서 서버 실행중')
})
