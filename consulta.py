# Importando a função "conectar" do arquivo "conexao.py"
from conexao import conectar
import mysql.connector

def realizar_consulta(conexao, nome_tabela):
    try:
        cursor = conexao.cursor(prepared=True)

        # Solicitar ao usuário se deseja usar a cláusula WHERE
        usar_where = input("Deseja usar a cláusula WHERE? (S/N): ").strip().lower()

        # Montar a consulta SQL
        consulta_sql = f"SELECT * FROM {nome_tabela}"
        if usar_where == "s":
            condicao = input("Digite a condição WHERE (sem 'WHERE campo=valor'): ")
            consulta_sql += f" WHERE {condicao}"

        # Executar a consulta SQL
        cursor.execute(consulta_sql)

        # Recuperar os resultados e exibi-los
        resultados = cursor.fetchall()
        if resultados:
            for resultado in resultados:
                print(resultado)
        else:
            print("Nenhum resultado encontrado.")

        cursor.close()

    except mysql.connector.Error as erro:
        print(f"Erro na consulta: {erro}")

if __name__ == "__main__":
    conexao = conectar()
    if conexao:
        nome_tabela = input("Digite o nome da tabela que deseja consultar: ")
        realizar_consulta(conexao, nome_tabela)
        conexao.close()
