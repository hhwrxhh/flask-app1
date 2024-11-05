import React, { useState } from 'react';
import axios from 'axios';

const ImageEditor = () => {
    const [image, setImage] = useState(null);
    const [brightness, setBrightness] = useState(1.0);
    const [contrast, setContrast] = useState(1.0);
    const [blur, setBlur] = useState(0);
    const [toGrayscale, setToGrayscale] = useState(false);

    const loadImage = async (event) => {
        const file = event.target.files[0];
        if (!file) {
            alert("Please select an image file.");
            return;
        }
        
        const reader = new FileReader();
        reader.onloadend = async () => {
            const imageData = reader.result;
            const response = await axios.post('http://127.0.0.1:5000/load_image', { image: imageData });
            setImage(response.data.image);
        };
        reader.readAsDataURL(file);
    };

    const updateImage = async () => {
        const response = await axios.post('http://127.0.0.1:5000/update_image', {
            brightness,
            contrast,
            blur,
            to_grayscale: toGrayscale
        });
        setImage(response.data.image);
    };

    const downloadImage = async () => {
        const response = await axios.post('http://127.0.0.1:5000/download_image');
        const link = document.createElement('a');
        link.href = 'data:image/jpeg;base64,' + response.data.image;
        link.download = 'edited_image.jpg';
        link.click();
    };

    return (
        <div className="container">
            <h1>Photo Editor</h1>
            <input type="file" accept="image/*" onChange={loadImage} />
            <div className="controls">
                <label>Brightness</label>
                <input type="range" min="0" max="2" step="0.1" value={brightness} onChange={(e) => { setBrightness(e.target.value); updateImage(); }} />
                <label>Contrast</label>
                <input type="range" min="0" max="2" step="0.1" value={contrast} onChange={(e) => { setContrast(e.target.value); updateImage(); }} />
                <label>Blur</label>
                <input type="range" min="0" max="10" step="1" value={blur} onChange={(e) => { setBlur(e.target.value); updateImage(); }} />
                <label>Grayscale</label>
                <input type="checkbox" checked={toGrayscale} onChange={(e) => { setToGrayscale(e.target.checked); updateImage(); }} />
            </div>
            <div className="image-container">
                {image && <img src={`data:image/jpeg;base64,${image}`} alt="Your image here" id="image-display" />}
            </div>
            {image && <button onClick={downloadImage}>Download Edited Image</button>}
        </div>
    );
};

export default ImageEditor;
