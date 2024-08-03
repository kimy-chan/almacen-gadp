document.getElementById('guardar_secretaria').addEventListener('click', (e) => {
    e.preventDefault()
    const form = document.getElementById('form_secretaria')

    axios.post('crear_secretaria_listar', form)
        .then((resultado) => {
            if (resultado.data.error) {
                document.getElementById('error').innerHTML = resultado.data.error
            } else if (resultado.data.data) {
                document.getElementById('error').innerHTML = ''
                Listar_secretaria()
            }
        })
        .catch((e) => {
            alert('error de servidor')
        })
})

function Listar_secretaria() {
    axios.get('crear_secretaria_listar',)
        .then((respuesta) => {
            if (respuesta.data.data) {
                const tbody = document.getElementById('tbody_table');
                tbody.innerHTML = '';
                respuesta.data.data.forEach(element => {
                    const row = document.createElement('tr');
                    const name_secretaria = document.createElement('td');
                    name_secretaria.textContent = element.secretaria; // Ajusta según las propiedades de tus datos
                    row.appendChild(name_secretaria);

                    const acciones = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Eliminar';
                    deleteButton.className = 'btn btn-danger btn-sm';
                    deleteButton.onclick = () => eliminar_sercretaria(element.id)
                    acciones.appendChild(deleteButton);
                    row.appendChild(acciones);

                    tbody.appendChild(row);
                });
            }
        })

        .catch((e) => {
            console.log(e);
        })

}

function eliminar_sercretaria(id) {

}
