import sqlite3

def post_pedido_carrinho(data):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO carrinho (item, quantidade, id_item, id_mesa, valor)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['item'], data['quantidade'], data['id_item'], data['id_mesa'], data['valor']))

    conn.commit()

    return {'message': 'Pedido adicionado com sucesso', 'status': 200}

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}

  finally:
    conn.close()

def get_carrinho(id_mesa):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM carrinho WHERE id_mesa = ?
    ''', (id_mesa,))

    carrinho = cursor.fetchall()
    colunas = ['id_mesa', 'item', 'quantidade', 'id_item', 'valor']
    
    #convertendo lista de tuplas para lista de dicionários
    carrinho_dict = [dict(zip(colunas, row)) for row in carrinho]
    return carrinho_dict

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return []

  finally:
    conn.close()

def post_pedido(data):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
      INSERT INTO pedidos (id_mesa) VALUES (?)
      ''', (data['id_mesa'],))
    id_pedido = cursor.lastrowid
    
    for item in data['itens']:
      cursor.execute('''
        INSERT INTO itens_pedido (id_mesa, id_item, item, quantidade, valor, id_pedido) 
        VALUES (?, ?, ?, ?, ?, ?)
      ''', (data['id_mesa'], item['id_item'], item['item'], item['quantidade'], item['valor'], id_pedido))
    conn.commit()

    return {'message': 'Pedido adicionado com sucesso', 'status': 200}
  except sqlite3.Error as e:
    conn.rollback()
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}
  finally:
    conn.close()

def get_pedidos_mesa(id_mesa):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
            SELECT p.id_pedido, i.id_item, i.item, i.valor, i.quantidade, p.data_hora, p.id_mesa
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            WHERE p.id_mesa = ?
            ORDER BY p.data_hora DESC
        ''', (id_mesa,))

    rows = cursor.fetchall()
    pedidos_dict = {}
    i = 0
    for row in rows:
      id_pedido = row[0]
      if id_pedido not in pedidos_dict:
        pedidos_dict[id_pedido] = {
          'id_pedido': id_pedido,
          'id_mesa': id_mesa,
          'data_hora': row[5],
          'itens': []
        }
      item_data = {
        'id_item': row[1],
        'item': row[2],
        'valor': row[3],
        'quantidade': row[4]
      }
      pedidos_dict[id_pedido]['itens'].append(item_data)

    return list(pedidos_dict.values())

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return []

  finally:
    conn.close()
    
def get_pedidos():
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
            SELECT i.id, p.id_pedido, i.id_item, i.item, i.valor, i.quantidade, p.data_hora, p.id_mesa, i.situacao
            FROM pedidos p
            JOIN itens_pedido i ON p.id_pedido = i.id_pedido
            ORDER BY p.id_mesa ASC, p.data_hora ASC
        ''')

    rows = cursor.fetchall()
    pedidos_dict = {}
    i = 0
    for row in rows:
      id_pedido = row[1]
      if id_pedido not in pedidos_dict:
        pedidos_dict[id_pedido] = {
          'id_pedido': id_pedido,
          'id_mesa': row[7],
          'data_hora': row[6],
          'itens': []
        }
      item_data = {
        'id': row[0],
        'id_item': row[2],
        'item': row[3],
        'valor': row[4],
        'quantidade': row[5],
        'situacao': row[8]
      }
      pedidos_dict[id_pedido]['itens'].append(item_data)

    return list(pedidos_dict.values())

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return []

  finally:
    conn.close()

def delete_pedido_carrinho(data):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM carrinho WHERE id_mesa = ? AND id_item = ?
    ''', (data['id_mesa'], data['id_item']))
    conn.commit()

    return {'message': 'Pedido deletado com sucesso', 'status': 200}

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}

  finally:
    conn.close()
    
def incrementar_quantidade(data):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE carrinho SET quantidade = quantidade + ? WHERE id_mesa = ? AND id_item = ?
    ''', (data['incremento'], data['id_mesa'], data['id_item']))
    conn.commit()

    return {'message': 'Quantidade incrementada com sucesso', 'status': 200}

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}

  finally:
    conn.close()
    
def deletar_carrinho(data):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM carrinho WHERE id_mesa = ?
    ''', (data['id_mesa'],))
    conn.commit()

    return {'message': 'Carrinho deletado com sucesso', 'status': 200}

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}

  finally:
    conn.close()

def finalizar_pedido(id_pedido):
  try:
    conn = sqlite3.connect('database/database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE itens_pedido SET situacao = 'finalizado' WHERE id_pedido = ?
    ''', (id_pedido,))
    conn.commit()

    return {'message': 'Pedido finalizado com sucesso', 'status': 200}

  except sqlite3.Error as e:
    print(f"Erro ao acessar banco de dados: {e}")
    return {'message': f'{e}', 'status': 500}

  finally:
    conn.close()