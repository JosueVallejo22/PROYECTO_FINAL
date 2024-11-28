document.addEventListener('DOMContentLoaded', () => {
    // Inicializar el mapa
    const map = L.map('map').setView([20, 0], 2); // Coordenadas iniciales y nivel de zoom
    let marker = null; // Variable para el marcador

    // Agregar el tile layer de OpenStreetMap
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map);
    
    

    // Función para mover el marcador al hacer clic en el mapa o seleccionar un país
    const setMarker = (lat, lng) => {
        if (marker) {
            marker.setLatLng([lat, lng]); // Mover marcador existente
        } else {
            marker = L.marker([lat, lng]).addTo(map); // Crear un nuevo marcador
        }
        map.setView([lat, lng], 5); // Centrar el mapa en la ubicación
    };

    // Manejar clics en el mapa
    map.on('click', async (e) => {
        const { lat, lng } = e.latlng;
        try {
            // Consultar la API de OpenStreetMap para obtener el nombre del país
            const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`);
            const data = await response.json();
            if (data && data.address && data.address.country) {
                document.getElementById('id_pais').value = data.address.country; // Asignar país al input
                setMarker(lat, lng); // Actualizar marcador en el mapa
            } else {
                Swal.fire({
                    icon: 'error', // Ícono de error
                    title: 'Error de ubicación',
                    text: 'No se pudo determinar el país en esta ubicación. Intente de nuevo.',
                    confirmButtonColor: '#d33', // Color del botón (rojo para errores)
                    confirmButtonText: 'Aceptar'
                });
                            }
        } catch (error) {
            console.error('Error al obtener datos del país:', error);
            Swal.fire({
                icon: 'error', // Ícono de error
                title: 'Consulta fallida',
                text: 'Error al consultar el país. Intente más tarde.',
                confirmButtonColor: '#d33', // Color del botón (rojo para errores)
                confirmButtonText: 'Aceptar'
            });
        }
    });

    // Si ya existe un país seleccionado (modo edición), centrar el mapa en ese país
    const paisInput = document.getElementById('id_pais');
    if (paisInput && paisInput.value) {
        const selectedCountry = paisInput.value;
        fetch(`https://nominatim.openstreetmap.org/search?country=${selectedCountry}&format=json`)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const { lat, lon } = data[0];
                    setMarker(lat, lon); // Colocar marcador en el país cargado
                } else {
                    console.warn('No se pudo localizar el país en el mapa:', selectedCountry);
                }
            })
            .catch(error => console.error('Error al buscar el país:', error));
    }

    // Configuración del autocompletado
    if (paisInput) {
        $(paisInput).autocomplete({
            source: async (request, response) => {
                try {
                    const res = await fetch(`/api/paises?q=${request.term}`);
                    const data = await res.json();
                    response(data.map(pais => pais.pais));
                } catch (error) {
                    console.error('Error al cargar los países:', error);
                    response([]);
                }
            },
            minLength: 2, // Activar después de escribir 2 caracteres
            select: async (event, ui) => {
                paisInput.value = ui.item.value;
                // Buscar el país en el mapa y centrarlo
                try {
                    const res = await fetch(`https://nominatim.openstreetmap.org/search?country=${ui.item.value}&format=json&accept-language=es`);
                    const data = await res.json();
                    if (data && data.length > 0) {
                        const { lat, lon } = data[0];
                        setMarker(lat, lon);
                    } else {
                        console.warn('No se encontró el país en el mapa:', ui.item.value);
                    }
                } catch (error) {
                    console.error('Error al buscar el país:', error);
                }
            }
        });
    }
});
