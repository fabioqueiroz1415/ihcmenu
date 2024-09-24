from flask import Flask, render_template, request, jsonify
import database.database as database
import json

from config import IDS_TO_TABLES
app = Flask(__name__)

carrinho_mesas = {
    "1": [],
    "2": [],
    "3": [],
    "4": [],
    "5": [],
    "6": [],
    "7": [],
    "8": [],
    "9": [],
    "10": []
}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#para servir o menu
@app.route('/principal.html/<path:id_mesa>', methods=['GET'])
def menu_principal(id_mesa):
    return render_template('principal.html', id_mesa=id_mesa)

@app.route('/secundario.html/<path:id_mesa>', methods=['GET'])
def menu_secundario(id_mesa):
    return render_template('secundario.html', id_mesa=id_mesa)

@app.route('/sobremesa.html/<path:id_mesa>', methods=['GET'])
def menu_sobremesa(id_mesa):
    return render_template('sobremesa.html', id_mesa=id_mesa)

@app.route('/promocoes.html/<path:id_mesa>', methods=['GET'])
def menu_promocoes(id_mesa):
    return render_template('promocoes.html', id_mesa=id_mesa)

@app.route('/bebNaoAlc.html/<path:id_mesa>', methods=['GET'])
def menu_beb_nao_alc(id_mesa):
    return render_template('bebNaoAlc.html', id_mesa=id_mesa)

@app.route('/bebAlc.html/<path:id_mesa>', methods=['GET'])
def menu_beb_alc(id_mesa):
    return render_template('bebAlc.html', id_mesa=id_mesa)

@app.route('/carrinho.html/<path:id_mesa>', methods=['GET'])
def menu_carrinho(id_mesa):
    total = 0.0
    for p in carrinho_mesas[str(id_mesa)]:
        total += float(p['valor']) * p['quantidade']
    return render_template('carrinho.html', carrinho=carrinho_mesas[str(id_mesa)], id_mesa=id_mesa, valor_total=format(total, '.2f'))

# rota para as mesas
@app.route('/m/<path:subpath>', methods=['GET'])
def home(subpath):
    table_id = IDS_TO_TABLES.get(subpath, None)
    if table_id:
        return render_template('index.html', id_mesa=table_id, carrinho=carrinho_mesas[str(table_id)])
    else:
        return 'PAGINA NÃO ENCONTRADA'
    
@app.route('/cozinha', methods=['GET'])
def vendedor():
    return render_template('cozinha.html')

@app.route('/post-pedido-carrinho', methods=['POST'])
def post_pedido_carrinho():
    global carrinho_mesas
    data = request.get_json()
    id_mesa = data['id_mesa']
    for p in carrinho_mesas[str(id_mesa)]: 
        if p['id_item'] == data['id_item']:
            p['quantidade'] += data['quantidade']
            return {'status': 200}
    carrinho_mesas[str(id_mesa)].append(data)
    return {'status': 200}

@app.route('/deletar-pedido-carrinho', methods=['POST'])
def deletar_pedido_carrinho():
    global carrinho_mesas
    data = request.get_json()
    id_mesa = data['id_mesa']
    for p in carrinho_mesas[str(id_mesa)]: 
        if p['id_item'] == data['id_item']:
            carrinho_mesas[str(id_mesa)].remove(p)
            return {'status': 200, 'quantidade': p['quantidade'], 'valor_decrementado': p['quantidade'] * float(p['valor'])}
    return {'status': 204}

@app.route('/post-pedido', methods=['POST'])
def post_pedido():
    data = request.get_json()
    id_mesa = data['id_mesa']
    pedido = {
        'id_mesa': id_mesa,
        'itens': carrinho_mesas[str(id_mesa)]
    }
    return database.post_pedido(pedido)

@app.route('/get-carrinho', methods=['GET'])
def get_carrinho():
    id_mesa = request.args.get('id_mesa')
    return database.get_carrinho(id_mesa)

@app.route('/get-pedidos-mesa', methods=['GET'])
def get_pedidos_mesa():
    id_mesa = request.args.get('id_mesa')
    return database.get_pedidos_mesa(id_mesa)

@app.route('/get-pedidos', methods=['GET'])
def get_pedidos():
    return database.get_pedidos()

@app.route('/incrementar-quantidade-carrinho', methods=['POST'])
def incrementar_quantidade():
    global carrinho_mesas
    data = request.get_json()
    id_mesa = data['id_mesa']
    for p in carrinho_mesas[str(id_mesa)]:
        if p['id_item'] == data['id_item']:
            p['quantidade'] += data['incremento']
            return {'status': 200, 'quantidade': p['quantidade'], 'valor_incrementado': data['incremento'] * float(p['valor'])}
    return {'status': 204}

@app.route('/limpar-carrinho', methods=['POST'])
def limpar_carrinho():
    global carrinho_mesas
    data = request.get_json()
    id_mesa = data['id_mesa']
    carrinho_mesas[str(id_mesa)] = []
    return {'status': 200}

@app.route('/finalizar-pedido/<path:id_pedido>', methods=['GET'])
def finailzar_pedido(id_pedido):
    return database.finalizar_pedido(id_pedido)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port='5000')