document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.getElementById('formset-container');
    const addFormBtn = document.getElementById('add-form');
    const totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    function reindexForms() {
        const productForms = formsetContainer.querySelectorAll('.formset-row');
        totalForms.value = productForms.length;

        productForms.forEach((formRow, index) => {
            formRow.querySelectorAll('input, textarea, select').forEach(input => {
                if (input.name) input.name = input.name.replace(/form-\d+-/, `form-${index}-`);
                if (input.id) input.id = input.id.replace(/form-\d+-/, `form-${index}-`);
            });

            const medidaForms = formRow.querySelectorAll('.medida-form');
            medidaForms.forEach((medidaForm, medidaIndex) => {
                medidaForm.querySelectorAll('input, select').forEach(input => {
                    if (input.name) input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${index}-medidas-${medidaIndex}-`);
                    if (input.id) input.id = input.id.replace(/form-\d+-medidas-\d+-/, `form-${index}-medidas-${medidaIndex}-`);
                });
            });

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

        // Limpiar campos del producto
        newForm.querySelectorAll('input, textarea').forEach(input => {
            input.value = '';
        });

        // Limpiar medidas excepto la primera
        const medidasContainer = newForm.querySelector('.medidas-container');
        const medidaForms = medidasContainer.querySelectorAll('.medida-form');
        medidaForms.forEach((form, index) => {
            if (index === 0) {
                form.querySelectorAll('input, select').forEach(input => input.value = '');
            } else {
                form.remove();
            }
        });

        formsetContainer.appendChild(newForm);
        reindexForms();
    });

    formsetContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-form')) {
            const formRows = formsetContainer.querySelectorAll('.formset-row');
            if (formRows.length <= 1) return alert("Debe haber al menos un producto.");
            e.target.closest('.formset-row').remove();
            reindexForms();
        }

        if (e.target.classList.contains('add-medida-btn')) {
            const productIndex = e.target.getAttribute('data-product-index');
            const medidasContainer = document.querySelector(`.medidas-container[data-product-index="${productIndex}"]`);
            const firstMedidaForm = medidasContainer?.querySelector('.medida-form');

            if (!firstMedidaForm) {
                alert("No hay formulario de medida para clonar.");
                return;
            }

            const medidaIndex = medidasContainer.querySelectorAll('.medida-form').length;
            const newMedidaForm = firstMedidaForm.cloneNode(true);

            newMedidaForm.querySelectorAll('input, select').forEach(input => {
                input.value = '';
                if (input.name) {
                    input.name = input.name.replace(/form-\d+-medidas-\d+-/, `form-${productIndex}-medidas-${medidaIndex}-`);
                }
                if (input.id) {
                    input.id = input.id.replace(/form-\d+-medidas-\d+-/, `form-${productIndex}-medidas-${medidaIndex}-`);
                }
            });

            medidasContainer.appendChild(newMedidaForm);
        }

        if (e.target.classList.contains('remove-medida-btn')) {
            const medidasContainer = e.target.closest('.medidas-container');
            const medidaForms = medidasContainer.querySelectorAll('.medida-form');
            if (medidaForms.length <= 1) {
                alert("Debe haber al menos una medida.");
                return;
            }
            e.target.closest('.medida-form').remove();
            reindexForms();
        }
    });
});