from conexao import conectar
import mysql.connector

def realizar_delete(conexao, nome_tabela):
    try:
        cursor = conexao.cursor(prepared=True)

        # Solicitar ao usuário se deseja usar a cláusula WHERE
        usar_where = input("Deseja usar a cláusula WHERE? (S/N): ").strip().lower()

        # Montar a consulta SQL
        delete_sql = f"DELETE FROM {nome_tabela}"
        if usar_where == "s":
            condicao = input("Digite a condição WHERE (exemplo: campo=valor): ")
            delete_sql += f" WHERE {condicao}"

        cursor.execute(delete_sql)
        conexao.commit()

        print("Delete realizado com sucesso!")

        cursor.close()

    except mysql.connector.Error as erro:
        print(f"Erro na consulta: {erro}")

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        nome_tabela = input("Digite o nome da tabela que deseja deletar: ")
        realizar_delete(conexao, nome_tabela)
        conexao.close()
