// app.js
// Importa os módulos necessários
const express = require('express');
const mysql = require('mysql');
const bodyParser = require('body-parser');
const path = require('path');

// Inicializa o aplicativo Express
const app = express();

// Configura a porta do servidor
const PORT = process.env.PORT || 3000;

// Middleware para processamento de JSON
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Configura o banco de dados MySQL
const db = mysql.createConnection({
    host: 'localhost',
    user: 'seu_usuario',
    password: 'sua_senha',
    database: 'service_platform'
});

// Conecta ao banco de dados
db.connect((err) => {
    if (err) throw err;
    console.log('Conectado ao banco de dados MySQL');
});

// Define a rota inicial
app.get('/', (req, res) => {
    res.send('Bem-vindo à Plataforma de Serviços Online');
});

// Rota para listar todos os prestadores
app.get('/prestadores', (req, res) => {
    const sql = 'SELECT * FROM providers';
    db.query(sql, (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

// Rota para listar todos os clientes
app.get('/clientes', (req, res) => {
    const sql = 'SELECT * FROM clients';
    db.query(sql, (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

// Rota para buscar prestadores por nome ou especialidade
app.get('/prestadores/busca', (req, res) => {
    const { nome, especialidade } = req.query;
    let sql = 'SELECT * FROM providers WHERE 1=1';
    if (nome) sql += ` AND full_name LIKE '%${nome}%'`;
    if (especialidade) sql += ` AND specialty LIKE '%${especialidade}%'`;

    db.query(sql, (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

// Rota para cadastro de prestadores
app.post('/cadastro/prestador', (req, res) => {
    const { nome, especialidade, descricao, email, telefone } = req.body;
    const sql = 'INSERT INTO providers (full_name, specialty, description, email, phone) VALUES (?, ?, ?, ?, ?)';
    db.query(sql, [nome, especialidade, descricao, email, telefone], (err, result) => {
        if (err) throw err;
        res.json({ message: 'Prestador cadastrado com sucesso!' });
    });
});

// Rota para cadastro de clientes
app.post('/cadastro/cliente', (req, res) => {
    const { nome, preferencias, email, telefone } = req.body;
    const sql = 'INSERT INTO clients (full_name, preferences, email, phone) VALUES (?, ?, ?, ?)';
    db.query(sql, [nome, preferencias, email, telefone], (err, result) => {
        if (err) throw err;
        res.json({ message: 'Cliente cadastrado com sucesso!' });
    });
});

// Rota simulada para videoconferência (para integração futura com Twilio ou WebRTC)
app.get('/video/:id', (req, res) => {
    const { id } = req.params;
    res.send(`Videoconferência em andamento com o ID: ${id}`);
});

// Servindo arquivos estáticos (CSS, JS, imagens) a partir da pasta 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Inicializa o servidor
app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});
