"""
storage.py — "Banco de dados" provisório em arquivos de texto.

Enquanto não existe um banco de dados de verdade, cada usuário
cadastrado é salvo como um arquivo dentro da pasta LOGINS/.

A pasta LOGINS/ NÃO existe até o primeiro cadastro ser feito — é o
próprio Python que cria ela (com os.makedirs) na primeira vez que
alguém se cadastra.

Cada arquivo LOGINS/<usuario>.txt guarda:
    nome=<nome completo>
    email=<e-mail>
    usuario=<usuário>
    senha=<hash da senha>
"""

import os
import hashlib
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGINS_DIR = os.path.join(BASE_DIR, "LOGINS")


def _hash_senha(senha: str) -> str:
    """Hash simples (sha256) só para não gravar a senha em texto puro.
    Não é um esquema de segurança de produção — apenas um cuidado básico
    enquanto o projeto não tem um banco de dados de verdade."""
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def _user_path(usuario: str) -> str:
    return os.path.join(LOGINS_DIR, f"{usuario}.txt")


def user_exists(usuario: str) -> bool:
    return os.path.isfile(_user_path(usuario))


def save_user(nome: str, email: str, usuario: str, senha: str) -> None:
    """Salva um novo usuário. Cria a pasta LOGINS/ se ainda não existir
    (isso só acontece na primeira vez que alguém se cadastra)."""
    os.makedirs(LOGINS_DIR, exist_ok=True)
    with open(_user_path(usuario), "w", encoding="utf-8") as f:
        f.write(f"nome={nome}\n")
        f.write(f"email={email}\n")
        f.write(f"usuario={usuario}\n")
        f.write(f"senha={_hash_senha(senha)}\n")


def get_user(usuario: str) -> Optional[dict]:
    path = _user_path(usuario)
    if not os.path.isfile(path):
        return None
    dados = {}
    with open(path, "r", encoding="utf-8") as f:
        for linha in f:
            if "=" in linha:
                chave, valor = linha.rstrip("\n").split("=", 1)
                dados[chave] = valor
    return dados


def validate_login(usuario: str, senha: str) -> bool:
    dados = get_user(usuario)
    if dados is None:
        return False
    return dados.get("senha") == _hash_senha(senha)
