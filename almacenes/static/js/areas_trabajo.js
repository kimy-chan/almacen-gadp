
document.getElementById('id_area_trabajo').addEventListener('click', (e) => {
    e.preventDefault()
    const formulario = document.getElementById('id_form_trabajo')
    axios.post('crear_aras_trabajo_listar', formulario)
        .then((resultado) => {
            if (resultado.data.error) {
                document.getElementById('error_trabajo').innerHTML = resultado.data.error
            } else if (resultado.data.data) {
                document.getElementById('error_trabajo').innerHTML = ''
                listar_areas_trabajo()

            }

        }).catch((err) => {
            alert("Error de seervdor")
        });
})
function listar_areas_trabajo() {
    axios.get('crear_aras_trabajo_listar')
        .then((resultado) => {
            tbody_table = document.getElementById('tbody_table_trabajo')
            tbody_table.innerHTML = ''
            resultado.data.data.forEach(element => {
                const row = document.createElement('tr');
                const nombre_area = document.createElement('td');
                nombre_area.textContent = element.nombre_area; // Ajusta según las propiedades de tus datos

                row.appendChild(nombre_area);
                const acciones = document.createElement('td');
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Eliminar';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => //crear la funcion para eliminar
                    acciones.appendChild(deleteButton);
                row.appendChild(acciones);

                tbody_table.appendChild(row);

            });
        })
        .catch((err) => {
            console.log(err);
            alert("Error de seervdor")

        });

}