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

// Botão de câmera para o QR Code, faz um clique no botão invisível
document.getElementById('cameraButtonQR').addEventListener('click', function() {
    document.getElementById('inputCameraQR').click();
});

document.getElementById('inputCameraQR').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('loading-screen').style.display = 'flex';

        const formData = new FormData();
        formData.append('file', file);

        fetch('/upload-qr', {
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

// Captura o valor do input e faz uma consulta ao servidor pelo ID do documento
document.getElementById('docIdButton').addEventListener('click', function() {
    const docId = document.querySelector('.doc-id input').value;
    document.getElementById('loading-screen').style.display = 'flex';


    if (docId) {
        // Envia o ID para o servidor
        fetch('/get_document_by_id', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },  
            body: JSON.stringify({ id: docId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Documento processado com sucesso');
                window.location.href = '/response.html';  // Redireciona para a página de resposta
            } else {
                alert('Erro ao processar o documento: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao consultar o banco de dados');
        });
    } else {
        alert('Por favor, insira um número válido.');
    }
});
