function get_filtro_pedidos() {
  const pendentes = document.getElementById('pendentes').checked;
  const finalizados = document.getElementById('finalizados').checked;

  return {
    pendentes,
    finalizados
  };
}

function atualizar_pedidos() {
  fetch(`/get-pedidos`)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    if (!data) {
      return;
    }

    for (var i = 1; i <= 10; i++) {
      var table = document.getElementById(`pedidos-mesa-${i}`);
      if (table) {
        removerMesa(i);
      }
    }

    data.forEach(pedido => {
      var num_itens_pedido = pedido.itens.length;
      const {pendentes, finalizados} = get_filtro_pedidos();
      const statusPedido = pedido.itens[0].situacao;

      if ((statusPedido === 'pendente' && pendentes) || (statusPedido === 'finalizado' && finalizados)
      ) {
        pedido.itens.forEach(item => {
          if (!document.getElementById(`pedidos-mesa-${pedido.id_mesa}`)) {
            criarMesa(pedido.id_mesa);
          }
          add_pedido_mesa_html(pedido.data_hora, pedido.id_mesa, item.item, item.quantidade, parseFloat(item.valor).toFixed(2), pedido.id_pedido, item.situacao, num_itens_pedido);
        })
    }
    });
  });
}

function removerMesa(id_mesa) {
  var container = document.getElementById('container-pedidos');
  container.innerHTML = '';
}

function criarMesa(id_mesa) {
  var container = document.getElementById('container-pedidos');
  table = document.createElement('table');
  table.id = `tabela-mesa-${id_mesa}`;
  table.classList.add('nao-selecionavel');
  table.innerHTML = `
  <thead>
    <tr>
      <th>item</th>
      <th>qtd</th>
      <th>und (R$)</th>
      <th>id pedido</th>
      <th>situação</th>
      <th>data hora</th>
    </tr>
  </thead>
  <tbody id="pedidos-mesa-${id_mesa}">
  </tbody>
  `;
  var tituloMesa = document.createElement('h2');
  tituloMesa.innerHTML = `Mesa ${id_mesa}`;
  tituloMesa.id = `Mesa ${id_mesa}`;
  tituloMesa.className = 'titulo-mesa';

  container.appendChild(tituloMesa)
  container.appendChild(table);
}

function add_pedido_mesa_html(data_hora, id_mesa, item, quantidade, valor, id_pedido, situacao, num_itens_pedido) {
  var table = document.getElementById(`pedidos-mesa-${id_mesa}`);
  var row = table.insertRow();
  var cell1 = row.insertCell(0);
  var cell2 = row.insertCell(1);
  var cell3 = row.insertCell(2);

  cell1.innerHTML = item;
  cell2.innerHTML = quantidade;
  cell3.innerHTML = valor;

  if (!document.getElementById(`celula-id-pedido-${id_pedido}`)) {
    var cell4 = row.insertCell(3);
    cell4.innerHTML = id_pedido;
    cell4.id = `celula-id-pedido-${id_pedido}`;
    cell4.rowSpan = num_itens_pedido;
  }

  if (!document.getElementById(`situacao-pedido-${id_pedido}`)) {
    var cell5 = row.insertCell(4);
    cell5.rowSpan = num_itens_pedido;
    cell5.innerHTML = `<button id="situacao-pedido-${id_pedido}" onclick="finalizar_pedido(${id_pedido})">${situacao}</button>`;

    var botao_situacao_pedido = document.getElementById(`situacao-pedido-${id_pedido}`);
    if(situacao === 'finalizado') {
      botao_situacao_pedido.disabled = true;
      botao_situacao_pedido.classList.add('pedido-finalizado');
    } else if (situacao === 'pendente') {
      botao_situacao_pedido.classList.add('pedido-pendente');
    }
  }

  if (!document.getElementById(`datahora-pedido-${id_pedido}`)) {
    var cell6 = row.insertCell(5);
    cell6.innerHTML = data_hora;
    cell6.id = `datahora-pedido-${id_pedido}`;
    cell6.rowSpan = num_itens_pedido;
  }
}

function finalizar_pedido(id_pedido) {
  fetch(`/finalizar-pedido/${id_pedido}`)
  .then(response => response.json())
  .then(data => {
    if (data.status == 'ok') {
      atualizar_pedidos();
    }
  });
}

addEventListener('load', function() {
  atualizar_pedidos();
  setInterval(atualizar_pedidos, 2000);
});
