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
        saida = input()
        if saida != "1":
            break
        if saida == "1":
            print("2")
            while True:
                print("3")
                nome = input("Digite o nome do produto (Aperte Enter para voltar ao menu inicial): ")
                if nome == "":
                    print("4")
                    return
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
                        if quantidade < 0 or preco <0:
                            if quantidade <0:
                                print(f"valor inválido ({quantidade})")
                            else:
                                print(f"valor inválido ({preco})")
                        else:
                            cursor.execute("INSERT INTO produtos(nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
                            conn.commit()
                            print("Produto adicionado com sucesso!")
                            print("Aperte 1 para adicionar um novo produto/ Aperte qualquer número para volta ao menu ")
                            saida = input()
                            if saida == "1":
                                print("8")
                                continue
                            else:
                                print("9")
                                return
                    except ValueError:
                            print("10")
                            return
    conn.commit()

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
    listar_produtos()
    id_produto = int(input("\nInforme o ID do produto: "))
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
            if novo_valor < 0:
                print(f"fValor Indisponível ({novo_valor})")
                return
            else:
                cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (novo_valor, id_produto))
        case 2:
            novo_valor = float(input("Novo preço: "))
            if novo_valor <= 0:
                print(f"Valor Indisponível ({novo_valor})")
            else:
                cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?", (novo_valor, id_produto))
        case _:
            print("Opção inválida.")
            return

    conn.commit()
    print("Produto atualizado com sucesso!")
    return 


def excluir_produtos(nome):
    cursor.execute("SELECT * FROM produtos WHERE nome = ?", (nome,))
    search = cursor.fetchone()
    if search:
        numb = input(f"Você tem certeza que deseja excluir o produto {search[1]}? Digite '1'\n:")
        if numb == "1" and search:
            cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome,))
            conn.commit()
            print("Produto excluido com sucesso")
    else:
        print("Produto não existe")

def menu_produtos():
    while True:
        print("-" * 42)
        print("|         Selecione uma opção         |")
        print("¯" * 42)
        print("|1  -         Criar Produto           |")
        print("|2  -         Listar Produto          |")
        print("|3  -         Atualizar Produto       |")
        print("|4  -         Remover Produto         |")
        print("|5  -         Sair                    |")
        print("-" * 42)
        opcaoMenu = input(":")
        match opcaoMenu:
            case '1':
                menu_criar_produto()
            case '2':
                listar_produtos()
            case '3':
                atualizar_produto()
            case '4':
                listar_produtos()
                nome = input("\nDigite o nome do produto que deseja excluir\n:")
                excluir_produtos(nome)
            case '5':
                return
            case _:
                print("Opção Inválida")

def menu_criar_produto():
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
                    if quantidade < 0 or preco < 0:
                        if quantidade < 0:
                            print(f"Valor inválido ({quantidade})")
                        else:
                            print(f"Valor inválido ({preco})")
                    else:
                        criar_produto(nome, quantidade, preco)
                        break

def inicio():
    while True:
        print("-" * 42)
        print("|          BEM VINDO AO ESTOQUE          |")
        print("¯" * 42)
        opcao = input("1 - Produtos\n2 - Sair do programa\n:")
        if opcao == "":
            break
        match opcao:
            case '1':
                menu_produtos()
            case '2':
                break
            case _:
                print("Valor inválido")
                break  

inicio()