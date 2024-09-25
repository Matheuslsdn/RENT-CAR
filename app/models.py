from app import db 
from werkzeug.security import generate_password_hash, check_password_hash

#Modelo de criação de Usuário 

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    senha_hash = db.Column(db.String(128), nullable=False)

    def set_senha(self, senha):
        """Define a senha com segurança usando um hash"""
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.id}: {self.nome} ({self.email})>"
    
#Modelo do veiculo
class Veiculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    marca = db.Column(db.String(20), nullable=False)
    modelo =db.Column(db.String(20), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    ano = db.Column(db.Date, nullable=False)
    preco_dia = db.Column(db.Float, nullable=False)
    disponibilidade = db.Column(db.String(20), nullable=False)
    placa = db.Column(db.String(20), unique=True, nullable=False)
    imagem = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<veiculo> {self.nome}'

#Modelo de reserva
class Reserva(db.Model):
    __tablename__ = 'reservas'
    id = db.Column(db.Integer, primary_key=True)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculo.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Supondo que você tenha um modelo de usuário
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)

    veiculo = db.relationship('Veiculo', backref='reservas')
    usuario = db.relationship('Usuario', backref='reservas')


# class manutencao(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     veiculo =  db.Column(db.String(20), db.ForeignKey('veiculo.id'))
#     descricao = db.Column(db.Text, nullable=False)
#     dataEntrada = db.Column(db.Date, nullable=False)
#     dataSaida = db.Column(db.Date, nullable=False)
    
#     def __repr__(self):
#         return f'<manutencao> {self.veiculo}'

    
# class dados_pessoais(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nome = db.Column(db.String(50), nullable=False)
#     senha = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     endereco = db.Column(db.String(50), nullable=False)
#     data_nascimento = db.Column(db.Date, nullable=False)
#     rg = db.Column(db.String(12), unique=True, nullable=False)
#     cpf = db.Column(db.String(14), unique=True, nullable=False)
#     telefone = db.Column(db.String(20), unique=True, nullable=False)
    
#     def __repr__(self):
#         return f'<dados_pessoais> {self.id_usuario}'
    

    
    
    