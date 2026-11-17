
import sqlite3
import database

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_temporaria_sistema_assistencia"

database.criar_tabelas()


def login_obrigatorio(funcao):
    @wraps(funcao)
    def verificar_acesso(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))

        return funcao(*args, **kwargs)

    return verificar_acesso


@app.route("/", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("index"))

    if request.method == "POST":
        if "novo_usuario" in request.form:
            usuario = request.form.get("novo_usuario", "").strip()
            senha = request.form.get("nova_senha", "")
            confirmar_senha = request.form.get("confirmar_senha", "")

            if not usuario or not senha or not confirmar_senha:
                flash("Preencha todos os campos.", "login")
                return redirect(url_for("login"))

            if senha != confirmar_senha:
                flash("As senhas não são iguais.", "login")
                return redirect(url_for("login"))

            if len(senha) < 8:
                flash("A senha deve ter pelo menos 8 caracteres.", "login")
                return redirect(url_for("login"))

            if database.cadastrar_usuario(usuario, senha):
                flash("Cadastro realizado com sucesso! Faça seu login.", "login")
            else:
                flash("Esse nome de usuário já está cadastrado.", "login")

            return redirect(url_for("login"))

        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        if not usuario or not senha:
            flash("Preencha o usuário e a senha.", "login")
            return redirect(url_for("login"))

        if database.verificar_usuario(usuario, senha):
            session["usuario"] = usuario
            return redirect(url_for("index"))

        flash("Usuário ou senha incorretos.", "login")

    return render_template("login.html")


@app.route("/inicio")
@login_obrigatorio
def index():
    conexao = database.conectar()

    try:
        resultado = conexao.execute("""
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(CASE WHEN status = 'Pendente' THEN 1 ELSE 0 END), 0) AS pendentes,
                COALESCE(SUM(CASE WHEN status = 'Em andamento' THEN 1 ELSE 0 END), 0) AS andamento,
                COALESCE(SUM(CASE WHEN status = 'Concluído' THEN 1 ELSE 0 END), 0) AS concluidos,
                COALESCE(SUM(CASE WHEN status = 'Entregue' THEN 1 ELSE 0 END), 0) AS entregues
            FROM servicos
        """).fetchone()

    finally:
        conexao.close()

    return render_template(
        "index.html",
        total=resultado["total"],
        pendentes=resultado["pendentes"],
        andamento=resultado["andamento"],
        concluidos=resultado["concluidos"],
        entregues=resultado["entregues"]
    )



@app.route("/clientes", methods=["GET", "POST"])
@login_obrigatorio
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()

        if not nome or not telefone:
            flash("Preencha todos os campos.", "clientes")
            return redirect(url_for("clientes"))

        conexao = database.conectar()

        try:
            conexao.execute(
                "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
                (nome, telefone)
            )

            conexao.commit()
            flash("Cliente cadastrado com sucesso!", "clientes")

        except sqlite3.IntegrityError:
            flash("Este telefone já está cadastrado.", "clientes")

        finally:
            conexao.close()

        return redirect(url_for("clientes"))

    pesquisa = request.args.get("pesquisa", "").strip()
    conexao = database.conectar()

    try:
        if pesquisa:
            lista_clientes = conexao.execute(
                """
                SELECT * FROM clientes
                WHERE nome LIKE ? OR telefone LIKE ?
                ORDER BY id_cliente DESC
                """,
                (f"%{pesquisa}%", f"%{pesquisa}%")
            ).fetchall()
        else:
            lista_clientes = conexao.execute(
                """
                SELECT * FROM clientes
                ORDER BY id_cliente DESC
                LIMIT 5
                """
            ).fetchall()

    finally:
        conexao.close()

    return render_template(
        "clientes.html",
        clientes=lista_clientes,
        pesquisa=pesquisa
    )


@app.route("/servicos", methods=["GET", "POST"])
@login_obrigatorio
def servicos():
    if request.method == "POST":
        telefone = request.form.get("telefone", "").strip()
        aparelho = request.form.get("aparelho", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data = request.form.get("data", "").strip()
        status = request.form.get("status", "").strip()

        if not all([telefone, aparelho, descricao, data, status]):
            flash("Preencha todos os campos.", "servicos")
            return redirect(url_for("servicos"))

        status_validos = ["Pendente", "Em andamento", "Concluído", "Entregue"]

        if status not in status_validos:
            flash("Status inválido.", "servicos")
            return redirect(url_for("servicos"))

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            flash("Data inválida.", "servicos")
            return redirect(url_for("servicos"))

        conexao = database.conectar()

        try:
            cliente = conexao.execute(
                "SELECT id_cliente FROM clientes WHERE telefone = ?",
                (telefone,)
            ).fetchone()

            if not cliente:
                flash(
                    "Nenhum cliente encontrado com esse telefone. Cadastre o cliente primeiro.",
                    "servicos"
                )
                return redirect(url_for("servicos"))

            conexao.execute(
                """
                INSERT INTO servicos
                (id_cliente, aparelho, descricao_problema, data_cadastro, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (cliente["id_cliente"], aparelho, descricao, data, status)
            )

            conexao.commit()
            flash("Serviço registrado com sucesso!", "servicos")

        finally:
            conexao.close()

        return redirect(url_for("servicos"))

    pesquisa = request.args.get("pesquisa", "").strip()
    conexao = database.conectar()

    try:
        consulta = """
            SELECT
                servicos.id_servico,
                clientes.nome,
                clientes.telefone,
                servicos.aparelho,
                servicos.descricao_problema,
                servicos.data_cadastro,
                servicos.status
            FROM servicos
            JOIN clientes
            ON servicos.id_cliente = clientes.id_cliente
        """

        if pesquisa:
            consulta += """
                WHERE clientes.telefone LIKE ?
                OR servicos.aparelho LIKE ?
            """

            resultados = conexao.execute(
                consulta + " ORDER BY servicos.id_servico DESC",
                (f"%{pesquisa}%", f"%{pesquisa}%")
            ).fetchall()

        else:
            resultados = conexao.execute(
                consulta + " ORDER BY servicos.id_servico DESC"
            ).fetchall()

    finally:
        conexao.close()

    servicos_formatados = []

    for servico in resultados:
        servico = dict(servico)

        try:
            data_original = datetime.strptime(
                servico["data_cadastro"], "%Y-%m-%d"
            )
            servico["data_cadastro"] = data_original.strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            pass

        servicos_formatados.append(servico)

    return render_template(
        "servicos.html",
        servicos=servicos_formatados,
        pesquisa=pesquisa
    )


@app.route("/servicos/atualizar/<int:id_servico>", methods=["POST"])
@login_obrigatorio
def atualizar_status(id_servico):
    novo_status = request.form.get("status", "").strip()
    pesquisa = request.form.get("pesquisa", "").strip()

    status_validos = ["Pendente", "Em andamento", "Concluído", "Entregue"]

    if novo_status not in status_validos:
        flash("Status inválido.", "servicos")
        return redirect(url_for("servicos", pesquisa=pesquisa))

    conexao = database.conectar()

    try:
        resultado = conexao.execute(
            """
            UPDATE servicos
            SET status = ?
            WHERE id_servico = ?
            """,
            (novo_status, id_servico)
        )

        if resultado.rowcount == 0:
            flash("Serviço não encontrado.", "servicos")
        else:
            conexao.commit()
            flash("Status atualizado com sucesso!", "servicos")

    finally:
        conexao.close()

    return redirect(url_for("servicos", pesquisa=pesquisa))


@app.route("/sair")
def sair():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
