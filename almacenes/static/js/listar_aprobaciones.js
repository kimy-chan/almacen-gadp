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
                    const row = document.createElement('tr');
                    const name_nombre = document.createElement('td');
                    name_nombre.textContent = element.nombre;
                    row.appendChild(name_nombre);
                    const name_secretaria = document.createElement('td');
                    name_secretaria.textContent = element.secretaria;
                    row.appendChild(name_secretaria);
                    const area = document.createElement('td');
                    area.textContent = element.area;
                    row.appendChild(area);
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

