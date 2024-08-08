function mostrar_aprobaciones_pedido(id_pedido) {
    var infoModal = new bootstrap.Modal(document.getElementById('infoModal'));
    infoModal.show();
    axios.get(`informacion/pedido/${id_pedido}`)
        .then((result) => {
            console.log(result);
            if (result.statusText == 'OK') {
                const tbody = document.getElementById('tbody_table');
                tbody.innerHTML = '';
                result.data.data.forEach(element => {
                    console.log(element.unidad);

                    const row = document.createElement('tr');
                    const name_nombre = document.createElement('td');
                    name_nombre.textContent = element.nombre;
                    row.appendChild(name_nombre);
                    const unidad = document.createElement('td');
                    unidad.textContent = element.unidad;
                    row.appendChild(unidad);
                    const oficina = document.createElement('td');
                    oficina.textContent = element.oficina == 'Ninguna' ? 'Encargado de unidad' : element.oficina;
                    row.appendChild(oficina);
                    const aprobacion = document.createElement('td');
                    aprobacion.textContent = element.aprobacion ? 'Aprobado' : 'No Aprobado';
                    row.appendChild(aprobacion);
                    tbody.appendChild(row);
                    const fecha = document.createElement('td');
                    fecha.textContent = element.fecha
                    row.appendChild(fecha);
                    tbody.appendChild(row);
                });
            }
        }).catch((err) => {
            console.log(err);
            alert('Error de servidor')
        });
}

