document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);

    const successMessage = urlParams.get('success');
    const errorMessage = urlParams.get('error');
    const rechazarPedido = urlParams.get('pedido_rechazado')
    if (successMessage) {
        swal("Éxito", successMessage, "success");
    } else if (errorMessage) {
        swal("Error", errorMessage, "error");
    } else if (rechazarPedido) {
        swal("Rechazado", rechazarPedido, "error");

    }
});