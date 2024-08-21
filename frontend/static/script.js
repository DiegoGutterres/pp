document.getElementById('botaoArquivo').addEventListener('click', function() {
    document.getElementById('inputArquivo').click();
});

document.getElementById('inputArquivo').addEventListener('change', function(event) {
    const fileName = event.target.files[0].name;
    document.getElementById('nomeArquivo').innerText = fileName;
    document.getElementById('botaoArquivo').style.display = 'none';
    document.getElementById('nextButton').style.display = 'block';
});

document.getElementById('nextButton').addEventListener('click', function() {
    var formData = new FormData(document.getElementById('uploadForm'));
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        console.log('Raw response:', response);
        return response.json();
    })
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



// botao de camera

document.getElementById('cameraButton').addEventListener('click', function() {
    document.getElementById('inputCamera').click();
});


document.getElementById('inputCamera').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        // Enviar a imagem para o servidor Flask
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
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
