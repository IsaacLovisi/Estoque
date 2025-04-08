import sqlite3
import datetime


conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    quantidade INT NOT NULL,
    preco REAL NOT NULL
    )
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        acao TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
        )
    """)

conn.commit()

"""def registrar_log(acao):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs(acao, timestamp) VALUES (?, ?)", (acao, timestamp))
    conn.commit()"""

def criar_produto(nome, quantidade, preco):
    try:
        cursor.execute("INSERT INTO produtos(nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Produto já existe")

def listar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        print(f"{'| ID ':<7} {'| Produtos ':<14} {'| Quantidade ':<13} {'| Preço |':<8}")
        print(50 * "-")
        for produtos in produtos:
            print(f"{produtos[0]:<9} {produtos[1]:<17} {produtos[2]:<10} {produtos[3]:<7.2f}")
    else:
        print("Nenhum produto cadastrado")

def atualizar_produto():
    id_produto = int(input("Informe o ID do produto: "))
    print("1 - Atualizar quantidade")
    print("2 - Atualizar preço")
    opcao = int(input("Escolha a opção: "))

    match opcao:
        case 1:
            novo_valor = int(input("Nova quantidade: "))
            cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_valor, id_produto))
        case 2:
            novo_valor = float(input("Novo preço: "))
            cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_valor, id_produto))
        case _:
            print("Opção inválida.")
            return

    conn.commit()
    print("Produto atualizado com sucesso!")

def inicio():
    print("-" * 42)
    print("|          BEM VINDO AO ESTOQUE          |")
    print("¯" * 42)
    opcao = int(input("1 - Produtos\n2 - Logs\n3 - Área de Acesso\n:"))
    match opcao:
        case 1:
            print("-" * 42)

inicio()