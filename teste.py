import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# Conectando ao banco de dados
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

# Criando as tabelas se não existirem
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    senha TEXT NOT NULL,
    nivel TEXT NOT NULL CHECK(nivel IN ('admin', 'controlador'))
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    acao TEXT NOT NULL,
    timestamp TEXT NOT NULL
)''')

conn.commit()

usuario_logado = None

def registrar_log(acao):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO logs (usuario, acao, timestamp) VALUES (?, ?, ?)", (usuario_logado, acao, timestamp))
    conn.commit()

# Funções CRUD
def criar_produto(nome, quantidade, preco):
    try:
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conn.commit()
        registrar_log(f"Adicionou produto: {nome}")
        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        listar_produtos()
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Nome do produto já existe!")

def listar_produtos():  
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM produtos")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)


def atualizar_produto(id, quantidade, preco):
    cursor.execute("UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?", (quantidade, preco, id))
    if cursor.rowcount == 0:
        messagebox.showerror("Erro", "ID não encontrado!")
    else:
        conn.commit()
        registrar_log(f"Atualizou produto ID {id}")
        messagebox.showinfo("Sucesso", "Produto atualizado!")
        listar_produtos()

def deletar_produto(id):
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        messagebox.showerror("Erro", "ID não encontrado!")
    else:
        conn.commit()
        registrar_log(f"Deletou produto ID {id}")
        messagebox.showinfo("Sucesso", "Produto deletado!")
        listar_produtos()

# Interface de Login
def autenticar():
    global usuario_logado
    nome = login_entry.get()
    senha = senha_entry.get()
    cursor.execute("SELECT nivel FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    resultado = cursor.fetchone()
    if resultado:
        usuario_logado = nome
        registrar_log("Login bem-sucedido")
        nivel = resultado[0]
        login_frame.pack_forget()
        if nivel == 'admin':
            iniciar_interface_admin()
        else:
            iniciar_interface_controlador()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# Interface Admin
def iniciar_interface_admin():
    janela.geometry("700x550")
    tk.Label(janela, text="Bem-vindo, Admin", font=("Arial", 14)).pack(pady=10)
    interface_estoque()

# Interface Controlador
def iniciar_interface_controlador():
    janela.geometry("700x500")
    tk.Label(janela, text="Bem-vindo, Controlador", font=("Arial", 14)).pack(pady=10)
    interface_estoque(admin=False)

# Interface de Estoque (com opção de admin ou não)
def interface_estoque(admin=True):
    global nome_entry, quantidade_entry, preco_entry, id_entry, tree

    frame = tk.Frame(janela)
    frame.pack(pady=10)

    tk.Label(frame, text="Nome:").grid(row=0, column=0)
    nome_entry = tk.Entry(frame)
    nome_entry.grid(row=0, column=1)

    tk.Label(frame, text="Quantidade:").grid(row=1, column=0)
    quantidade_entry = tk.Entry(frame)
    quantidade_entry.grid(row=1, column=1)

    tk.Label(frame, text="Preço:").grid(row=2, column=0)
    preco_entry = tk.Entry(frame)
    preco_entry.grid(row=2, column=1)

    botao_frame = tk.Frame(janela)
    botao_frame.pack(pady=10)

    if admin:
        tk.Button(botao_frame, text="Adicionar Produto", command=lambda: criar_produto(
            nome_entry.get(), int(quantidade_entry.get()), float(preco_entry.get()))).grid(row=0, column=0, padx=5)

        tk.Label(botao_frame, text="ID para atualizar/deletar:").grid(row=1, column=0)
        id_entry = tk.Entry(botao_frame)
        id_entry.grid(row=1, column=1)

        tk.Button(botao_frame, text="Atualizar Produto", command=lambda: atualizar_produto(
            int(id_entry.get()), int(quantidade_entry.get()), float(preco_entry.get()))).grid(row=2, column=0, padx=5)

        tk.Button(botao_frame, text="Deletar Produto", command=lambda: deletar_produto(int(id_entry.get()))).grid(row=2, column=1, padx=5)

    tree = ttk.Treeview(janela, columns=("ID", "Nome", "Quantidade", "Preço"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço")
    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    listar_produtos()

# Interface de login
janela = tk.Tk()
janela.title("Login - Estoque")
janela.geometry("300x200")

login_frame = tk.Frame(janela)
login_frame.pack(pady=30)

tk.Label(login_frame, text="Usuário:").grid(row=0, column=0)
login_entry = tk.Entry(login_frame)
login_entry.grid(row=0, column=1)

tk.Label(login_frame, text="Senha:").grid(row=1, column=0)
senha_entry = tk.Entry(login_frame, show="*")
senha_entry.grid(row=1, column=1)

tk.Button(login_frame, text="Entrar", command=autenticar).grid(row=2, column=0, columnspan=2, pady=10)

janela.mainloop()
conn.close()