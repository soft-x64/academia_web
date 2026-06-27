# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from services.aluno_service import AlunoService, CPFDuplicadoError
from services.instrutor_service import InstrutorService, CREFDuplicadoError

app = Flask(__name__)
app.secret_key = "chave-temporaria-trocar-depois"

aluno_service = AlunoService()
instrutor_service = InstrutorService()

@app.route("/alunos")
def listar_alunos():
    alunos = aluno_service.listar()
    return render_template("aluno_lista.html", alunos=alunos)

@app.route("/alunos/novo", methods=["GET", "POST"])
def novo_aluno():
    if request.method == "POST":
        try:
            peso_form = request.form.get("peso")
            altura_form = request.form.get("altura")

            peso = float(peso_form) if peso_form else None
            altura = float(altura_form) if altura_form else None

            aluno_service.cadastrar(
                nome=request.form["nome"],
                cpf=request.form["cpf"],
                email=request.form["email"],
                telefone=request.form["telefone"],
                peso=peso,
                altura=altura,
            )

            flash("Aluno cadastrado com sucesso!")
            return redirect(url_for("listar_alunos"))

        except CPFDuplicadoError as e:
            flash(str(e))

        except ValueError:
            flash("Peso e altura devem ser valores numéricos válidos.")

    return render_template("aluno_form.html", aluno=None)

@app.route("/alunos/<int:aluno_id>/editar", methods=["GET", "POST"])
def editar_aluno(aluno_id):
    if request.method == "POST":
        peso = float(request.form["peso"]) if request.form["peso"] else None
        altura = float(request.form["altura"]) if request.form["altura"] else None

        aluno_service.editar(
            aluno_id,
            nome=request.form["nome"],
            cpf=request.form["cpf"],
            email=request.form["email"],
            telefone=request.form["telefone"],
            peso=peso,
            altura=altura
        )

        flash("Aluno atualizado!")
        return redirect(url_for("listar_alunos"))

    aluno = aluno_service.buscar(aluno_id)

    return render_template("aluno_form.html", aluno=aluno)

@app.route("/alunos/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    aluno_service.excluir(aluno_id)
    flash("Aluno excluído!")
    return redirect(url_for("listar_alunos"))

# --- rotas de Instrutor ---

@app.route("/instrutores")
def listar_instrutores():
    instrutores = instrutor_service.listar()
    return render_template("instrutor_lista.html", instrutores=instrutores)

@app.route("/instrutores/novo", methods=["GET", "POST"])
@app.route("/instrutores/novo", methods=["GET", "POST"])
def novo_instrutor():
    if request.method == "POST":
        try:
            instrutor_service.cadastrar(
                nome=request.form["nome"],
                cpf=request.form["cpf"],
                email=request.form["email"],
                telefone=request.form["telefone"],
                cref=request.form["cref"],
                especialidade=request.form["especialidade"],
            )

            flash("Instrutor cadastrado com sucesso!")
            return redirect(url_for("listar_instrutores"))

        except CPFDuplicadoError as e:
            flash(str(e))

        except CREFDuplicadoError as e:
            flash(str(e))

    return render_template("instrutor_form.html", instrutor=None)

@app.route("/instrutores/<int:instrutor_id>/editar", methods=["GET", "POST"])
def editar_instrutor(instrutor_id):
    if request.method == "POST":
        instrutor_service.editar(
            instrutor_id,
            nome=request.form["nome"],
            cpf=request.form["cpf"],
            email=request.form["email"],
            telefone=request.form["telefone"],
            cref=request.form["cref"],
            especialidade=request.form["especialidade"],
        )

        flash("Instrutor atualizado!")
        return redirect(url_for("listar_instrutores"))

    instrutor = instrutor_service.buscar(instrutor_id)

    if instrutor is None:
        flash("Instrutor não encontrado.")
        return redirect(url_for("listar_instrutores"))

    return render_template("instrutor_form.html", instrutor=instrutor)

@app.route("/instrutores/<int:instrutor_id>/excluir", methods=["POST"])
def excluir_instrutor(instrutor_id):
    instrutor_service.excluir(instrutor_id)
    flash("Instrutor excluído!")
    return redirect(url_for("listar_instrutores"))

if __name__ == "__main__":
    app.run(debug=True)