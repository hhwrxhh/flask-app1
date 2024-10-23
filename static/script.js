$(document).ready(function () {
    let brightness = 1.0;
    let contrast = 1.0;
    let blur = 0;
    let toGrayscale = false;

    // Завантаження зображення з локального комп'ютера
    $('#load-image-btn').click(function () {
        const fileInput = $('#image-file')[0];
        if (fileInput.files.length === 0) {
            alert("Please select an image file.");
            return;
        }
        
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(event) {
            const imageData = event.target.result; // Base64 image data
            $.ajax({
                type: 'POST',
                url: '/load_image',
                contentType: 'application/json',
                data: JSON.stringify({ image: imageData }),
                success: function (response) {
                    if (response.error) {
                        alert("Error loading image: " + response.error);
                    } else {
                        $('#image-display').attr('src', 'data:image/jpeg;base64,' + response.image);
                        $('#download-image-btn').hide(); // Сховати кнопку завантаження до обробки зображення
                        
                        // Скинути значення слайдерів і чекбоксу
                        brightness = 1.0;
                        contrast = 1.0;
                        blur = 0;
                        toGrayscale = false;

                        $('#brightness-slider').val(brightness);
                        $('#contrast-slider').val(contrast);
                        $('#blur-slider').val(blur);
                        $('#grayscale-checkbox').prop('checked', toGrayscale);
                    }
                }
            });
        };

        reader.readAsDataURL(file); // Convert the file to base64
    });

    // Функція для оновлення зображення
    function updateImage() {
        $.ajax({
            type: 'POST',
            url: '/update_image',
            contentType: 'application/json',
            data: JSON.stringify({ 
                brightness: brightness, 
                contrast: contrast, 
                blur: blur, 
                to_grayscale: toGrayscale 
            }),
            success: function (response) {
                if (response.error) {
                    alert("Error updating image: " + response.error);
                } else {
                    $('#image-display').attr('src', 'data:image/jpeg;base64,' + response.image);
                    $('#download-image-btn').show(); // Показати кнопку завантаження після обробки зображення
                }
            }
        });
    }

    // Обробка зміни значень слайдерів
    $('#brightness-slider').on('input', function () {
        brightness = $(this).val();
        updateImage();  // Оновити зображення при зміні
    });

    $('#contrast-slider').on('input', function () {
        contrast = $(this).val();
        updateImage();  // Оновити зображення при зміні
    });

    $('#blur-slider').on('input', function () {
        blur = $(this).val();
        updateImage();  // Оновити зображення при зміні
    });

    $('#grayscale-checkbox').on('change', function () {
        toGrayscale = $(this).is(':checked');
        updateImage();  // Оновити зображення при зміні
    });

    // Завантаження обробленого зображення
    $('#download-image-btn').click(function () {
        $.ajax({
            type: 'POST',
            url: '/download_image',
            contentType: 'application/json',
            success: function (response) {
                if (response.error) {
                    alert("Error downloading image: " + response.error);
                } else {
                    const link = document.createElement('a');
                    link.href = 'data:image/jpeg;base64,' + response.image;
                    link.download = 'edited_image.jpg';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                }
            }
        });
    });
});
