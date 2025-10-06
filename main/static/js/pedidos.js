
document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.getElementById('formset-container');
    const addFormBtn = document.getElementById('add-form');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    function updateMedidasTotalForms(medidasContainer) {
        const totalFormsInput = medidasContainer.querySelector('input[name$="-TOTAL_FORMS"]');
        if (totalFormsInput) {
            const medidaForms = medidasContainer.querySelectorAll('.medida-form');
            totalFormsInput.value = medidaForms.length;
        }
    }

    function reindexForms() {
        const productForms = formsetContainer.querySelectorAll('.formset-row');
        totalForms.value = productForms.length;

        productForms.forEach((formRow, index) => {
            formRow.querySelectorAll('input, textarea, select').forEach(input => {
                if (input.name && !input.name.includes('medidas')) {
                    input.name = input.name.replace(/form-\d+-/, `form-${index}-`);
                }
                if (input.id && !input.id.includes('medidas')) {
                    input.id = input.id.replace(/id_form-\d+-/, `id_form-${index}-`);
                }
            });

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

            const medidasContainer = formRow.querySelector('.medidas-container');
            const addMedidaBtn = formRow.querySelector('.add-medida-btn');
            if (medidasContainer) medidasContainer.setAttribute('data-product-index', index);
            if (addMedidaBtn) addMedidaBtn.setAttribute('data-product-index', index);
        });
    }

    if (addFormBtn) {
        addFormBtn.addEventListener('click', function () {
            const currentFormCount = parseInt(totalForms.value);
            const firstForm = formsetContainer.querySelector('.formset-row');
            if (!firstForm) return alert("No hay formularios para clonar.");

            const newForm = firstForm.cloneNode(true);
            const newIndex = currentFormCount;

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

            const medidasContainer = newForm.querySelector('.medidas-container');
            medidasContainer.setAttribute('data-product-index', newIndex);

            const medidaForms = medidasContainer.querySelectorAll('.medida-form');
            medidaForms.forEach((form, index) => {
                if (index === 0) {
                    form.querySelectorAll('input, select').forEach(input => {
                        input.value = '';
                        if (input.name) {
                            input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${newIndex}-medidas-0-`);
                        }
                        if (input.id) {
                            input.id = input.id.replace(/form-\d+-medidas-\d+-/, `form-${newIndex}-medidas-0-`);
                        }
                    });
                    const removeBtn = form.querySelector('.remove-medida-btn');
                    if (removeBtn) {
                        removeBtn.setAttribute('data-product-index', newIndex);
                    }
                } else {
                    form.remove();
                }
            });

            const addMedidaBtn = newForm.querySelector('.add-medida-btn');
            if (addMedidaBtn) {
                addMedidaBtn.setAttribute('data-product-index', newIndex);
            }

            formsetContainer.appendChild(newForm);
            totalForms.value = parseInt(totalForms.value) + 1;
        });
    }

    formsetContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-form')) {
            const formRows = formsetContainer.querySelectorAll('.formset-row');
            if (formRows.length <= 1) {
                alert("Debe haber al menos un producto.");
                return;
            }
            e.target.closest('.formset-row').remove();
            reindexForms();
        }

        if (e.target.classList.contains('add-medida-btn')) {
            e.preventDefault();
            const productIndex = e.target.getAttribute('data-product-index');
            const medidasContainer = document.querySelector(`.medidas-container[data-product-index="${productIndex}"]`);
            if (!medidasContainer) {
                console.error('No se encontró el contenedor de medidas');
                return;
            }

            const medidaIndex = medidasContainer.querySelectorAll('.medida-form').length;

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
            updateMedidasTotalForms(medidasContainer);
        }

        if (e.target.classList.contains('remove-medida-btn')) {
            e.preventDefault();
            const medidasContainer = e.target.closest('.medidas-container');
            const medidaForms = medidasContainer.querySelectorAll('.medida-form');
            if (medidaForms.length <= 1) {
                alert("Debe haber al menos una medida.");
                return;
            }
            e.target.closest('.medida-form').remove();

            const productIndex = medidasContainer.getAttribute('data-product-index');
            medidasContainer.querySelectorAll('.medida-form').forEach((form, index) => {
                form.querySelectorAll('input, select').forEach(input => {
                    if (input.name) {
                        input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${productIndex}-medidas-${index}-`);
                    }
                    if (input.id) {
                        input.id = input.id.replace(/form-\d+-medidas-\d+-/, `form-${productIndex}-medidas-${index}-`);
                    }
                });
            });

            updateMedidasTotalForms(medidasContainer);
        }
    });

    function getMedidaOptions() {
        const firstSelect = document.querySelector('select[name*="medidas"]');
        if (firstSelect) {
            return firstSelect.innerHTML;
        }
        return '';
    }
});
