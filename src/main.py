import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess


def executar_comando_sudo(comando):
    """
    Função auxiliar para executar comandos de sistema via subprocess.
    CONTEXTO DE APRENDIZAGEM:
    Utiliza subprocess.run para invocar o shell do Linux.
    É necessário rodar este script com 'sudo' (root) para que os comandos
    'useradd' e 'userdel' tenham permissão de escrita em /etc/passwd e /etc/shadow.
    """
    try:
        # shell=True permite passar o comando como uma string completa.
        # capture_output=True captura tanto o sucesso (stdout) quanto erros (stderr).
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )

        # Verifica o código de retorno (0 = Sucesso)
        if resultado.returncode == 0:
            return True, "Operação realizada com sucesso!"
        else:
            # Retorna a mensagem de erro do próprio Linux (stderr)
            return False, f"Erro do Sistema: {resultado.stderr.strip()}"
    except Exception as e:
        return False, f"Erro inesperado no Python: {str(e)}"


def criar_usuario():
    nome = entry_nome.get().strip()

    # Validação simples de entrada
    if not nome:
        messagebox.showwarning("Atenção", "O campo nome não pode estar vazio.")
        return
    if " " in nome:
        messagebox.showerror("Erro", "Nomes de usuário Linux não podem conter espaços.")
        return

    # REQUISITO 1: Criação de Usuário
    # Comando useradd com flag -m para criar o diretório home (/home/usuario)
    comando = f"useradd -m {nome}"

    sucesso, msg = executar_comando_sudo(comando)

    if sucesso:
        lbl_feedback.config(text=f"Sucesso: Usuário '{nome}' criado.", fg="green")
        atualizar_visualizacao()
    else:
        lbl_feedback.config(text=msg, fg="red")


def excluir_usuario():
    nome = entry_nome.get().strip()

    if not nome:
        messagebox.showwarning("Atenção", "Digite o nome do usuário para excluir.")
        return

    # REQUISITO 2: Exclusão de Usuário
    # Comando userdel com flag -r para remover também a pasta home e arquivos
    comando = f"userdel -r {nome}"

    sucesso, msg = executar_comando_sudo(comando)

    if sucesso:
        lbl_feedback.config(text=f"Sucesso: Usuário '{nome}' excluído.", fg="green")
        atualizar_visualizacao()
    else:
        lbl_feedback.config(text=msg, fg="red")


def atualizar_visualizacao():
    """
    REQUISITO 3: Visualização
    Lê o arquivo /etc/passwd para confirmar as alterações no sistema.
    """
    try:
        # Usa 'tail' para pegar apenas as últimas 10 linhas do arquivo
        resultado = subprocess.run("tail -n 10 /etc/passwd", shell=True, capture_output=True, text=True)
        texto_passwd.delete(1.0, tk.END)
        texto_passwd.insert(tk.INSERT, resultado.stdout)
    except Exception as e:
        texto_passwd.insert(tk.INSERT, f"Erro de leitura: {str(e)}")


# --- Construção da Interface Gráfica (Tkinter) ---
janela = tk.Tk()
janela.title("Gerenciador de Usuários (Lubuntu VM)")
janela.geometry("620x480")

# Cabeçalho
tk.Label(janela, text="Administração de Usuários Linux", font=("Arial", 14, "bold")).pack(pady=10)

# Entrada de Dados
frame_input = tk.Frame(janela)
frame_input.pack(pady=5)
tk.Label(frame_input, text="Nome do Usuário:").pack(side=tk.LEFT, padx=5)
entry_nome = tk.Entry(frame_input, width=25)
entry_nome.pack(side=tk.LEFT, padx=5)

# Botões de Ação
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=15)

# Botão Criar (Verde Claro)
btn_criar = tk.Button(frame_botoes, text="Criar Usuário (useradd)", bg="#d1e7dd", width=20, command=criar_usuario)
btn_criar.pack(side=tk.LEFT, padx=10)

# Botão Excluir (Vermelho Claro)
btn_excluir = tk.Button(frame_botoes, text="Excluir Usuário (userdel)", bg="#f8d7da", width=20, command=excluir_usuario)
btn_excluir.pack(side=tk.LEFT, padx=10)

# REQUISITO 4: Feedback Visual
lbl_feedback = tk.Label(janela, text="Sistema pronto.", font=("Arial", 10, "italic"), fg="blue")
lbl_feedback.pack(pady=5)

# Área de Texto (Visualização)
tk.Label(janela, text="Conteúdo do /etc/passwd (últimas linhas):", font=("Arial", 10, "bold")).pack(pady=(15, 5))
texto_passwd = scrolledtext.ScrolledText(janela, width=75, height=12)
texto_passwd.pack(padx=10, pady=5)

# Inicialização
atualizar_visualizacao()
janela.mainloop()