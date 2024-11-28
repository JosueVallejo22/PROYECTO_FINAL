function openModal(button) {
    // Obtiene el ID y el nombre del jugador del enlace
    var jugadorId = button.getAttribute('data-jugador-id');
    var jugadorNombre = button.getAttribute('data-jugador-nombre');

    // Inserta el nombre del jugador en el modal
    document.getElementById('jugadorNombre').textContent = jugadorNombre;

    // Configura la URL de acción del formulario con el ID del jugador
    var deleteForm = document.getElementById('deleteForm');
    deleteForm.action = `/jugador/${jugadorId}/eliminar/`;  // Cambia esta URL según tus rutas
}



