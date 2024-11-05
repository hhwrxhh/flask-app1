# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from PIL import Image, ImageEnhance, ImageFilter
# import io
# import base64

# app = Flask(__name__)
# CORS(app)  # Дозволити кросс-домашні запити

# @app.route('/load_image', methods=['POST'])
# def load_image():
#     data = request.get_json()
#     image_data = data['image']
#     image = Image.open(io.BytesIO(base64.b64decode(image_data.split(',')[1])))
#     image.save('uploaded_image.jpg')
#     return jsonify({'image': image_to_base64(image)})

# @app.route('/update_image', methods=['POST'])
# def update_image():
#     data = request.get_json()
#     brightness = float(data['brightness'])
#     contrast = float(data['contrast'])
#     blur = int(data['blur'])
#     to_grayscale = data['to_grayscale']

#     # Завантажити зображення
#     image = Image.open('uploaded_image.jpg')

#     # Застосувати зміни
#     if to_grayscale:
#         image = image.convert('L').convert('RGB')  # Перетворити в градації сірого
#     image = ImageEnhance.Brightness(image).enhance(brightness)
#     image = ImageEnhance.Contrast(image).enhance(contrast)
#     if blur > 0:
#         image = image.filter(ImageFilter.GaussianBlur(blur))

#     # Зберегти та повернути оброблене зображення
#     image.save('edited_image.jpg')
#     return jsonify({'image': image_to_base64(image)})

# @app.route('/download_image', methods=['POST'])
# def download_image():
#     image = Image.open('edited_image.jpg')
#     return jsonify({'image': image_to_base64(image)})

# def image_to_base64(image):
#     buffered = io.BytesIO()
#     image.save(buffered, format="JPEG")
#     return base64.b64encode(buffered.getvalue()).decode()

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
import base64

app = Flask(__name__)
CORS(app)  # Дозволити кросс-домашні запити

# Глобальні змінні для збереження оригінального та відредагованого зображення
original_image = None
adjusted_image = None

def adjust_image(image, brightness=1.0, contrast=1.0, blur=0, to_grayscale=False):
    # Налаштування яскравості зображення
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)
    
    # Налаштування контрасту зображення
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)
    
    # Застосування розмиття
    if blur > 0:
        image = image.filter(ImageFilter.GaussianBlur(blur))
    
    # Конвертація в градації сірого
    if to_grayscale:
        image = image.convert('L').convert('RGB')
    
    return image

# @app.route('/')
# def index():
#     return render_template('./index.html')

@app.route('/load_image', methods=['POST'])
def load_image():
    global original_image
    data = request.json
    image_data = data['image']
    
    try:
        # Decode the base64 string to bytes
        image_data = image_data.split(',')[1]  # Remove the prefix (data:image/jpeg;base64,)
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        original_image = image.convert('RGB')  # Ensure the image is in RGB format
        
        # Convert the image to base64 for the frontend
        buffered = BytesIO()
        original_image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/update_image', methods=['POST'])
def update_image():
    global original_image, adjusted_image
    if original_image is None:
        return jsonify({'error': 'Image not loaded'})
    
    data = request.json
    brightness = float(data.get('brightness', 1.0))
    contrast = float(data.get('contrast', 1.0))
    blur = float(data.get('blur', 0))
    to_grayscale = data.get('to_grayscale', False)
    
    # Обробка зображення з новими параметрами
    adjusted_image = adjust_image(original_image, brightness, contrast, blur, to_grayscale)
    
    # Конвертуємо оброблене зображення в base64 для фронтенду
    buffered = BytesIO()
    adjusted_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    return jsonify({'image': img_str})

@app.route('/download_image', methods=['POST'])
def download_image():
    global adjusted_image
    if adjusted_image is None:
        return jsonify({'error': 'Image not loaded'})

    # Конвертуємо відредаговане зображення в base64
    buffered = BytesIO()
    adjusted_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run(debug=True)


