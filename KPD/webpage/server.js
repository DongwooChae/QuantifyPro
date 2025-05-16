const express = require('express')
const mysql = require('mysql2/promise') // promise 기반 사용 권장

const app = express()

// 정적 파일 서비스 루트 지정 //
app.use(express.static(__dirname));

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




// app.get('/', (requests, response)=>{
//     response.send('서버에 성공적으로 접속하였습니다.')
// })

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



app.listen(8080, () => {
    console.log('http://localhost:8080 에서 서버 실행중')
})
