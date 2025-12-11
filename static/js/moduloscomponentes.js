document.getElementById("adminForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const urlDestino = document.getElementById("componentes").value;

    if (!urlDestino) {
        alert("Por favor selecciona un componente.");
        return;
    }

    window.location.href = urlDestino;
});