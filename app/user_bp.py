from flask import Blueprint, render_template, request, redirect, url_for, flash


user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['POST', 'GET'])
def user():
    return render_template('perfil.html')

@user_bp.route('/veiculos')
def veiculos():
    return render_template('veiculos.html')

@user_bp.route('/veiculos_logged')
def veiculos_logged():
    return render_template('veiculos_logged.html')

