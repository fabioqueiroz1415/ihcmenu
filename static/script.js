document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('.main a');
    const screenContent = document.getElementById('screen-content');

    links.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Impede o comportamento padrão de abrir um link
            const href = link.getAttribute('href');

            loadContent(href);
        });
    });

    function loadContent(href) {
        // Faz uma requisição para o arquivo HTML
        fetch(href)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(html => {
                // Insere o conteúdo HTML na div.screen
                screenContent.innerHTML = html;

                const scripts = screenContent.querySelectorAll('script');
                scripts.forEach(script => {
                    const newScript = document.createElement('script');
                    
                    if (script.src) {
                        newScript.src = script.src;
                        newScript.async = false;
                    } else {
                        newScript.textContent = script.textContent;
                    }

                    document.body.appendChild(newScript);
                })
            })
            .catch(error => {
                // Trata erros, como arquivos não encontrados
                screenContent.innerHTML = '<h1>Erro</h1><p>Não foi possível carregar o conteúdo.</p>';
                console.error('There was a problem with the fetch operation:', error);
            });
    }
    var id_mesa = document.body.id;
    loadContent(`/principal.html/${id_mesa}`);
});
