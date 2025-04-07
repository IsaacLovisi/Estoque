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

def atualizar_produtos(cod, quantidade, preco):
    match cod:
        case 1:         
            cursor.execute("UPDATE produtos SET produtos(quantidade) VALUE (?) ", (quantidade))
        case 2:
            cursor.execute("Update produtos SET produtos(preco) VALUE (?)", (preco))



