buttons = document.querySelectorAll('button');
buttons.forEach(function(button) {
  button.addEventListener('click', function() {
    id_mesa = document.body.id;
    const item = button.parentNode.parentNode;
    var id_item = item.id;
    var nome_item = item.querySelector('.description').textContent;
    var valor = button.value;
    var quantidade = 1;
    var path_imagem = item.querySelector('img').src;
    add_pedido_carrinho(id_mesa, nome_item, id_item, valor, quantidade, path_imagem);
  });
});

function add_pedido_carrinho(id_mesa, nome_item, id_item, valor, quantidade, path_imagem) {
  var data = {
    id_mesa: id_mesa,
    item: nome_item,
    id_item: id_item,
    valor: parseFloat(valor).toFixed(2),
    quantidade: quantidade,
    path_imagem: path_imagem
  };
  add_pedido_carrinho_servidor(data);
}

function add_pedido_carrinho_servidor(data) {
  fetch('/post-pedido-carrinho', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(d => {
    if (d.status === 200) {
      console.log('Pedido adicionado.');
    }
  })
  .catch((error) => {
    console.error(error);
  });
}
