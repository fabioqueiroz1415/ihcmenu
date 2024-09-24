function incrementar_quantidade(item, i) {
  var data = {
    id_mesa: item.id_mesa,
    id_item: item.id_item,
    incremento: i
  };
  
  var quantidade = parseInt(document.getElementById(`qtd-item-${data.id_item}`).textContent);
  if((quantidade + i) > 0) {
    incrementar_quantidade_servidor(data);
  } else {
    deletar_pedido_carrinho_servidor(data);
  }
}

function deletar_pedido_carrinho_servidor(data) {
  fetch('/deletar-pedido-carrinho', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(d => {
    if (d.status === 200) {
      document.getElementById(`item-${data.id_item}`).remove();
      var old_total = parseFloat(document.getElementById('total').textContent);
      document.getElementById('total').textContent = (old_total - parseFloat(d.valor_decrementado)).toFixed(2);
    }
  })
  .catch((error) => {
    console.error(error);
  });
}

function incrementar_quantidade_servidor(data) {
  fetch('/incrementar-quantidade-carrinho', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => response.json())
  .then(d => {
    if (d.status === 200) {
      document.getElementById(`qtd-item-${data.id_item}`).textContent = d.quantidade;
      var old_total = parseFloat(document.getElementById('total').textContent);
      document.getElementById('total').textContent = (old_total + parseFloat(d.valor_incrementado)).toFixed(2);
    }
  })
  .catch((error) => {
    console.error(error);
  });
}

function limpar_carrinho(id_mesa) {
  var data = {
    id_mesa: id_mesa
  };
  fetch('/limpar-carrinho', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .then(d => {
    if (d.status === 200) {
      document.getElementById('carrinho-content').innerHTML = '';
      document.getElementById('total').textContent = '0.00';
    }
  })
}

function enviar_pedido(id_mesa) {
  var data = {
    id_mesa: id_mesa
  };
  fetch('/post-pedido', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(response => response.json())
  .then(d => {
    if (d.status === 200) {
      limpar_carrinho(id_mesa);
    }
  })
}