import psycopg2
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from services.aluno_service import AlunoService, CPFDuplicadoError
from services.instrutor_service import InstrutorService, CREFDuplicadoError
from services.avaliacao_fisica_service import AvaliacaoFisicaService, ValorInvalidoError


app = Flask(__name__)
app.secret_key = "chave-temporaria-trocar-depois"

aluno_service = AlunoService()
instrutor_service = InstrutorService()
avaliacao_service = AvaliacaoFisicaService()


@app.route("/")
def index():
    return redirect(url_for("listar_alunos"))


# --- rotas de Aluno ---

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
    aluno = aluno_service.buscar(aluno_id)

    if aluno is None:
        flash("Aluno não encontrado.")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        try:
            peso_form = request.form.get("peso")
            altura_form = request.form.get("altura")

            peso = float(peso_form) if peso_form else None
            altura = float(altura_form) if altura_form else None

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

        except ValueError:
            flash("Peso e altura devem ser valores numéricos válidos.")

    return render_template("aluno_form.html", aluno=aluno)


@app.route("/alunos/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    try:
        aluno_service.excluir(aluno_id)
        flash("Aluno excluído!")

    except psycopg2.IntegrityError as e:
        if e.pgcode == "23503":
            flash("Não é possível excluir este aluno, pois ele possui avaliações físicas vinculadas.")
        else:
            flash("Erro de integridade ao tentar excluir o aluno.")

    except Exception:
        flash("Ocorreu um erro inesperado ao tentar excluir o aluno.")

    return redirect(url_for("listar_alunos"))


# --- rotas de Instrutor ---

@app.route("/instrutores")
def listar_instrutores():
    instrutores = instrutor_service.listar()
    return render_template("instrutor_lista.html", instrutores=instrutores)


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
    instrutor = instrutor_service.buscar(instrutor_id)

    if instrutor is None:
        flash("Instrutor não encontrado.")
        return redirect(url_for("listar_instrutores"))

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

    return render_template("instrutor_form.html", instrutor=instrutor)


@app.route("/instrutores/<int:instrutor_id>/excluir", methods=["POST"])
def excluir_instrutor(instrutor_id):
    instrutor_service.excluir(instrutor_id)
    flash("Instrutor excluído!")
    return redirect(url_for("listar_instrutores"))


# --- rotas de Avaliação Física ---

@app.route("/alunos/<int:aluno_id>/avaliacoes")
def listar_avaliacoes(aluno_id):
    aluno = aluno_service.buscar(aluno_id)

    if aluno is None:
        flash("Aluno não encontrado.")
        return redirect(url_for("listar_alunos"))

    avaliacoes = avaliacao_service.listar_por_aluno(aluno_id)

    return render_template(
        "avaliacao_lista.html",
        aluno=aluno,
        avaliacoes=avaliacoes
    )


@app.route("/alunos/<int:aluno_id>/avaliacoes/nova", methods=["GET", "POST"])
def nova_avaliacao(aluno_id):
    aluno = aluno_service.buscar(aluno_id)

    if aluno is None:
        flash("Aluno não encontrado.")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        try:
            data_avaliacao = datetime.strptime(
                request.form["data_avaliacao"],
                "%Y-%m-%d"
            ).date()

            percentual = request.form.get("percentual_gordura")
            percentual_gordura = float(percentual) if percentual else None

            avaliacao_service.cadastrar(
                aluno_id=aluno_id,
                data_avaliacao=data_avaliacao,
                peso=float(request.form["peso"]),
                percentual_gordura=percentual_gordura,
                observacoes=request.form.get("observacoes", ""),
            )

            flash("Avaliação registrada com sucesso!")
            return redirect(url_for("listar_avaliacoes", aluno_id=aluno_id))

        except ValorInvalidoError as e:
            flash(str(e))

        except ValueError:
            flash("Data, peso e percentual de gordura devem ser valores válidos.")

    return render_template("avaliacao_form.html", aluno=aluno, avaliacao=None)


@app.route("/avaliacoes/<int:avaliacao_id>/editar", methods=["GET", "POST"])
def editar_avaliacao(avaliacao_id):
    avaliacao = avaliacao_service.buscar(avaliacao_id)

    if avaliacao is None:
        flash("Avaliação não encontrada.")
        return redirect(url_for("listar_alunos"))

    aluno = aluno_service.buscar(avaliacao.aluno_id)

    if aluno is None:
        flash("Aluno vinculado à avaliação não foi encontrado.")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        try:
            data_avaliacao = datetime.strptime(
                request.form["data_avaliacao"],
                "%Y-%m-%d"
            ).date()

            percentual = request.form.get("percentual_gordura")
            percentual_gordura = float(percentual) if percentual else None

            avaliacao_service.editar(
                avaliacao_id=avaliacao_id,
                aluno_id=avaliacao.aluno_id,
                data_avaliacao=data_avaliacao,
                peso=float(request.form["peso"]),
                percentual_gordura=percentual_gordura,
                observacoes=request.form.get("observacoes", "")
            )

            flash("Avaliação atualizada com sucesso!")
            return redirect(url_for("listar_avaliacoes", aluno_id=avaliacao.aluno_id))

        except ValorInvalidoError as e:
            flash(str(e))

        except ValueError:
            flash("Data, peso e percentual de gordura devem ser valores válidos.")

    return render_template("avaliacao_form.html", aluno=aluno, avaliacao=avaliacao)


@app.route("/avaliacoes/<int:avaliacao_id>/excluir", methods=["POST"])
def excluir_avaliacao(avaliacao_id):
    avaliacao = avaliacao_service.buscar(avaliacao_id)

    if avaliacao is None:
        flash("Avaliação não encontrada.")
        return redirect(url_for("listar_alunos"))

    aluno_id = avaliacao.aluno_id

    avaliacao_service.excluir(avaliacao_id)

    flash("Avaliação excluída!")
    return redirect(url_for("listar_avaliacoes", aluno_id=aluno_id))


if __name__ == "__main__":
    app.run(debug=True)