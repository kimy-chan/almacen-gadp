
document.getElementById('id_oficinas').addEventListener('click', (e) => {
    e.preventDefault()
    const formulario = document.getElementById('id_form_oficinas')
    axios.post('oficinas', formulario)
        .then((result) => {
            if (result.data.error) {
                document.getElementById('error_oficinas').innerHTML = result.data.error
            } else if (result.data.data) {
                document.getElementById('error_oficinas').innerHTML = ''
                listar_oficinas()
            }
        }).catch((err) => {
            alert(err)
        });

})


function listar_oficinas() {
    axios.get('oficinas')
        .then((result) => {
            tbody_table_oficinas = document.getElementById('tbody_table_oficinas')
            tbody_table_oficinas.innerHTML = ''
            result.data.data.forEach(element => {
                const row = document.createElement('tr');
                const nombre = document.createElement('td');
                nombre.textContent = element.nombre; // Ajusta según las propiedades de tus datos
                row.appendChild(nombre);

                const acciones = document.createElement('td');
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Eliminar';
                deleteButton.className = 'btn btn-danger btn-sm';
                deleteButton.onclick = () => eliminar_oficina(element.id); // Ajusta según las propiedades de tus datos
                acciones.appendChild(deleteButton);
                row.appendChild(acciones);


                tbody_table_oficinas.appendChild(row);

            });
        })
        .catch((e) => {
            console.log(e);
            alert('error de servidor')
        }

        )

}

