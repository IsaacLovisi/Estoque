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
    while True:
        print("1")
        cursor.execute("INSERT INTO produtos(nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        print("Produto adicionado com sucesso!")
        print("Aperte 1 para adicionar um novo produto/ Aperte qualquer número para volta ao menu ")
        saida = int(input())
        if saida != 1:
            break
        if saida == 1:
            print("2")
            while True:
                print("3")
                nome = input("Digite o nome do produto (Aperte Enter para voltar ao menu inicial): ")
                if nome == "":
                    print("4")
                    break
                print("5")
                cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
                search = cursor.fetchone()
                if search: 
                    print("6")
                    print("Produto já existe!")
                else:
                    try:
                        print("7")
                        quantidade = int(input(("Quantidade de itens: ")))
                        preco = float(input(("Valor unitário: ")))
                        print("Produto adicionado com sucesso!")
                        print("Aperte 1 para adicionar um novo produto/ Aperte qualquer número para volta ao menu ")
                        saida = int(input())
                        if saida == 1:
                            print("8")
                            continue
                        else:
                            print("9")
                            return
                    except ValueError:
                        print("10")
                        return

def listar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    if produtos:
        print("-" * 50)
        print(f"{'| ID ':<7} {'| Produtos ':<14} {'| Quantidade ':<13} {'| Preço |':<8}")
        print(50 * "-")
        for produtos in produtos:
            print(f"{produtos[0]:<9} {produtos[1]:<17} {produtos[2]:<10} {produtos[3]:<7.2f}")
    else:
        print("Nenhum produto cadastrado")

def atualizar_produto():
    id_produto = int(input("Informe o ID do produto: "))
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
    produtos = cursor.fetchall()
    
    if not produtos:
        print("ID inválido")
        return

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
    return 


def excluir_produtos(nome, id_produto):
    cursor.execute("DELETE FROM produtos WHERE nome = ? AND id = ?", (nome, id_produto))
    conn.commit()


def inicio():
    while True:
        print("-" * 42)
        print("|          BEM VINDO AO ESTOQUE          |")
        print("¯" * 42)
        opcao = input("1 - Produtos\n2 - Logs\n3 - Área de Acesso\n4 - Sair do programa\n:")
        if opcao == "":
            break
        match opcao:
            case '1':
                while True:
                    print("-" * 42)
                    print("|         Selecione uma opção         |")
                    print("¯" * 42)
                    print("|1  -         Criar Produto           |")
                    print("|2  -         Listar Produto          |")
                    print("|3  -         Atualizar Produto       |")
                    print("|4  -         Remover Produto         |")
                    print("|5  -         Voltar ao menu          |")
                    print("|6  -         Sair                    |")
                    print("-" * 42)
                    subopcao = input(":")
                    match subopcao:
                        case '1':
                            while True:
                                print("12")
                                nome = input(("Digite o nome do produto (Aperte Enter para voltar): "))
                                cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
                                search = cursor.fetchone()
                                if nome == "":
                                    print("13")
                                    break
                                if search:
                                    print("14")
                                    print("Produto já existe")
                                else: 
                                    print("15")
                                    quantidade = int(input(("Quantidade de itens: ")))
                                    preco = float(input(("Valor unitário: ")))
                                    criar_produto(nome, quantidade, preco)
                                    break
                        case '2':
                            listar_produtos()
                        case '3':
                            atualizar_produto()
                        case '4':
                            print("CRIAR FUNÇÃO DE REMOVER PRODUTO")#CRIAR FUNÇÃO DE REMOVER PRODUTO
                        case '5':
                            break
                        case '6':
                            return
                        case _:
                            print("Opção Inválida")
            case '2':
                print()
            case '3':
                print()
            case '4':
                print("passou pelo break da area bem vindo")
                break
            case _:
                print("Valor inválido")
                break  

inicio()
#excluir_produtos("Digite o nome do produto: ", 10)

