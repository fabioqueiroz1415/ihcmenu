import pymysql

host = 'ihcmenu.mysql.pythonanywhere-services.com'
user = 'ihcmenu'
password = 'p1a4s1s5w9o'
name = 'ihcmenu$default'

conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def post_pedido_carrinho(data):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO carrinho (item, quantidade, id_item, id_mesa, valor)
            VALUES (%s, %s, %s, %s, %s)
        ''', (data['item'], data['quantidade'], data['id_item'], data['id_mesa'], data['valor']))

        conn.commit()

        return {'message': 'Pedido adicionado com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()


def get_carrinho(id_mesa):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM carrinho WHERE id_mesa = %s
        ''', (id_mesa,))

        carrinho = cursor.fetchall()
        colunas = ['id_mesa', 'item', 'quantidade', 'id_item', 'valor']
        
        # Convertendo lista de tuplas para lista de dicionários
        carrinho_dict = [dict(zip(colunas, row)) for row in carrinho]
        return carrinho_dict

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return []

    finally:
        conn.close()


def post_pedido(data):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO pedidos (id_mesa) VALUES (%s)
        ''', (data['id_mesa'],))
        id_pedido = cursor.lastrowid

        for item in data['itens']:
            cursor.execute('''
                INSERT INTO itens_pedido (id_mesa, id_item, item, quantidade, valor, id_pedido) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (data['id_mesa'], item['id_item'], item['item'], item['quantidade'], item['valor'], id_pedido))

        conn.commit()

        return {'message': 'Pedido adicionado com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        conn.rollback()
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()


def get_pedidos_mesa(id_mesa):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT p.id_pedido, i.id_item, i.item, i.valor, i.quantidade, p.data_hora, p.id_mesa
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            WHERE p.id_mesa = %s
            ORDER BY p.data_hora DESC
        ''', (id_mesa,))

        rows = cursor.fetchall()
        pedidos_dict = {}

        for row in rows:
            id_pedido = row['id_pedido']
            if id_pedido not in pedidos_dict:
                pedidos_dict[id_pedido] = {
                    'id_pedido': id_pedido,
                    'id_mesa': id_mesa,
                    'data_hora': row['data_hora'],
                    'itens': []
                }
            item_data = {
                'id_item': row['id_item'],
                'item': row['item'],
                'valor': row['valor'],
                'quantidade': row['quantidade']
            }
            pedidos_dict[id_pedido]['itens'].append(item_data)

        return list(pedidos_dict.values())

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return []

    finally:
        conn.close()


def get_pedidos():
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT i.id, p.id_pedido, i.id_item, i.item, i.valor, i.quantidade, p.data_hora, p.id_mesa, i.situacao
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            ORDER BY p.id_mesa ASC, p.data_hora ASC
        ''')

        rows = cursor.fetchall()
        pedidos_dict = {}

        for row in rows:
            id_pedido = row['id_pedido']
            if id_pedido not in pedidos_dict:
                pedidos_dict[id_pedido] = {
                    'id_pedido': id_pedido,
                    'id_mesa': row['id_mesa'],
                    'data_hora': row['data_hora'],
                    'itens': []
                }
            item_data = {
                'id': row['id'],
                'id_item': row['id_item'],
                'item': row['item'],
                'valor': row['valor'],
                'quantidade': row['quantidade'],
                'situacao': row['situacao']
            }
            pedidos_dict[id_pedido]['itens'].append(item_data)

        return list(pedidos_dict.values())

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return []

    finally:
        conn.close()


def delete_pedido_carrinho(data):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM carrinho WHERE id_mesa = %s AND id_item = %s
        ''', (data['id_mesa'], data['id_item']))
        conn.commit()

        return {'message': 'Pedido deletado com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()

def incrementar_quantidade(data):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE carrinho SET quantidade = quantidade + %s WHERE id_mesa = %s AND id_item = %s
        ''', (data['incremento'], data['id_mesa'], data['id_item']))
        conn.commit()

        return {'message': 'Quantidade incrementada com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()

def deletar_carrinho(data):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM carrinho WHERE id_mesa = %s
        ''', (data['id_mesa'],))
        conn.commit()

        return {'message': 'Carrinho deletado com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()

def finalizar_pedido(id_pedido):
    try:
        conn = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE itens_pedido SET situacao = 'finalizado' WHERE id_pedido = %s
        ''', (id_pedido,))
        conn.commit()

        return {'message': 'Pedido finalizado com sucesso', 'status': 200}

    except pymysql.MySQLError as e:
        print(f"Erro ao acessar banco de dados: {e}")
        return {'message': f'{e}', 'status': 500}

    finally:
        conn.close()

