from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader
from cloudinary.uploader import destroy

import os,json
import firebase_admin
from flask import Flask,jsonify,request
from flask_cors import CORS
from firebase_admin import credentials,firestore


cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET") 

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret,
    secure=True,
)


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
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    imagem = request.files.get('imagem')

    if not nome or not cpf:
        return jsonify({'mensagem': 'ERRO! Campos nome e cpf são obrigatórios'}), 400

    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({'mensagem': 'ERRO! CPF deve conter 11 dígitos numéricos'}), 400

    cpf_existente = db.collection('usuarios').where('cpf', '==', cpf).stream()
    if any(cpf_existente): 
        return jsonify({'mensagem': f'ERRO! Usuário com CPF {cpf} já existe'}), 409

    imagem_url = None
    public_id = None

    # Upload da imagem
    if imagem:
        upload_result = cloudinary.uploader.upload(imagem)
        print(upload_result['public_id'])
        imagem_url = upload_result['secure_url']
        public_id = upload_result['public_id']        

    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id})

    doc_ref = db.collection('usuarios').document(str(novo_id))
    doc_ref.set({
        'id': novo_id,
        'cpf': cpf,
        'nome': nome,
        'status': True,
        'imagem_url': imagem_url,
        'public_id': public_id
    })

    return jsonify({'mensagem': f'Usuário {nome} cadastrado com sucesso', 'id': novo_id}), 201


@app.route('/gym/user/<int:id>', methods=['PUT'])
def editUser(id):
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    status = request.form.get('status')
    imagem = request.files.get('imagem')

    if not nome or not cpf or status is None:
        return jsonify({'mensagem': 'ERRO! Campos nome, cpf e status são obrigatórios'}), 400

    if not cpf.isdigit() or len(cpf) != 11:
        return jsonify({'mensagem': 'ERRO! CPF deve conter 11 dígitos numéricos'}), 400

    if status.lower() not in ['true', 'false']:
        return jsonify({'mensagem': 'ERRO! O campo status deve ser true ou false (booleano)'}), 400

    status_bool = status.lower() == 'true'

    usuarios = db.collection('usuarios').where('cpf', '==', cpf).stream()
    for u in usuarios:
        if u.to_dict().get('id') != id:
            return jsonify({'mensagem': f'ERRO! CPF {cpf} já está sendo usado por outro usuário'}), 409

    doc_ref = db.collection('usuarios').document(str(id))
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem': 'ERRO! Usuário não encontrado!'}), 404

    dados_antigos = doc.to_dict()

    imagem_url = dados_antigos.get('imagem_url')
    public_id = dados_antigos.get('public_id')

    if imagem:
        if public_id:
            try:
                destroy(public_id)
            except Exception as e:
                print("Erro ao deletar imagem antiga:", e)

        novo_upload = cloudinary.uploader.upload(imagem)
        imagem_url = novo_upload['secure_url']
        public_id = novo_upload['public_id']

    doc_ref.update({
        'nome': nome,
        'cpf': cpf,
        'status': status_bool,
        'imagem_url': imagem_url,
        'public_id': public_id
    })

    return jsonify({'mensagem': 'Usuário atualizado com sucesso!'}), 200



@app.route('/gym/user/<int:id>', methods=['DELETE'])
def deleteUser(id):
    doc_ref = db.collection('usuarios').document(str(id))
    doc = doc_ref.get()

    if not doc.exists:
        return jsonify({'mensagem': 'ERRO! Usuário não encontrado!'}), 404

    dados = doc.to_dict()
    public_id = dados.get('public_id')

    if public_id:
        destroy(public_id)

    doc_ref.delete()

    return jsonify({'mensagem': 'Usuário excluído com sucesso!'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)