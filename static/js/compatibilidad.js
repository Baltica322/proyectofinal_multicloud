document.addEventListener("DOMContentLoaded", function () {
    const cpuSelect = document.getElementById("cpu");
    const motherboardSelect = document.getElementById("motherboard");
    const ramSelect = document.getElementById("ram");

    // ✅ Evento: cuando se cambia el CPU, cargar placas compatibles
    cpuSelect.addEventListener("change", function () {
        const cpuId = this.value;

        // Limpiar selects dependientes
        motherboardSelect.innerHTML = '<option value="">-- Selecciona una placa madre --</option>';
        ramSelect.innerHTML = '<option value="">-- Selecciona una RAM compatible --</option>';
        ramSelect.disabled = true;

        if (!cpuId) return;

        fetch(`/api/placas-compatible-con/${cpuId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener placas madre");
                return response.json();
            })
            .then(data => {
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo}`;
                    motherboardSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error("Error al cargar placas madre compatibles:", error);
            });
    });

    // ✅ Evento: cuando se cambia la placa, cargar RAMs compatibles
    motherboardSelect.addEventListener("change", function () {
        const placaId = this.value;

        ramSelect.innerHTML = '<option value="">-- Cargando RAM compatibles... --</option>';
        ramSelect.disabled = true;

        if (!placaId) {
            ramSelect.innerHTML = '<option value="">-- Selecciona RAM --</option>';
            ramSelect.disabled = false;
            return;
        }

        fetch(`/api/rams-compatible-con/${placaId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener RAMs");
                return response.json();
            })
            .then(data => {
                ramSelect.innerHTML = '<option value="">-- Selecciona RAM --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.tipo_memoria})`;
                    ramSelect.appendChild(option);
                });
                ramSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar RAMs compatibles:", error);
                ramSelect.innerHTML = '<option value="">-- Error al cargar RAM --</option>';
            });
    });

    

    const gpuSelect = document.getElementById("gpu");

    // Cargar tarjetas gráficas compatibles cuando se selecciona una placa madre
    motherboardSelect.addEventListener("change", function () {
        const placaId = this.value;

        // Ya estás manejando RAM aquí, ahora también GPUs:
        gpuSelect.innerHTML = '<option value="">-- Cargando tarjetas gráficas... --</option>';
        gpuSelect.disabled = true;

        if (!placaId) {
            gpuSelect.innerHTML = '<option value="">-- Selecciona GPU --</option>';
            gpuSelect.disabled = false;
            return;
        }

        fetch(`/api/gpus-compatible-con/${placaId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener GPUs");
                return response.json();
            })
            .then(data => {
                gpuSelect.innerHTML = '<option value="">-- Selecciona GPU --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.vram}GB VRAM)`;
                    gpuSelect.appendChild(option);
                });
                gpuSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar GPUs compatibles:", error);
                gpuSelect.innerHTML = '<option value="">-- Error al cargar GPU --</option>';
            });
    });

    const almacenamientoSelect = document.getElementById("almacenamiento");

    motherboardSelect.addEventListener("change", function () {
        const placaId = this.value;

        almacenamientoSelect.innerHTML = '<option value="">-- Cargando opciones de almacenamiento... --</option>';
        almacenamientoSelect.disabled = true;

        if (!placaId) {
            almacenamientoSelect.innerHTML = '<option value="">-- Selecciona almacenamiento --</option>';
            almacenamientoSelect.disabled = false;
            return;
        }

        fetch(`/api/almacenamientos-compatible-con/${placaId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener almacenamientos");
                return response.json();
            })
            .then(data => {
                almacenamientoSelect.innerHTML = '<option value="">-- Selecciona almacenamiento --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.capacidad}, ${item.tipo_almacenamiento})`;
                    almacenamientoSelect.appendChild(option);
                });
               almacenamientoSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar almacenamientos compatibles:", error);
                almacenamientoSelect.innerHTML = '<option value="">-- Error al cargar almacenamiento --</option>';
            });
    });


    const gabineteSelect = document.getElementById("gabinete");

    motherboardSelect.addEventListener("change", function () {
        const placaId = this.value;

        gabineteSelect.innerHTML = '<option value="">-- Cargando gabinetes... --</option>';
        gabineteSelect.disabled = true;

        if (!placaId) {
            gabineteSelect.innerHTML = '<option value="">-- Selecciona gabinete --</option>';
            gabineteSelect.disabled = false;
            return;
        }

        fetch(`/api/gabinetes-compatible-con/${placaId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener gabinetes");
                return response.json();
            })
            .then(data => {
                gabineteSelect.innerHTML = '<option value="">-- Selecciona gabinete --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.vidrio})`;
                    gabineteSelect.appendChild(option);
                });
                gabineteSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar gabinetes compatibles:", error);
                gabineteSelect.innerHTML = '<option value="">-- Error al cargar gabinetes --</option>';
            });
    });


    const fuenteSelect = document.getElementById("fuente_poder");

    gpuSelect.addEventListener("change", function () {
        const gpuId = this.value;

        fuenteSelect.innerHTML = '<option value="">-- Cargando fuentes... --</option>';
        fuenteSelect.disabled = true;

        if (!gpuId) {
            fuenteSelect.innerHTML = '<option value="">-- Selecciona fuente de poder --</option>';
            fuenteSelect.disabled = false;
            return;
        }

        fetch(`/api/fuentes-compatible-con/${gpuId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener fuentes");
                return response.json();
            })
            .then(data => {
                fuenteSelect.innerHTML = '<option value="">-- Selecciona fuente de poder --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.potencia}, ${item.certificacion})`;
                    fuenteSelect.appendChild(option);
                });
                fuenteSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar fuentes compatibles:", error);
                fuenteSelect.innerHTML = '<option value="">-- Error al cargar fuentes --</option>';
            });
    });

    const coolerSelect = document.getElementById("cooler");

    cpuSelect.addEventListener("change", function () {
        const cpuId = this.value;

        coolerSelect.innerHTML = '<option value="">-- Cargando coolers compatibles... --</option>';
        coolerSelect.disabled = true;

        if (!cpuId) {
            coolerSelect.innerHTML = '<option value="">-- Selecciona un cooler --</option>';
            coolerSelect.disabled = false;
            return;
        }

        fetch(`/api/coolers-compatible-con/${cpuId}/`)
            .then(response => {
                if (!response.ok) throw new Error("Error al obtener coolers");
                return response.json();
            })
            .then(data => {
                coolerSelect.innerHTML = '<option value="">-- Selecciona un cooler --</option>';
                data.forEach(item => {
                    const option = document.createElement("option");
                    option.value = item.id;
                    option.textContent = `${item.fabricante} ${item.modelo} (${item.dimensiones})`;
                    coolerSelect.appendChild(option);
                });
                coolerSelect.disabled = false;
            })
            .catch(error => {
                console.error("Error al cargar coolers compatibles:", error);
                coolerSelect.innerHTML = '<option value="">-- Error al cargar coolers --</option>';
            });
    });

});
