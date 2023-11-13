from conexao import conectar
import mysql.connector

def realizar_update(conexao, nome_tabela):
    try:
        cursor = conexao.cursor(prepared=True)

        usar_between = input("Deseja usar um início e um fim para o seu update? (S/N)").strip().lower()

        coluna_update = input("Digite o nome da coluna a ser atualizada: ").strip()
        novo_valor = input("Digite o novo valor para a coluna: ").strip()

        update_sql = f"UPDATE {nome_tabela} SET {coluna_update} = %s"

        if usar_between == "s":
            nome_coluna_between = input("Digite o nome da coluna com a condição BETWEEN: ").strip()
            inicio = input("Digite o valor de início para o BETWEEN: ").strip()
            fim = input("Digite o valor de fim para o BETWEEN: ").strip()
            update_sql += f" WHERE {nome_coluna_between} BETWEEN %s AND %s"
            if input("Deseja adicionar uma cláusula adicional no WHERE? (S/N)").strip().lower() == "s":
                coluna_where = input("Digite o nome da coluna para a cláusula adicional: ").strip()
                valor_where = input("Digite o valor para a cláusula adicional: ").strip()
                update_sql += f" AND {coluna_where} = %s;"
                cursor.execute(update_sql, (novo_valor, inicio, fim, valor_where))
            else:
                update_sql += ";"
                cursor.execute(update_sql, (novo_valor, inicio, fim))
        else:
            if input("Deseja adicionar uma cláusula WHERE no update? (S/N)").strip().lower() == "s":
                coluna_where = input("Digite o nome da coluna para a cláusula WHERE: ").strip()
                valor_where = input("Digite o valor para a cláusula WHERE: ").strip()
                update_sql += f" WHERE {coluna_where} = %s;"
                cursor.execute(update_sql, (novo_valor, valor_where))
            else:
                update_sql += ";"
                cursor.execute(update_sql, (novo_valor,))

        conexao.commit()  # Importante para aplicar a atualização no banco de dados

        print("Atualização realizada com sucesso!")

    except mysql.connector.Error as erro:
        print(f"Erro na atualização: {erro}")

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        nome_tabela = input("Digite o nome da tabela em que deseja realizar a atualização: ")
        realizar_update(conexao, nome_tabela)
        conexao.close()
