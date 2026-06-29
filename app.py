import psycopg2
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash

from services.aluno_service import AlunoService, CPFDuplicadoError
from services.instrutor_service import InstrutorService, CREFDuplicadoError
from services.avaliacao_fisica_service import AvaliacaoFisicaService, ValorInvalidoError
from services.aparelho_service import AparelhoService
from services.exercicio_service import ExercicioService
from services.fichaTreino_service import FichaTreinoService


app = Flask(__name__)
app.secret_key = "chave-temporaria-trocar-depois"

aluno_service = AlunoService()
instrutor_service = InstrutorService()
avaliacao_service = AvaliacaoFisicaService()
aparelho_service = AparelhoService()
exercicio_service = ExercicioService()
ficha_service = FichaTreinoService()


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    hoje = datetime.today()

    alunos = aluno_service.listar()
    instrutores = instrutor_service.listar()

    total_alunos = len(alunos)
    total_instrutores = len(instrutores)

    total_avaliacoes_mes = avaliacao_service.contar_avaliacoes_no_mes(
        ano=hoje.year,
        mes=hoje.month
    )

    ultimas_avaliacoes = avaliacao_service.listar_ultimas(limite=4)

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        total_instrutores=total_instrutores,
        total_avaliacoes_mes=total_avaliacoes_mes,
        ultimas_avaliacoes=ultimas_avaliacoes
    )


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

            flash("Aluno cadastrado com sucesso!", "success")
            return redirect(url_for("listar_alunos"))

        except CPFDuplicadoError as e:
            flash(str(e), "danger")

        except ValueError:
            flash("Peso e altura devem ser valores numéricos válidos.", "danger")

        except psycopg2.IntegrityError:
            flash("Já existe um aluno cadastrado com esses dados.", "danger")

        except Exception:
            flash("Ocorreu um erro inesperado ao cadastrar o aluno.", "danger")

    return render_template("aluno_form.html", aluno=None)


@app.route("/alunos/<int:aluno_id>/editar", methods=["GET", "POST"])
def editar_aluno(aluno_id):
    aluno = aluno_service.buscar(aluno_id)

    if aluno is None:
        flash("Aluno não encontrado.", "danger")
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
                altura=altura,
            )

            flash("Aluno atualizado com sucesso!", "success")
            return redirect(url_for("listar_alunos"))

        except CPFDuplicadoError as e:
            flash(str(e), "danger")

        except ValueError:
            flash("Peso e altura devem ser valores numéricos válidos.", "danger")

        except psycopg2.IntegrityError:
            flash("Não foi possível atualizar. Já existe outro aluno com esse CPF.", "danger")

        except Exception:
            flash("Ocorreu um erro inesperado ao atualizar o aluno.", "danger")

    return render_template("aluno_form.html", aluno=aluno)


@app.route("/alunos/<int:aluno_id>/excluir", methods=["POST"])
def excluir_aluno(aluno_id):
    try:
        aluno_service.excluir(aluno_id)
        flash("Aluno excluído com sucesso!", "success")

    except psycopg2.IntegrityError:
        flash(
            "Não é possível excluir este aluno, pois ele possui avaliações físicas vinculadas.",
            "warning"
        )

    except Exception:
        flash("Ocorreu um erro inesperado ao tentar excluir o aluno.", "danger")

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

            flash("Instrutor cadastrado com sucesso!", "success")
            return redirect(url_for("listar_instrutores"))

        except CPFDuplicadoError as e:
            flash(str(e), "danger")

        except CREFDuplicadoError as e:
            flash(str(e), "danger")

        except psycopg2.IntegrityError:
            flash("Já existe um instrutor cadastrado com esse CPF ou CREF.", "danger")

        except Exception:
            flash("Ocorreu um erro inesperado ao cadastrar o instrutor.", "danger")

    return render_template("instrutor_form.html", instrutor=None)


