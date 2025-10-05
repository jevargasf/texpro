document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.getElementById('formset-container');
    const addFormBtn = document.getElementById('add-form');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    function reindexForms() {
        const productForms = formsetContainer.querySelectorAll('.formset-row');
        totalForms.value = productForms.length;

        productForms.forEach((formRow, index) => {
            // Reindexar campos del producto
            formRow.querySelectorAll('input, textarea, select').forEach(input => {
                if (input.name && !input.name.includes('medidas')) {
                    input.name = input.name.replace(/form-\d+-/, `form-${index}-`);
                }
                if (input.id && !input.id.includes('medidas')) {
                    input.id = input.id.replace(/id_form-\d+-/, `id_form-${index}-`);
                }
            });

            // Reindexar medidas
            const medidaForms = formRow.querySelectorAll('.medida-form');
            medidaForms.forEach((medidaForm, medidaIndex) => {
                medidaForm.querySelectorAll('input, select').forEach(input => {
                    if (input.name) {
                        input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${index}-medidas-${medidaIndex}-`);
                    }
                    if (input.id) {
                        input.id = input.id.replace(/form-\d+-medidas-\d+-/, `form-${index}-medidas-${medidaIndex}-`);
                    }
                });
            });

            // Actualizar data attributes
            const medidasContainer = formRow.querySelector('.medidas-container');
            const addMedidaBtn = formRow.querySelector('.add-medida-btn');
            if (medidasContainer) medidasContainer.setAttribute('data-product-index', index);
            if (addMedidaBtn) addMedidaBtn.setAttribute('data-product-index', index);
        });
    }

    addFormBtn.addEventListener('click', function () {
        const currentFormCount = parseInt(totalForms.value);
        const firstForm = formsetContainer.querySelector('.formset-row');
        if (!firstForm) return alert("No hay formularios para clonar.");

        const newForm = firstForm.cloneNode(true);
        const newIndex = currentFormCount;

        // Limpiar campos del producto
        newForm.querySelectorAll('input, textarea').forEach(input => {
            if (!input.name.includes('medidas')) {
                input.value = '';
                if (input.name) {
                    input.name = input.name.replace(/form-\d+-/, `form-${newIndex}-`);
                }
                if (input.id) {
                    input.id = input.id.replace(/id_form-\d+-/, `id_form-${newIndex}-`);
                }
            }
        });

        // Configurar medidas: mantener solo una medida vacía
        const medidasContainer = newForm.querySelector('.medidas-container');
        medidasContainer.setAttribute('data-product-index', newIndex);
        
        const medidaForms = medidasContainer.querySelectorAll('.medida-form');
        medidaForms.forEach((form, index) => {
            if (index === 0) {
                // Mantener la primera medida pero limpiar y reindexar
                form.querySelectorAll('input, select').forEach(input => {
                    input.value = '';
                    if (input.name) {
                        input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${newIndex}-medidas-0-`);
                    }
                });
            } else {
                // Eliminar medidas adicionales
                form.remove();
            }
        });

        // Actualizar botón de agregar medida
        const addMedidaBtn = newForm.querySelector('.add-medida-btn');
        if (addMedidaBtn) {
            addMedidaBtn.setAttribute('data-product-index', newIndex);
        }

        formsetContainer.appendChild(newForm);
        totalForms.value = parseInt(totalForms.value) + 1;
    });

    formsetContainer.addEventListener('click', function (e) {
        // Eliminar producto
        if (e.target.classList.contains('remove-form')) {
            const formRows = formsetContainer.querySelectorAll('.formset-row');
            if (formRows.length <= 1) {
                alert("Debe haber al menos un producto.");
                return;
            }
            e.target.closest('.formset-row').remove();
            reindexForms();
        }

        // Agregar medida
        if (e.target.classList.contains('add-medida-btn')) {
            e.preventDefault();
            const productIndex = e.target.getAttribute('data-product-index');
            const medidasContainer = document.querySelector(`.medidas-container[data-product-index="${productIndex}"]`);
            
            if (!medidasContainer) {
                console.error('No se encontró el contenedor de medidas');
                return;
            }

            const medidaIndex = medidasContainer.querySelectorAll('.medida-form').length;
            
            // Crear nueva medida
            const newMedidaForm = document.createElement('div');
            newMedidaForm.className = 'medida-form mb-2';
            newMedidaForm.innerHTML = `
                <div class="row align-items-end">
                    <div class="col-md-5">
                        <label class="form-label">Medida</label>
                        <select name="form-${productIndex}-medidas-${medidaIndex}-medidas" class="form-select">
                            ${getMedidaOptions()}
                        </select>
                    </div>
                    <div class="col-md-5">
                        <label class="form-label">Longitud</label>
                        <input type="number" name="form-${productIndex}-medidas-${medidaIndex}-longitud" class="form-control" required>
                    </div>
                    <div class="col-md-2">
                        <button type="button" class="btn btn-sm btn-danger remove-medida-btn">Eliminar</button>
                    </div>
                </div>
            `;

            medidasContainer.appendChild(newMedidaForm);
        }

        // Eliminar medida
        if (e.target.classList.contains('remove-medida-btn')) {
            e.preventDefault();
            const medidasContainer = e.target.closest('.medidas-container');
            const medidaForms = medidasContainer.querySelectorAll('.medida-form');
            if (medidaForms.length <= 1) {
                alert("Debe haber al menos una medida.");
                return;
            }
            e.target.closest('.medida-form').remove();
            
            // Reindexar medidas del producto actual
            const productIndex = medidasContainer.getAttribute('data-product-index');
            medidasContainer.querySelectorAll('.medida-form').forEach((form, index) => {
                form.querySelectorAll('input, select').forEach(input => {
                    if (input.name) {
                        input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${productIndex}-medidas-${index}-`);
                    }
                });
            });
        }
    });

    // Función auxiliar para obtener las opciones de medida
    function getMedidaOptions() {
        const firstSelect = document.querySelector('select[name*="medidas"]');
        if (firstSelect) {
            return firstSelect.innerHTML;
        }
        return '';
    }
});