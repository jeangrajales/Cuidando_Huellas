setTimeout(function() {
    const alerts = document.querySelectorAll('#notificaciones .alert');
    alerts.forEach(function(alert) {
    // Desvanece el mensaje (opcional)
    alert.classList.remove('show'); // Oculta con la animación de Bootstrap
    alert.classList.add('fade');
    
    // Lo elimina completamente después de la animación
    setTimeout(function() {
        alert.remove();
    }, 900); // Tiempo para que termine la animación fade
    }); 
}, 2000);