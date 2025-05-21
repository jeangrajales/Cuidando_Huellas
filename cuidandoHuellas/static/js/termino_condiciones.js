document.addEventListener('DOMContentLoaded', function() {
    const date = new Date();
    const formattedDate = date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
    document.getElementById('current-date').textContent = formattedDate;

    // Marcar automáticamente la casilla al hacer clic en Aceptar en el modal
    document.getElementById('acceptTermsBtn').addEventListener('click', function() {
        document.getElementById('termsCheck').checked = true;
    });

    // Validar que se acepten los términos antes de enviar el formulario
    document.querySelector('form').addEventListener('submit', function(e) {
        if (!document.getElementById('termsCheck').checked) {
        e.preventDefault();
        alert('Debe aceptar los Términos y Condiciones para registrarse');
        }
    });
});