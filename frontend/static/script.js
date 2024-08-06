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


document.getElementById('retrieveButton').addEventListener('click', function() {
    fetch('/retrieve')
    .then(response => response.json())
    .then(data => {
        let recordList = document.getElementById('recordList');
        recordList.innerHTML = '';
        data.data.forEach(record => {
            let listItem = document.createElement('li');
            listItem.textContent = record.conteudo;
            recordList.appendChild(listItem);
        });
    })
    .catch((error) => {
        console.error('Erro ao recuperar os registros:', error);
    });
});