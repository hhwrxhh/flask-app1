from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from os import path
import base64

app = Flask(__name__,static_folder='../static')
app.template_folder = path.join('..', 'templates')
# app.config['STATIC_FOLDER'] = "../static"

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

@app.route('/')
def index():
    return render_template('./index.html')

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

