document.getElementById('startButton').addEventListener('click', function() {
    window.location.href = '/index.html';
});

window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    const mainContent = document.getElementById('how-it-works');

    // Simular um carregamento (tempo de 3 segundos)
    setTimeout(function() {
        preloader.style.display = 'none';
        mainContent.style.display = 'block';
    }, 3000); // Tempo em milissegundos
});
