
document.getElementById('id_servicios').addEventListener('click', (e) => {
    e.preventDefault()
    const formulario = document.getElementById('id_form_servicios')

    axios.post('servicios', formulario)
        .then((result) => {
            if (result.data.error) {
                document.getElementById('error_servicios').innerHTML = result.data.error
            } else if (result.data.data) {
                document.getElementById('error_servicios').innerHTML = ''
                listar_servicios()
            }
        }).catch((err) => {
            alert(err)
        });

})


function listar_servicios() {
    axios.get('servicios')
        .then((result) => {
            tbody_table_servicios = document.getElementById('tbody_table_servicios')
            tbody_table_servicios.innerHTML = ''
            result.data.data.forEach(element => {
                const row = document.createElement('tr');
                const nombre = document.createElement('td');
                nombre.textContent = element.nombre;
                row.appendChild(nombre);
                const acciones = document.createElement('td');
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Eliminar';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => //crear la funcion para eliminar
                    acciones.appendChild(deleteButton);
                row.appendChild(acciones);

                tbody_table_servicios.appendChild(row);
            });
        })
        .catch((e) => {
            console.log(e);
            alert('error de servidor')
        }

        )

}

