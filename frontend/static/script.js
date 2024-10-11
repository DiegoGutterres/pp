//clicar no input invisivel que tem em baixo do botao de upload
document.getElementById('botaoArquivo').addEventListener('click', function() {
    document.getElementById('inputArquivo').click();
});

//atualizar com o arquivo q foi inputado
document.getElementById('inputArquivo').addEventListener('change', function(event) {
    //define qual arquivo q foi inputado e troca o display do input p aparecer la
    const fileName = event.target.files[0].name;
    document.getElementById('nomeArquivo').innerText = fileName;
    document.getElementById('botaoArquivo').style.display = 'none';
    document.getElementById('nextButton').style.display = 'block';
});

//quando clica no next, ele vai fazer uma req pro servidor
// Adicionar um event listener ao botão de upload de arquivo
document.getElementById('nextButton').addEventListener('click', function() {
    // Exibir a tela de carregamento
    document.getElementById('loading-screen').style.display = 'flex';

    // Cria um objeto formData a partir do formulário de upload
    var formData = new FormData(document.getElementById('uploadForm'));

    // Envia o arquivo para o servidor na rota /upload
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Verifica se o upload foi bem-sucedido
        if (data.success) {
            // Redireciona para a página de resposta
            window.location.href = '/response.html';
        } else {
            // Exibe um erro se houver falha no upload
            alert('Erro no upload: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro no upload');
    });
});

// Botão de câmera, faz um clique no botão invisível
document.getElementById('cameraButton').addEventListener('click', function() {
    document.getElementById('inputCamera').click();
});

document.getElementById('inputCamera').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        // Exibe a tela de carregamento
        document.getElementById('loading-screen').style.display = 'flex';

        const formData = new FormData();
        formData.append('file', file);

        // Enviar a imagem para o servidor
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/response.html';
            } else {
                alert('Erro no upload: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro no upload');
        });
    }
});


