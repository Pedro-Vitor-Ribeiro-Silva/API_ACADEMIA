import os,json
import firebase_admin
from flask import Flask,jsonify,request
from flask_cors import CORS
from firebase_admin import credentials,firestore
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

FBKEY=json.loads(os.getenv('CONFIG_FIREBASE'))

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

db = firestore.client() #conecta ao db do firebase


@app.route('/')
def index():
    return jsonify({'mensagem':'API ON'}), 200


@app.route('/gym', methods=['GET'])
def listUser():
    usuarios = []

    lista = db.collection('usuarios').stream()

    for item in lista:
        usuarios.append(item.to_dict())

    if usuarios:
        return jsonify(usuarios),200
    else:
        return jsonify({'mensagem':'ERRO! Nenhum usuario cadastrado'}), 404
    
@app.route('/gym/user/id/<int:id>', methods=['GET'])
def selectUser(id):
    doc = db.collection('usuarios').document(str(id)).get()
    if doc.exists:
        return jsonify(doc.to_dict()), 200
    else:
        return jsonify({'mensagem': f'Usuário com id {id} não encontrado'}), 404

@app.route('/gym/user/cpf/<cpf>', methods=['GET'])
def selectCpfUser(cpf):
    resultado = db.collection('usuarios').where('cpf', '==', cpf).stream()
    for doc in resultado:
        return jsonify(doc.to_dict()), 200
    return jsonify({'mensagem': f'Usuário com CPF {cpf} não encontrado'}), 404
    
@app.route('/gym', methods=['POST'])
def createUser():
    usuario_dados=request.json

    if 'cpf' not in usuario_dados or 'nome' not in usuario_dados or 'status' not in usuario_dados:
        return jsonify({'mensagem':'ERRO! Campos nome, cpf e status são obrigatórios'}), 400
    
    cpf = str(usuario_dados['cpf'])

    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({'mensagem': 'ERRO! CPF deve conter 11 dígitos numéricos'}), 400

    if not isinstance(usuario_dados['status'], bool):
        return jsonify({'mensagem': 'ERRO! O campo status deve ser true ou false (booleano)'}), 400

    cpf_existente = db.collection('usuarios').where('cpf', '==', cpf).stream()
    if any(cpf_existente): 
        return jsonify({'mensagem': f'ERRO! Usuário com CPF {cpf} já existe'}), 409


    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id= contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id':novo_id})

    doc_ref = db.collection('usuarios').document(str(novo_id))
    doc_ref.set({
        'id': novo_id,
        'cpf': cpf,
        'nome': usuario_dados['nome'],
        'status': usuario_dados['status']
    })

    return jsonify({'mensagem': f'Usuário {usuario_dados["nome"]} cadastrado com sucesso', 'id': novo_id}), 201


@app.route('/gym/user/<int:id>', methods=['PUT'])
def editUser(id):
    usuario_dados = request.json

    cpf = str(usuario_dados['cpf'])

    if 'cpf' not in usuario_dados or 'nome' not in usuario_dados or 'status' not in usuario_dados:
        return jsonify({'mensagem':'ERRO! Campos nome, cpf e status são obrigatórios'}), 400
    
    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({'mensagem': 'ERRO! CPF deve conter 11 dígitos numéricos'}), 400
    
    if not isinstance(usuario_dados['status'], bool):
        return jsonify({'mensagem': 'ERRO! O campo status deve ser true ou false (booleano)'}), 400
    
    usuarios = db.collection('usuarios').where('cpf', '==', cpf).stream()
    for u in usuarios:
        if u.to_dict().get('id') != id:
            return jsonify({'mensagem': f'ERRO! CPF {cpf} já está sendo usado por outro usuário'}), 409

    doc_ref = db.collection('usuarios').document(str(id))
    doc = doc_ref.get()

    if doc.exists:
        doc_ref.update({
            'cpf': usuario_dados['cpf'],
            'nome': usuario_dados['nome'],
            'status': usuario_dados['status']
        })
        return jsonify({'mensagem':'Usuário atualizado com sucesso!'}), 200
    else:
        return jsonify({'mensagem':'ERRO! Usuário não encontrado!'}), 404



@app.route('/gym/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    doc_ref = db.collection('usuarios').document(str(id))
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem': 'ERRO! Usuário não encontrado!'}), 404

    doc_ref.delete()
    return jsonify({'mensagem': 'Usuário excluído com sucesso!'}), 200


if __name__ == '__main__':
    app.run()