@app.route("/instrutores/<int:instrutor_id>/editar", methods=["GET", "POST"])
def editar_instrutor(instrutor_id):
    instrutor = instrutor_service.buscar(instrutor_id)

    if instrutor is None:
        flash("Instrutor não encontrado.", "danger")
        return redirect(url_for("listar_instrutores"))

    if request.method == "POST":
        try:
            instrutor_service.editar(
                instrutor_id,
                nome=request.form["nome"],
                cpf=request.form["cpf"],
                email=request.form["email"],
                telefone=request.form["telefone"],
                cref=request.form["cref"],
                especialidade=request.form["especialidade"],
            )

            flash("Instrutor atualizado com sucesso!", "success")
            return redirect(url_for("listar_instrutores"))

        except CPFDuplicadoError as e:
            flash(str(e), "danger")

        except CREFDuplicadoError as e:
            flash(str(e), "danger")

        except psycopg2.IntegrityError:
            flash("Não foi possível atualizar. Já existe outro instrutor com esse CPF ou CREF.", "danger")

        except Exception:
            flash("Ocorreu um erro inesperado ao atualizar o instrutor.", "danger")

    return render_template("instrutor_form.html", instrutor=instrutor)


@app.route("/instrutores/<int:instrutor_id>/excluir", methods=["POST"])
def excluir_instrutor(instrutor_id):
    try:
        instrutor_service.excluir(instrutor_id)
        flash("Instrutor excluído com sucesso!", "success")

    except psycopg2.IntegrityError:
        flash(
            "Não é possível excluir este instrutor, pois ele possui dados vinculados no sistema.",
            "warning"
        )

    except Exception:
        flash("Ocorreu um erro inesperado ao tentar excluir o instrutor.", "danger")

    return redirect(url_for("listar_instrutores"))


# --- rotas de Avaliação Física ---

@app.route("/avaliacoes")
def avaliacoes_geral():
    alunos = aluno_service.listar()
    return render_template("avaliacao_geral.html", alunos=alunos)


@app.route("/alunos/<int:aluno_id>/avaliacoes")
def listar_avaliacoes(aluno_id):
    aluno = aluno_service.buscar(aluno_id)

    if aluno is None:
        flash("Aluno não encontrado.", "danger")
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
        flash("Aluno não encontrado.", "danger")
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

            flash("Avaliação registrada com sucesso!", "success")
            return redirect(url_for("listar_avaliacoes", aluno_id=aluno_id))

        except ValorInvalidoError as e:
            flash(str(e), "danger")

        except ValueError:
            flash("Data, peso e percentual de gordura devem ser valores válidos.", "danger")

        except psycopg2.IntegrityError:
            flash("Não foi possível registrar a avaliação, pois o aluno vinculado não existe.", "warning")

        except Exception:
            flash("Ocorreu um erro inesperado ao registrar a avaliação.", "danger")

    return render_template("avaliacao_form.html", aluno=aluno, avaliacao=None)


@app.route("/avaliacoes/<int:avaliacao_id>/editar", methods=["GET", "POST"])
def editar_avaliacao(avaliacao_id):
    avaliacao = avaliacao_service.buscar(avaliacao_id)

    if avaliacao is None:
        flash("Avaliação não encontrada.", "danger")
        return redirect(url_for("listar_alunos"))

    aluno = aluno_service.buscar(avaliacao.aluno_id)

    if aluno is None:
        flash("Aluno vinculado à avaliação não foi encontrado.", "danger")
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

            flash("Avaliação atualizada com sucesso!", "success")
            return redirect(url_for("listar_avaliacoes", aluno_id=avaliacao.aluno_id))

        except ValorInvalidoError as e:
            flash(str(e), "danger")

        except ValueError:
            flash("Data, peso e percentual de gordura devem ser valores válidos.", "danger")

        except psycopg2.IntegrityError:
            flash("Não foi possível atualizar a avaliação, pois o aluno vinculado não existe.", "warning")

        except Exception:
            flash("Ocorreu um erro inesperado ao atualizar a avaliação.", "danger")

    return render_template("avaliacao_form.html", aluno=aluno, avaliacao=avaliacao)


