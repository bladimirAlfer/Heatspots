document.addEventListener('DOMContentLoaded', () => {
    async function fetchData(endpoint) {
        const response = await fetch(endpoint);
        return response.json();
    }

    async function initDashboard() {
        // Calefactores
        const calefactoresData = await fetchData('/api/calefactores');
        const calefactoresChart = new Chart(document.getElementById('calefactoresChart'), {
            type: 'pie',
            data: {
                labels: ['Encendido', 'Apagado'],
                datasets: [{
                    data: calefactoresData,
                    backgroundColor: ['#4caf50', '#f44336'],
                }],
            },
        });

        // Opiniones
        const opinionesData = await fetchData('/api/opiniones/ratings');
        const opinionesChart = new Chart(document.getElementById('opinionesChart'), {
            type: 'bar',
            data: {
                labels: ['1★', '2★', '3★', '4★', '5★'],
                datasets: [{
                    data: opinionesData,
                    backgroundColor: '#3f51b5',
                }],
            },
        });

        // Sensores
        const sensoresData = await fetchData('/api/sensores');
        const sensoresChart = new Chart(document.getElementById('sensoresChart'), {
            type: 'line',
            data: {
                labels: sensoresData.dates,
                datasets: [
                    { label: 'Temperatura', data: sensoresData.temperatures, borderColor: '#ff5722' },
                    { label: 'Personas', data: sensoresData.personas, borderColor: '#009688' },
                ],
            },
        });

        // Reportes
        const reportesData = await fetchData('/api/reportes');
        const reportesChart = new Chart(document.getElementById('reportesChart'), {
            type: 'bar',
            data: {
                labels: ['Por Revisar', 'En Revisión', 'Solucionado'],
                datasets: [{
                    data: reportesData,
                    backgroundColor: ['#ffc107', '#03a9f4', '#4caf50'],
                }],
            },
        });

        // Instituciones
        const institucionesData = await fetchData('/api/instituciones');
        const institucionesChart = new Chart(document.getElementById('institucionesChart'), {
            type: 'horizontalBar',
            data: {
                labels: institucionesData.names,
                datasets: [{
                    data: institucionesData.pisos,
                    backgroundColor: '#673ab7',
                }],
            },
        });

        // Últimos reportes
        const reportesTableBody = document.getElementById('reportesTableBody');
        const lastReports = await fetchData('/api/reportes/last');
        lastReports.forEach(report => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${report.tipo_reporte}</td><td>${report.estado}</td><td>${new Date(report.fecha_reporte).toLocaleString()}</td>`;
            reportesTableBody.appendChild(row);
        });
    }

    initDashboard();
});
