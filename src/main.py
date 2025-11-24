import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess


def executar_comando_sudo(comando):
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return True, "Comando executado com sucesso!"
        else:
            return False, f"Erro: {resultado.stderr.strip()}"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def criar_usuario():
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showwarning("Atenção", "Digite um nome de usuário.")
        return

    sucesso, msg = executar_comando_sudo(f"useradd -m {nome}")

    if sucesso:
        lbl_feedback.config(text=f"Usuário '{nome}' criado com sucesso!", fg="green")
        atualizar_visualizacao()
    else:
        lbl_feedback.config(text=msg, fg="red")


def excluir_usuario():
    nome = entry_nome.get().strip()
    if not nome:
        messagebox.showwarning("Atenção", "Digite um nome de usuário.")
        return

    sucesso, msg = executar_comando_sudo(f"userdel -r {nome}")

    if sucesso:
        lbl_feedback.config(text=f"Usuário '{nome}' excluído com sucesso!", fg="green")
        atualizar_visualizacao()
    else:
        lbl_feedback.config(text=msg, fg="red")


def atualizar_visualizacao():
    try:
        resultado = subprocess.run("tail -n 10 /etc/passwd", shell=True, capture_output=True, text=True)
        texto_passwd.delete(1.0, tk.END)
        texto_passwd.insert(tk.INSERT, resultado.stdout)
    except Exception as e:
        texto_passwd.insert(tk.INSERT, f"Erro ao ler arquivo: {str(e)}")


janela = tk.Tk()
janela.title("Gerenciador de Usuários (Lubuntu VM)")
janela.geometry("600x450")

frame_input = tk.Frame(janela, pady=10)
frame_input.pack()

tk.Label(frame_input, text="Nome do Usuário:").pack(side=tk.LEFT, padx=5)
entry_nome = tk.Entry(frame_input, width=20)
entry_nome.pack(side=tk.LEFT, padx=5)

frame_botoes = tk.Frame(janela, pady=10)
frame_botoes.pack()

btn_criar = tk.Button(frame_botoes, text="Criar Usuário (useradd)", bg="#d1e7dd", command=criar_usuario)
btn_criar.pack(side=tk.LEFT, padx=10)

btn_excluir = tk.Button(frame_botoes, text="Excluir Usuário (userdel)", bg="#f8d7da", command=excluir_usuario)
btn_excluir.pack(side=tk.LEFT, padx=10)

lbl_feedback = tk.Label(janela, text="Aguardando operação...", font=("Arial", 10, "italic"))
lbl_feedback.pack(pady=5)

tk.Label(janela, text="Visualização (/etc/passwd - últimas linhas):", font=("Arial", 10, "bold")).pack(pady=(20, 5))
texto_passwd = scrolledtext.ScrolledText(janela, width=70, height=10)
texto_passwd.pack(padx=10, pady=10)

atualizar_visualizacao()

janela.mainloop()