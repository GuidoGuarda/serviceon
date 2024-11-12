from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from services.video_service import create_video_room, generate_access_token
import os
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://username:senai@123/saas_plataform")

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

app.config['TWILIO_ACCOUNT_SID'] = 'your_account_sid'
app.config['TWILIO_AUTH_TOKEN'] = 'your_auth_token'

class Provider(db.Model):
    __tablename__ = 'providers'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    preferences = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html', title='Página Inicial')

@app.route('/prestador', methods=['GET', 'POST'])
def prestador():
    if request.method == 'POST':
        full_name = request.form['full_name']
        specialty = request.form['specialty']
        description = request.form['description']
        email = request.form['email']
        phone = request.form['phone']

        novo_prestador = Provider(
            full_name=full_name,
            specialty=specialty,
            description=description,
            email=email,
            phone=phone
        )

        try:
            db.session.add(novo_prestador)
            db.session.commit()
            flash("Prestador cadastrado com sucesso!", "success")
            return redirect(url_for('listar_prestadores'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao cadastrar prestador: " + str(e), "danger")

    return render_template('cadastro_prestador.html', tipo='prestador', title='Cadastro de Prestador')

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
        full_name = request.form['full_name']
        preferences = request.form['preferences']
        email = request.form['email']
        phone = request.form['phone']

        novo_cliente = Client(
            full_name=full_name,
            preferences=preferences,
            email=email,
            phone=phone
        )

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            flash("Cliente cadastrado com sucesso!", "success")
            return redirect(url_for('listar_clientes'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao cadastrar cliente: " + str(e), "danger")

    return render_template('cadastro_cliente.html', tipo='cliente', title='Cadastro de Cliente')

@app.route('/listar_prestadores')
def listar_prestadores():
    prestadores = Provider.query.all()
    return render_template('listar_prestadores.html', prestadores=prestadores, title='Lista de Prestadores')

@app.route('/listar_clientes')
def listar_clientes():
    clientes = Client.query.all()
    return render_template('listar_clientes.html', clientes=clientes, title='Lista de Clientes')

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    if request.method == 'POST':
        termo = request.form['termo']
        tipo = request.form['tipo']

        if tipo == 'prestador':
            resultados = Provider.query.filter(Provider.full_name.contains(termo)).all()
            return render_template('search_results.html', resultados=resultados, tipo=tipo)
        else:
            resultados = Client.query.filter(Client.full_name.contains(termo)).all()
            return render_template('search_results.html', resultados=resultados, tipo=tipo)

    return render_template('pesquisa.html', title='Pesquisa de Cadastro')

@app.route('/create-room', methods=['POST'])
def create_room():
    room_name = request.form['room_name']
    room = create_video_room(room_name)
    if room:
        return render_template('room_created.html', room_name=room_name)
    return "Erro ao criar sala!"

@app.route('/generate-token', methods=['GET'])
def generate_token():
    room_name = request.args.get('room_name')
    user_name = request.args.get('user_name')
    token = generate_access_token(room_name, user_name)
    if token:
        return render_template('video_conference.html', token=token)
    return "Erro ao gerar token"

@app.route('/video/<int:id>')
def video(id):
    return render_template('video.html', title='Videoconferência', id=id)

if __name__ == '__main__':
    app.run(debug=True)
