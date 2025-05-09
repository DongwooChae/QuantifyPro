// server.js
const express = require('express');
const cors    = require('cors');
const mysql   = require('mysql2/promise');

const app = express();
app.use(cors());

const pool = mysql.createPool({
  host:     'localhost',
  user:     'YOUR_DB_USER',
  password: 'YOUR_DB_PASS',
  database: 'YOUR_DB_NAME',
  waitForConnections: true,
  connectionLimit: 10
});

app.get('/api/companies', async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM company');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'DB 조회 실패' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`API 서버 실행: http://localhost:${PORT}`);
});
