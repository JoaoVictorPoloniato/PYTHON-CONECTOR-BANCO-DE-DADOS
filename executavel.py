import tkinter as tk
from tkinter import messagebox
from conexao import conectar
import mysql.connector

def realizar_consulta(tabela_entry, usar_where_var, condicao_entry, resultado_text):
    tabela = tabela_entry.get()
    usar_where = usar_where_var.get()
    condicao = condicao_entry.get()

    try:
        conexao = conectar()
        cursor = conexao.cursor(prepared=True)

        consulta_sql = f"SELECT * FROM {tabela}"
        if usar_where == 1 and condicao:
            consulta_sql += f" WHERE {condicao}"

        cursor.execute(consulta_sql)
        resultados = cursor.fetchall()

        resultado_text.delete("1.0", tk.END)
        if resultados:
            resultado_text.insert(tk.END, "Resultados da Consulta:\n")
            for resultado in resultados:
                resultado_text.insert(tk.END, f"{resultado}\n")
        else:
            resultado_text.insert(tk.END, "Nenhum resultado encontrado.")

        cursor.close()
        conexao.close()

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro na Consulta", f"Erro na consulta: {erro}")

def realizar_delete(tabela_entry, usar_where_var, condicao_entry):
    tabela = tabela_entry.get()
    usar_where = usar_where_var.get()
    condicao = condicao_entry.get()

    try:
        conexao = conectar()
        cursor = conexao.cursor(prepared=True)

        delete_sql = f"DELETE FROM {tabela}"
        if usar_where == 1 and condicao:
            delete_sql += f" WHERE {condicao}"

        cursor.execute(delete_sql)
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Deletar", "Delete realizado com sucesso!")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro no Delete", f"Erro no delete: {erro}")

def realizar_update(tabela_entry, coluna_entry, novo_valor_entry, usar_between_var,
                    nome_coluna_between_entry, inicio_entry, fim_entry,
                    usar_where_var, coluna_where_entry, valor_where_entry):
    tabela = tabela_entry.get()
    coluna_update = coluna_entry.get()
    novo_valor = novo_valor_entry.get()

    usar_between = usar_between_var.get()
    nome_coluna_between = nome_coluna_between_entry.get()
    inicio = inicio_entry.get()
    fim = fim_entry.get()

    usar_where = usar_where_var.get()
    coluna_where = coluna_where_entry.get()
    valor_where = valor_where_entry.get()

    try:
        conexao = conectar()
        cursor = conexao.cursor(prepared=True)

        update_sql = f"UPDATE {tabela} SET {coluna_update} = %s"

        if usar_between == 1 and nome_coluna_between and inicio and fim:
            update_sql += f" WHERE {nome_coluna_between} BETWEEN %s AND %s"
            if usar_where == 1 and coluna_where and valor_where:
                update_sql += f" AND {coluna_where} = %s;"
                cursor.execute(update_sql, (novo_valor, inicio, fim, valor_where))
            else:
                cursor.execute(update_sql, (novo_valor, inicio, fim))
        else:
            if usar_where == 1 and coluna_where and valor_where:
                update_sql += f" WHERE {coluna_where} = %s;"
                cursor.execute(update_sql, (novo_valor, valor_where))
            else:
                update_sql += f";"
                cursor.execute(update_sql, (novo_valor,))

        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Atualizar", "Atualizacao realizada com sucesso!")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro na Atualização", f"Erro na atualização: {erro}")

def consultar():
    consultar_window = tk.Toplevel(root)
    consultar_window.title("Consultar")
    consultar_window.geometry("500x300")
    consultar_window.configure(bg="#f0f0f0")

    frame_consulta = tk.Frame(consultar_window, bg="white", padx=20, pady=20, borderwidth=2, relief=tk.SOLID)
    frame_consulta.pack(pady=10, padx=10)

    tabela_label = tk.Label(frame_consulta, text="Digite o nome da tabela que deseja consultar:", font=("Arial", 12), bg="white")
    tabela_label.pack(pady=5)

    tabela_entry = tk.Entry(frame_consulta, font=("Arial", 12))
    tabela_entry.pack()

    usar_where_var = tk.IntVar()
    usar_where_checkbox = tk.Checkbutton(frame_consulta, text="Deseja usar a cláusula WHERE?", variable=usar_where_var, font=("Arial", 12), bg="white")
    usar_where_checkbox.pack()

    condicao_label = tk.Label(frame_consulta, text="Digite a condição WHERE (sem 'WHERE campo=valor'):", font=("Arial", 12), bg="white")
    condicao_entry = tk.Entry(frame_consulta, font=("Arial", 12))
    condicao_label.pack(pady=5)
    condicao_entry.pack()

    consultar_button = tk.Button(frame_consulta, text="Consultar", command=lambda: realizar_consulta(tabela_entry, usar_where_var, condicao_entry, resultado_text), font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, padx=10)
    consultar_button.pack(pady=20)

    resultado_text = tk.Text(consultar_window, height=10, width=40, font=("Arial", 12), bg="white", bd=0)
    resultado_text.pack(pady=10)

