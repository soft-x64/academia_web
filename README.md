# Instalação e Execução do Projeto

## TrainerX64

Sistema web de gerenciamento de academia desenvolvido com **Python**, **Flask**, **PostgreSQL**, **HTML**, **CSS**, **Bootstrap** e **Jinja2**.

---

## Pré-requisitos

Antes de rodar o projeto, é necessário ter instalado:

* Python 3
* PostgreSQL
* Git
* VS Code ou outro editor de código

---

## 1. Clonar o repositório

```bash
git clone https://github.com/soft-x64/academia_web.git
```

Depois, entre na pasta do projeto:

```bash
cd academia_web
```

---

## 2. Criar ambiente virtual

```bash
python -m venv venv
```

Ativar o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

---

## 3. Instalar dependências

Se existir o arquivo `requirements.txt`, execute:

```bash
pip install -r requirements.txt
```

Caso não exista, instale manualmente:

```bash
pip install flask psycopg2-binary
```

---

## 4. Configurar o banco de dados

O sistema utiliza **PostgreSQL**.

Crie um banco de dados para o projeto:

```sql
CREATE DATABASE academia_db;
```

Depois, execute os scripts SQL disponíveis na pasta:

```txt
database/
```

As principais tabelas esperadas são:

```txt
aluno
instrutor
avaliacao_fisica
aparelho
exercicio
exercicio_aparelho
ficha_treino
item_ficha
configuracao_sistema
```

---

## 5. Configurar conexão com o banco

Verifique o arquivo:

```txt
database/connection.py
```

Configure com os dados do seu PostgreSQL:

```python
import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="academia_db",
        user="postgres",
        password="SUA_SENHA",
        port="5432"
    )
```

Altere `database`, `user`, `password` e `port` conforme sua configuração local.

---

## 6. Rodar o sistema

Com o ambiente virtual ativado, execute:

```bash
python app.py
```

Acesse no navegador:

```txt
http://127.0.0.1:5000
```

ou:

```txt
http://localhost:5000
```
---

## 7. Acesso por link público

Para disponibilizar o sistema temporariamente para outras pessoas, é possível usar o **ngrok**.

Com o Flask rodando, abra outro terminal e execute:

```bash
ngrok http 5000
```

O ngrok irá gerar um link parecido com:

```txt
https://alguma-coisa.ngrok-free.app
```

Esse link pode ser compartilhado para acesso ao sistema enquanto o servidor estiver rodando.