@app.route("/avaliacoes/<int:avaliacao_id>/excluir", methods=["POST"])
def excluir_avaliacao(avaliacao_id):
    avaliacao = avaliacao_service.buscar(avaliacao_id)

    if avaliacao is None:
        flash("Avaliação não encontrada.", "danger")
        return redirect(url_for("listar_alunos"))

    aluno_id = avaliacao.aluno_id

    try:
        avaliacao_service.excluir(avaliacao_id)
        flash("Avaliação excluída com sucesso!", "success")

    except Exception:
        flash("Ocorreu um erro inesperado ao excluir a avaliação.", "danger")

    return redirect(url_for("listar_avaliacoes", aluno_id=aluno_id))

# --- rotas de Aparelho ---

@app.route("/aparelhos")
def listar_aparelhos():
    aparelhos = aparelho_service.listar()
    return render_template("aparelho_lista.html", aparelhos=aparelhos)

@app.route("/aparelhos/novo", methods=["GET", "POST"])
def novo_aparelho():
    if request.method == "POST":
        aparelho_service.cadastrar(
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
            status=request.form.get("status", "Disponível")
        )
        flash("Aparelho cadastrado com sucesso!")
        return redirect(url_for("listar_aparelhos"))

    return render_template("aparelho_form.html", aparelho=None)

@app.route("/aparelhos/<int:aparelho_id>/editar", methods=["GET", "POST"])
def editar_aparelho(aparelho_id):
    aparelho = aparelho_service.buscar(aparelho_id)

    if aparelho is None:
        flash("Aparelho não encontrado.")
        return redirect(url_for("listar_aparelhos"))

    if request.method == "POST":
        aparelho_service.editar(
            aparelho_id=aparelho_id,
            nome=request.form["nome"],
            descricao=request.form.get("descricao", ""),
            status=request.form["status"]
        )
        flash("Aparelho atualizado!")
        return redirect(url_for("listar_aparelhos"))

    return render_template("aparelho_form.html", aparelho=aparelho)

@app.route("/aparelhos/<int:aparelho_id>/excluir", methods=["POST"])
def excluir_aparelho(aparelho_id):
    try:
        aparelho_service.excluir(aparelho_id)
        flash("Aparelho excluído!")
    except Exception:
        flash("Não foi possível excluir este aparelho. Ele pode estar vinculado a um exercício.")
    return redirect(url_for("listar_aparelhos"))

# --- rotas de Exercício ---

@app.route("/exercicios")
def listar_exercicios():
    exercicios = exercicio_service.listar()
    return render_template("exercicio_lista.html", exercicios=exercicios)

@app.route("/exercicios/novo", methods=["GET", "POST"])
def novo_exercicio():
    if request.method == "POST":
        exercicio_service.cadastrar(
            nome=request.form["nome"],
            grupo_muscular=request.form["grupo_muscular"],
            descricao=request.form.get("descricao", "")
        )
        flash("Exercício cadastrado com sucesso!")
        return redirect(url_for("listar_exercicios"))

    return render_template("exercicio_form.html", exercicio=None)

@app.route("/exercicios/<int:exercicio_id>/editar", methods=["GET", "POST"])
def editar_exercicio(exercicio_id):
    exercicio = exercicio_service.buscar(exercicio_id)

    if exercicio is None:
        flash("Exercício não encontrado.")
        return redirect(url_for("listar_exercicios"))

    if request.method == "POST":
        exercicio_service.editar(
            exercicio_id=exercicio_id,
            nome=request.form["nome"],
            grupo_muscular=request.form["grupo_muscular"],
            descricao=request.form.get("descricao", "")
        )
        flash("Exercício atualizado!")
        return redirect(url_for("listar_exercicios"))

    return render_template("exercicio_form.html", exercicio=exercicio)

