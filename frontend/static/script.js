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
document.getElementById('nextButton').addEventListener('click', function() {
    //cria um objeto formdata a partir do q foi dado upload
    var formData = new FormData(document.getElementById('uploadForm'));
    //manda o arquivo p servidor na rota upload
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    //converte a resposta p json
    .then(response => {
        console.log('Raw response:', response);
        return response.json();
    })

    //verifica se o upload deu bao e manda p pagina de response se sim
    .then(data => {
        console.log('Parsed response:', data);
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
});



// botao de camera, faz um click nobotao invisivel
document.getElementById('cameraButton').addEventListener('click', function() {
    document.getElementById('inputCamera').click();
});


document.getElementById('inputCamera').addEventListener('change', function(event) {
    //cria uma variavel p ver a file
    const file = event.target.files[0];
    if (file) {
        //cria dnv mais um formdata
        const formData = new FormData();
        //coloca  afile dentro do objetio
        formData.append('file', file);

        // Enviar a imagem para o servidor Flask
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        //transforma a resposta em json
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirecionar ou exibir a resposta processada
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
