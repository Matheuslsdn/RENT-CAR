from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from app.models import Usuario, Veiculo, Reserva
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os

bp = Blueprint('home', __name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Cria a pasta de uploads, se não existir
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()
        
        if not usuario:
            flash('Usuário não encontrado.', 'error')
            return redirect(url_for('home.login'))

        if usuario and usuario.check_senha(senha):
            session['user_id'] = usuario.id  # Armazena o ID do usuário na sessão
            flash('Login bem-sucedido!', 'success')
            return render_template('index_logged.html')
        else:
            flash('Credenciais inválidas, tente novamente.', 'danger')

    return render_template('login.html')

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('home.cadastro'))

        # Verifique se o email já existe
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado. Tente outro.', 'error')
            return redirect(url_for('home.cadastro'))

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('home.login'))

@bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu com sucesso!', 'success')
    return redirect(url_for('home.index'))

@bp.route('/excluir_usuario/<int:usuario_id>', methods=['GET', 'POST'])
def excluir_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        flash('Usuário não encontrado.')
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!')
        return redirect(url_for('home.index'))

    return render_template('confirmar_exclusao.html', usuario=usuario)

@bp.route('/cad_veiculo', methods=['GET', 'POST'])
def cad_veiculo():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        modelo = request.form['modelo']
        categoria = request.form['categoria']
        
        try:
            ano_str = request.form['ano']
            ano = datetime.strptime(ano_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de ano inválido. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('home.cad_veiculo'))
        
        preco_dia = float(request.form['preco_dia'])
        disponibilidade = request.form['disponibilidade']
        placa = request.form['placa']
        imagem = request.files.get('imagem')

        if not all([nome, marca, modelo, categoria, ano, preco_dia, disponibilidade, placa]):
            flash('Preencha todos os campos.', 'error')
            return redirect(url_for('home.cad_veiculo'))

        if Veiculo.query.filter_by(placa=placa).first():
            flash('Placa já cadastrada.', 'error')
            return redirect(url_for('home.cad_veiculo'))

        novo_veiculo = Veiculo(
            nome=nome,
            marca=marca,
            modelo=modelo,
            categoria=categoria,
            ano=ano,
            preco_dia=preco_dia,
            disponibilidade=disponibilidade,
            placa=placa
        )
        
        if imagem and allowed_file(imagem.filename):  # Verifica se há imagem e se ela é válida
            filename = secure_filename(imagem.filename)
            filepath = os.path.join('app/static/uploads', filename)
            imagem.save(filepath)  # Salva a imagem no diretório `static/uploads`
            novo_veiculo.imagem = filename  # Armazena apenas o nome do arquivo no banco de dados

        try:
            db.session.add(novo_veiculo)
            db.session.commit()
            flash('Veículo cadastrado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar veículo: {str(e)}', 'error')
            return redirect(url_for('home.cad_veiculo'))

        return redirect(url_for('home.index'))

    return render_template('cad_veiculo.html')

@bp.route('/deletar_veiculo/<int:id>', methods=['POST'])
def deletar_veiculo(id):
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para acessar essa página.', 'error')
        return redirect(url_for('home.login'))

    veiculo = Veiculo.query.get(id)
    
    if not veiculo:
        flash('Veículo não encontrado.', 'error')
        return redirect(url_for('home.index_logged'))

    try:
        db.session.delete(veiculo)
        db.session.commit()
        flash('Veículo deletado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao deletar veículo: {str(e)}', 'error')

    return redirect(url_for('home.cad_veiculo'))

@bp.route('/listar_veiculos', methods=['GET'])
def listar_veiculos():
    veiculos = Veiculo.query.all()
    return render_template('listar_veiculos.html', veiculos=veiculos)

@bp.route('/reservar_veiculo/<int:veiculo_id>', methods=['GET', 'POST'])
def reservar_veiculo(veiculo_id):
    # Verifica se o usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para reservar um veículo.', 'error')
        return redirect(url_for('home.login'))

    veiculo = Veiculo.query.get(veiculo_id)

    if request.method == 'POST':
        data_inicio = request.form['data_inicio']
        data_fim = request.form['data_fim']

        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

            if data_inicio >= data_fim:
                flash('A data de início deve ser anterior à data de fim.', 'error')
                return redirect(url_for('home.reservar_veiculo', veiculo_id=veiculo_id))

            # Verifica se o veículo já está reservado nesse período
            if Reserva.query.filter(
                Reserva.veiculo_id == veiculo_id,
                Reserva.data_inicio < data_fim,
                Reserva.data_fim > data_inicio
            ).first():
                flash('O veículo já está reservado nesse período.', 'error')
                return redirect(url_for('home.reservar_veiculo', veiculo_id=veiculo_id))

            # Cria a reserva
            nova_reserva = Reserva(
                veiculo_id=veiculo_id,
                usuario_id=session.get('user_id'),  # ID do usuário logado
                data_inicio=data_inicio,
                data_fim=data_fim
            )

            db.session.add(nova_reserva)
            db.session.commit()
            flash('Reserva realizada com sucesso!', 'success')
            return redirect(url_for('home.index'))

        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD.', 'error')
            return redirect(url_for('home.reservar_veiculo', veiculo_id=veiculo_id))

    return render_template('reservar_veiculo.html', veiculo=veiculo)

@bp.route('/alugar_logged')
def alugar_logged():
    # Consulta todos os veículos do banco de dados
    veiculos = Veiculo.query.all()

    # Renderiza a página 'alugar_logged.html' passando a lista de veículos
    return render_template('alugar_logged.html', veiculos=veiculos)