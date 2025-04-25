
# 📦 API Pulse Fit - Gerenciamento de Usuários

API RESTful desenvolvida com **Flask** para gerenciar usuários de uma academia. Utiliza **Firebase Firestore** como banco de dados, **Cloudinary** para armazenar imagens e **Twilio WhatsApp** para envio de mensagens automáticas.

API desenvolvida por [Pedro Vitor](https://api-academia-alpha.vercel.app/)

FrontEnd desenvolvido por [João Pedro](https://github.com/joazao-pedroso)

[Link do site da Catraca na Vercel](https://pulse-fit-catraca.vercel.app/) - [Repositório GitHub](https://github.com/joazao-pedroso/projeto-acedemia-users)

[Link do site Adm na Vercel](https://pulse-fit-adm.vercel.app/) - [Repositório GitHub](https://github.com/joazao-pedroso/projeto-academia-adm)


## 🚀 Tecnologias Utilizadas

- Python (Flask)
- Firebase Firestore
- Cloudinary (upload de imagens)
- Twilio WhatsApp API (envio de mensagens)
- Dotenv (gerenciamento de variáveis de ambiente)
- CORS (Cross-Origin Resource Sharing)

---

## 📁 Estrutura do Projeto

```
├── app.py                # Arquivo principal da API
├── .env                  # Variáveis de ambiente (NÃO subir no GitHub)
├── requirements.txt      # Dependências do projeto
├── vercel.json           # Arquivo para fazer o deploy do projeto na Vercel 
└── README.md             # Este arquivo
```

---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/Pedro-Vitor-Ribeiro-Silva/API_ACADEMIA.git
cd API_ACADEMIA
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Crie um arquivo `.env` com as seguintes variáveis:

```env
CLOUDINARY_CLOUD_NAME=''
CLOUDINARY_API_KEY=''
CLOUDINARY_API_SECRET=''

TWILIO_SID=''
TWILIO_TOKEN=''
TWILIO_WHATSAPP_FROM='whatsapp:+11111111111' <-- Altere o Número para o qual o Twilio te disponibilizar!

CONFIG_FIREBASE={"type": "...","project_id": "...",...} # JSON como string (com aspas)
```


---

## 🧪 Endpoints

### ✅ Status da API

`GET /`

Retorna uma mensagem de que a API está online.

---

### 👥 Usuários

#### 📄 Listar todos
`GET /gym`

#### 🔍 Buscar por ID
`GET /gym/user/id/<id>`

#### 🔍 Buscar por CPF
`GET /gym/user/cpf/<cpf>`

#### ➕ Criar usuário
`POST /gym`

**Form-Data**:
- nome
- cpf
- telefone
- imagem (opcional)

#### ✏️ Editar usuário
`PUT /gym/user/<id>`

**Form-Data**:
- nome
- cpf
- telefone
- imagem (opcional)

#### 🔃 Atualizar status (ativo/inativo)
`PATCH /gym/user/<id>`

**JSON**:
```json
{ "status": "true" }
```

#### 💬 Enviar mensagem WhatsApp
`GET /gym/user/wpp/<id>`

#### ❌ Excluir usuário
`DELETE /gym/user/<id>`

---

## 📸 Upload de Imagens

As imagens dos usuários são armazenadas no **Cloudinary** e o `public_id` é salvo para possibilitar atualização ou exclusão futura.

---

## 📲 Envio de Mensagens

O envio de mensagens via **Twilio WhatsApp** é utilizado para notificar usuários inativos.

---

## 🔐 Requisitos Extras

- Validação de CPF (11 dígitos numéricos)
- Verificação de duplicidade de CPF
- Controle incremental de ID (`controle_id` no Firestore)
- Upload e remoção de imagem no Cloudinary

---

## 🧼 Observações

- Para usar a Twilio WhatsApp API, é necessário ter um número verificado.
- Certifique-se de configurar corretamente seu `.env`.
- As imagens são deletadas do Cloudinary ao atualizar ou excluir um usuário.

---

## 🧑‍💻 Autor

Desenvolvido por **Pedro Vitor Ribeiro Silva**

---

## 📜 Licença

MIT © 2025
