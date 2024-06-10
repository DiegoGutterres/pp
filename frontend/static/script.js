document.addEventListener('DOMContentLoaded', function() {
    var botaoArquivo = document.getElementById('botaoArquivo');
    var inputArquivo = document.getElementById('inputArquivo');
    var nomeArquivo = document.getElementById('nomeArquivo');

    botaoArquivo.addEventListener('click', function() {
        inputArquivo.click();
    });

    inputArquivo.addEventListener('change', function() {
        if (inputArquivo.files.length > 0) {
            var arquivoSelecionado = inputArquivo.files[0].name;
            nomeArquivo.textContent = "Arquivo selecionado: " + arquivoSelecionado;
            botaoArquivo.textContent = ">"        

            // Crie um FormData para enviar o arquivo via AJAX
            var formData = new FormData();
            formData.append('file', inputArquivo.files[0]);

            // Envie o arquivo via AJAX
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            nomeArquivo.textContent = "";
            botaoArquivo.textContent = "Upload"        

        }
    });
});