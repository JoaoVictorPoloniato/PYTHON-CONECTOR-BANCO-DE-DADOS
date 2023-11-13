from conexao import conectar
import mysql.connector

def realizar_insert(conexao, nome_tabela, filial_id, nome, cgc, inscr, uf):
    try:
        cursor = conexao.cursor(prepared=True)
        filial_id = int(input('Digite qual será o ID da loja: '))
        nome = input("Digite o nome fantasia da loja: ")
        cgc = int(input("Digite o CNPJ da loja do cliente: (não pode conter pontos ou traços)"))
        inscr = input("Digite a IE da loja do cliente: (não pode conter pontos ou traços)")
        uf = str(input("Digite a UF da loja do cliente: (apenas as duas primeiras MT exemplo)"))
        
        sql_insert = f'INSERT INTO {nome_tabela} (filial_id, nome, cgc, inscr, uf) VALUES (%s, %s, %s, %s, %s)'
        valores = (filial_id, nome, cgc, inscr, uf)
        cursor.execute(sql_insert, valores)
        conexao.commit()
        print("Criada Filial corretamente")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir dados {err}")
conexao = conectar()
realizar_insert(conexao, 'filial')
conexao.close()
