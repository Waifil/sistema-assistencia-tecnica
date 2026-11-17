
import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = Path(__file__).resolve().parent / "assistencia.db"


def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL UNIQUE
        )
    """)

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            aparelho TEXT NOT NULL,
            descricao_problema TEXT NOT NULL,
            data_cadastro TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        )
    """)

    conexao.commit()
    conexao.close()


def cadastrar_usuario(usuario, senha):
    conexao = conectar()

    try:
        senha_hash = generate_password_hash(senha)

        conexao.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha_hash)
        )

        conexao.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conexao.close()


def verificar_usuario(usuario, senha):
    conexao = conectar()

    try:
        resultado = conexao.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        ).fetchone()

        return bool(
            resultado and check_password_hash(resultado["senha"], senha)
        )

    finally:
        conexao.close()

def apagar_tudo():
    conexao = conectar()

    try:
        conexao.execute("DELETE FROM servicos")
        conexao.execute("DELETE FROM clientes")
        conexao.execute("DELETE FROM usuarios")
        conexao.commit()
        return True

    except sqlite3.Error:
        conexao.rollback()
        return False

    finally:
        conexao.close()
