
document.getElementById('unidad').addEventListener('click', (e) => {
    e.preventDefault()
    const formulario = document.getElementById('unidadform')

    axios.post('unidad', formulario)
        .then((result) => {
            if (result.data.error) {
                document.getElementById('error_unidad').innerHTML = result.data.error
            } else if (result.data.data) {
                document.getElementById('error_unidad').innerHTML = ''
                listar_unidad()
            }
        }).catch((err) => {
            alert(err)
        });

})


function listar_unidad() {
    axios.get('unidad')
        .then((result) => {
            tbody_table_unidad = document.getElementById('tbody_table_unidad')
            tbody_table_unidad.innerHTML = ''
            result.data.data.forEach(element => {
                const row = document.createElement('tr');
                const nombre = document.createElement('td');
                nombre.textContent = element.nombre; // Ajusta según las propiedades de tus datos
                row.appendChild(nombre);
                const acciones = document.createElement('td');
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Eliminar';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => //crear la funcion para eliminar
                    acciones.appendChild(deleteButton);
                row.appendChild(acciones);

                tbody_table_unidad.appendChild(row);
            });
        })
        .catch((e) => {
            alert('error de servidor')
        }

        )

}