def deletar():
    deletar_window = tk.Toplevel(root)
    deletar_window.title("Deletar")
    deletar_window.geometry("500x200")
    deletar_window.configure(bg="#f0f0f0")

    frame_deletar = tk.Frame(deletar_window, bg="white", padx=20, pady=20, borderwidth=2, relief=tk.SOLID)
    frame_deletar.pack(pady=10, padx=10)

    tabela_label = tk.Label(frame_deletar, text="Digite o nome da tabela que deseja deletar:", font=("Arial", 12), bg="white")
    tabela_label.pack(pady=5)

    tabela_entry = tk.Entry(frame_deletar, font=("Arial", 12))
    tabela_entry.pack()

    usar_where_var = tk.IntVar()
    usar_where_checkbox = tk.Checkbutton(frame_deletar, text="Deseja usar a cláusula WHERE?", variable=usar_where_var, font=("Arial", 12), bg="white")
    usar_where_checkbox.pack()

    condicao_label = tk.Label(frame_deletar, text="Digite a condição WHERE (exemplo: campo=valor):", font=("Arial", 12), bg="white")
    condicao_entry = tk.Entry(frame_deletar, font=("Arial", 12))
    condicao_label.pack(pady=5)
    condicao_entry.pack()

    deletar_button = tk.Button(frame_deletar, text="Deletar", command=lambda: realizar_delete(tabela_entry, usar_where_var, condicao_entry), font=("Arial", 12), bg="#FF5722", fg="white", bd=0, padx=10)
    deletar_button.pack()

def atualizar():
    atualizar_window = tk.Toplevel(root)
    atualizar_window.title("Atualizar")
    atualizar_window.geometry("500x400")
    atualizar_window.configure(bg="#f0f0f0")

    frame_atualizar = tk.Frame(atualizar_window, bg="white", padx=20, pady=20, borderwidth=2, relief=tk.SOLID)
    frame_atualizar.pack(pady=10, padx=10)

    tabela_label = tk.Label(frame_atualizar, text="Digite o nome da tabela que deseja atualizar:", font=("Arial", 12), bg="white")
    tabela_label.pack(pady=5)

    tabela_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    tabela_entry.pack()

    coluna_label = tk.Label(frame_atualizar, text="Digite o nome da coluna a ser atualizada:", font=("Arial", 12), bg="white")
    coluna_label.pack(pady=5)

    coluna_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    coluna_entry.pack()

    novo_valor_label = tk.Label(frame_atualizar, text="Digite o novo valor para a coluna:", font=("Arial", 12), bg="white")
    novo_valor_label.pack(pady=5)

    novo_valor_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    novo_valor_entry.pack()

    usar_between_var = tk.IntVar()
    usar_between_checkbox = tk.Checkbutton(frame_atualizar, text="Deseja usar a cláusula BETWEEN?", variable=usar_between_var, font=("Arial", 12), bg="white")
    usar_between_checkbox.pack()

    nome_coluna_between_label = tk.Label(frame_atualizar, text="Digite o nome da coluna com a condição BETWEEN:", font=("Arial", 12), bg="white")
    nome_coluna_between_label.pack(pady=5)

    nome_coluna_between_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    nome_coluna_between_entry.pack()

    inicio_label = tk.Label(frame_atualizar, text="Digite o valor de início para o BETWEEN:", font=("Arial", 12), bg="white")
    inicio_label.pack(pady=5)

    inicio_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    inicio_entry.pack()

    fim_label = tk.Label(frame_atualizar, text="Digite o valor de fim para o BETWEEN:", font=("Arial", 12), bg="white")
    fim_label.pack(pady=5)

    fim_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    fim_entry.pack()

    usar_where_var = tk.IntVar()
    usar_where_checkbox = tk.Checkbutton(frame_atualizar, text="Deseja usar a cláusula WHERE?", variable=usar_where_var, font=("Arial", 12), bg="white")
    usar_where_checkbox.pack()

    coluna_where_label = tk.Label(frame_atualizar, text="Digite o nome da coluna para a cláusula WHERE:", font=("Arial", 12), bg="white")
    coluna_where_label.pack(pady=5)

    coluna_where_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    coluna_where_entry.pack()

    valor_where_label = tk.Label(frame_atualizar, text="Digite o valor para a cláusula WHERE:", font=("Arial", 12), bg="white")
    valor_where_label.pack(pady=5)

    valor_where_entry = tk.Entry(frame_atualizar, font=("Arial", 12))
    valor_where_entry.pack()

    atualizar_button = tk.Button(frame_atualizar, text="Atualizar", command=lambda: realizar_update(tabela_entry, coluna_entry, novo_valor_entry, usar_between_var,
                    nome_coluna_between_entry, inicio_entry, fim_entry,
                    usar_where_var, coluna_where_entry, valor_where_entry), font=("Arial", 12), bg="#2196F3", fg="white", bd=0, padx=10)
    atualizar_button.pack(pady=20)

root = tk.Tk()
root.title("Interface para Banco de Dados")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

consultar_button = tk.Button(root, text="Consultar", command=consultar, font=("Arial", 12), bg="#4CAF50", fg="white", bd=0, padx=10)
consultar_button.pack(pady=10)

deletar_button = tk.Button(root, text="Deletar", command=deletar, font=("Arial", 12), bg="#FF5722", fg="white", bd=0, padx=10)
deletar_button.pack(pady=10)

atualizar_button = tk.Button(root, text="Atualizar", command=atualizar, font=("Arial", 12), bg="#2196F3", fg="white", bd=0, padx=10)
atualizar_button.pack(pady=10)

root.mainloop()
