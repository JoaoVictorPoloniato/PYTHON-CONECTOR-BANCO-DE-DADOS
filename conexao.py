import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456big',
            database='gerente'
        )
        print("Conexão bem-sucedida!")
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar: {erro}")
        return None

