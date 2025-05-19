
// 1. 서버 초기화 & 미들웨어
const express = require('express')
const mysql = require('mysql2/promise') // promise 기반 사용 권장
const app = express()

// 정적 파일 서비스 루트 지정 //
app.use(express.static(__dirname));


// 2. 데이터베이스 풀 생성
// mysql 연결 풀 만들기 //
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'coehddn!0104',
    database: 'price',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
}) ;




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
        f.ticker AS 종목명,
        f.평균주가        AS 평균주가,
        f.PER            AS PER,
        f.PSR            AS PSR,
        f.PBR            AS PBR,
        f.EPS            AS EPS,
        f.SPS            AS SPS,
        f.BPS            AS BPS,
        c.대분류          AS 대분류,
        c.중분류          AS 중분류,
        c.\`11차표준(세분류)\`           AS 세분류,
        c.\`그룹명\`        AS 그룹명,
        c.\`주요상품 및 서비스\`      AS 주요상품,
        c.\`매출비율\`       AS 매출비율
      FROM price.fsdata AS f
      INNER JOIN price.category AS c
        ON f.ticker = c.\`기업명\` `;
        const params = [];
        // 2) 검색어가 넘어오면 WHERE절 추가
        if (req.query.ticker) {
            sql += ' WHERE f.ticker LIKE ?';
            params.push(`%${req.query.ticker}%`);
        }

        // 그룹명 필터
        if (req.query.group) {
            sql += (params.length ? ' AND ' : ' WHERE ') + `c.\`그룹명\` = ?`;
            params.push(req.query.group)
        }

        // 3) 실행 및 반환
        const [rows] = await pool.query(sql, params);
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).send('테이블 결합 데이터 조회 중 오류 발생');
    }
});


// unique 그룹명 목록 가져오기
app.get('/api/groupnames', async (req, res) => {
    try {
        const [rows] = await pool.query(
            `SELECT DISTINCT \`그룹명\` AS group_name
             FROM price.category
             ORDER BY \`그룹명\``
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
