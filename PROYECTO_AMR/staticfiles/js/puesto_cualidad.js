document.addEventListener("DOMContentLoaded", () => {
    const editButtons = document.querySelectorAll(".edit-button");
    const modalForm = document.getElementById("editForm");
    const modalPuesto = document.getElementById("modalPuesto");
    const modalCualidad = document.getElementById("modalCualidad");
    const modalPeso = document.getElementById("modalPeso");

    editButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const id = button.getAttribute("data-id");
            const puesto = button.getAttribute("data-puesto");
            const cualidad = button.getAttribute("data-cualidad");
            const peso = button.getAttribute("data-peso");

            modalForm.action = `/cualidad_puesto/editar/${id}/`;
            modalPuesto.value = puesto;
            modalCualidad.value = cualidad;
            modalPeso.value = peso;
        });
    });
});
