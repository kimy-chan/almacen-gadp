
document.getElementById('id_departamental').addEventListener('click', (e) => {
    e.preventDefault()
    const formulario = document.getElementById('id_form_departamental')
    axios.post('departamental', formulario)
        .then((result) => {
            if (result.data.error) {
                document.getElementById('error_departamental').innerHTML = result.data.error
            } else if (result.data.data) {
                document.getElementById('error_departamental').innerHTML = ''
                listar_departamental()
            }
        }).catch((err) => {
            alert(err)
        });

})


function listar_departamental() {
    axios.get('departamental')
        .then((result) => {
            tbody_table_departamental = document.getElementById('tbody_table_departamental')
            tbody_table_departamental.innerHTML = ''
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

                tbody_table_departamental.appendChild(row);

            });
        })
        .catch((e) => {
            console.log(e);
            alert('error de servidor')
        }

        )

}

