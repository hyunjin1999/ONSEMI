document.addEventListener('DOMContentLoaded', function() {
    let imageUploadContainer = document.getElementById('image-upload-container');
    let addImageButton = document.getElementById('add-image');
    let totalForms = document.querySelector('#id_form-TOTAL_FORMS');

    function createImageUploadField() {
        let newFormIndex = totalForms.value;
        let newForm = document.createElement('div');
        newForm.classList.add('image-upload');
        newForm.innerHTML = `
            <input type="file" name="form-${newFormIndex}-image" id="id_form-${newFormIndex}-image" style="display: none;">
            <img src="" alt="이미지 미리보기" class="image-preview" id="preview-${newFormIndex}" style="display: none;">
            <button type="button" class="remove-image">&times;</button>
        `;
        imageUploadContainer.insertBefore(newForm, addImageButton);

        let fileInput = newForm.querySelector(`input[type="file"]`);
        let previewImage = newForm.querySelector('.image-preview');
        fileInput.click();

        fileInput.addEventListener('change', function() {
            if (fileInput.files && fileInput.files[0]) {
                let reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.style.display = 'block';
                }
                reader.readAsDataURL(fileInput.files[0]);
            }
        });

        newForm.querySelector('.remove-image').addEventListener('click', function() {
            newForm.remove();
            updateFormIndices();
        });

        totalForms.value = parseInt(totalForms.value) + 1;
    }

    function updateFormIndices() {
        let forms = imageUploadContainer.querySelectorAll('.image-upload');
        let index = 0;
        forms.forEach((form) => {
            if (form.querySelector('input[type="file"]')) {
                let fileInput = form.querySelector(`input[type="file"]`);
                fileInput.name = `form-${index}-image`;
                fileInput.id = `id_form-${index}-image`;
                let previewImage = form.querySelector('.image-preview');
                previewImage.id = `preview-${index}`;
                index += 1;
            }
        });
        totalForms.value = index; // Update total forms count
    }

    addImageButton.addEventListener('click', function() {
        createImageUploadField();
    });
});