@app.route("/exercicios/<int:exercicio_id>/excluir", methods=["POST"])
def excluir_exercicio(exercicio_id):
    try:
        exercicio_service.excluir(exercicio_id)
        flash("Exercício excluído!")
    except Exception:
        flash("Não foi possível excluir este exercício. Ele pode estar vinculado a uma ficha de treino.")
    return redirect(url_for("listar_exercicios"))

# --- rotas de Ficha de Treino ---

@app.route("/fichas")
def listar_fichas():
    # Podemos buscar todas as fichas no serviço, que já traz o status (Ativa/Vencida)
    fichas = ficha_service.listar_fichas()
    return render_template("ficha_lista.html", fichas=fichas)

@app.route("/fichas/nova", methods=["GET", "POST"])
def nova_ficha():
    if request.method == "POST":
        try:
            ficha_service.criar_ficha(
                aluno_id=request.form["aluno_id"],
                instrutor_id=request.form["instrutor_id"],
                data_inicio=request.form["data_inicio"],
                data_vencimento=request.form["data_vencimento"],
                objetivo=request.form["objetivo"]
            )
            flash("Ficha criada com sucesso!")
            return redirect(url_for("listar_fichas"))
        except Exception as e:
            flash("Erro ao criar a ficha. Verifique as datas e os campos informados.")

    # Busca listas para os combos (<select>) do HTML
    alunos = aluno_service.listar()
    instrutores = instrutor_service.listar()
    return render_template("ficha_form.html", ficha=None, alunos=alunos, instrutores=instrutores)

@app.route("/fichas/<int:ficha_id>/editar", methods=["GET", "POST"])
def editar_ficha(ficha_id):
    # Lógica simplificada: para editar a ficha, vamos buscar todas as fichas e filtrar (no cenário ideal, você teria um buscar_por_id no repository da Ficha)
    fichas = ficha_service.listar_fichas()
    ficha = next((f for f in fichas if f.id == ficha_id), None)

    if ficha is None:
        flash("Ficha não encontrada.")
        return redirect(url_for("listar_fichas"))

    if request.method == "POST":
        try:
            ficha_service.editar_ficha(
                ficha_id=ficha_id,
                aluno_id=request.form["aluno_id"],
                instrutor_id=request.form["instrutor_id"],
                data_inicio=request.form["data_inicio"],
                data_vencimento=request.form["data_vencimento"],
                objetivo=request.form["objetivo"]
            )
            flash("Ficha atualizada com sucesso!")
            return redirect(url_for("listar_fichas"))
        except Exception as e:
            flash("Erro ao atualizar a ficha.")

    alunos = aluno_service.listar()
    instrutores = instrutor_service.listar()
    return render_template("ficha_form.html", ficha=ficha, alunos=alunos, instrutores=instrutores)

@app.route("/fichas/<int:ficha_id>/excluir", methods=["POST"])
def excluir_ficha(ficha_id):
    try:
        ficha_service.excluir_ficha(ficha_id)
        flash("Ficha excluída com sucesso!")
    except Exception:
        flash("Ocorreu um erro ao excluir a ficha.")
    return redirect(url_for("listar_fichas"))

# (Opcional: Rota de visualização detalhada da Ficha)
@app.route("/fichas/<int:ficha_id>/visualizar")
def visualizar_ficha(ficha_id):
    fichas = ficha_service.listar_fichas()
    ficha = next((f for f in fichas if f.id == ficha_id), None)
    
    if ficha is None:
        flash("Ficha não encontrada.")
        return redirect(url_for("listar_fichas"))
        
    itens_ficha = ficha_service.obter_exercicios_da_ficha(ficha_id)
    return render_template("ficha_visualizar.html", ficha=ficha, itens_ficha=itens_ficha)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)