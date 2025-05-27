const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const previewContainer = document.getElementById('preview-container');

    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.style.border = '2px solid blue';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.border = '2px dashed #ccc';
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.style.border = '2px dashed #ccc';
        const file = event.dataTransfer.files[0];
        handleFile(file);
    });

    uploadBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        handleFile(fileInput.files[0]);
    });

    function handleFile(file) {
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewContainer.innerHTML = `
                    <img src="${e.target.result}" class="img-thumbnail d-block mb-2" style="max-width: 200px;">
                    <p>Archivo seleccionado: ${file.name}</p>
                    <button type="button" id="remove-btn" class="btn btn-danger btn-sm">Eliminar</button>
                `;
                document.getElementById('remove-btn').addEventListener('click', () => {
                    fileInput.value = "";
                    previewContainer.innerHTML = "";
                });
            };
            reader.readAsDataURL(file);
        }
    }