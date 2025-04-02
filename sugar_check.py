from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
from PIL import Image
import pytesseract
from pillow_heif import register_heif_opener

register_heif_opener()
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

sugar_list = [
    'agave nectar','barbados sugar','barley malt','barley malt syrup','beet sugar', 
    'brown sugar', 'buttered syrup' ,'cane juice','cane juice crystals','cane sugar',
    'caramel','carob syrup','castor sugar','coconut palm sugar','coconut sugar',
    'confectioner\'s sugar','corn sweetener','corn syrup','corn syrup solids','date sugar',
    'dehydrated cane juice', 'demerara sugar','dextrin','dextrose','evaporated cane juice',
    'free flowing brown sugars','fructose','fruit juice','fruit juice concentrate',
    'glucose','glucose solids','golden sugar','golden syrup','grape sugar','hfcs',
    'high fructose corn syrup','honey','icing sugar','invert sugar','malt syrup',
    'maltodextrin','maltol','maltose','mannose','maple syrup','molasses','muscovado',
    'palmsugar','panocha','powdered sugar','raw sugar','refiner\'s syrup','rice syrup',
    'raccharose','sorghum syrup','sucrose','sugar (granulated)','sweet sorghum','syrup',
    'treacle','turbinado sugar', 'yellow sugar','sugars','added sugars'
]
@app.route('/')
def home():
    return "welcome to the app"
@app.route('/sugar-check', methods=['POST'])
def sugar_check():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save the file temporarily
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Process the image (convert if needed)
        if file.filename.lower().endswith('.heic'):
            image = Image.open(file_path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + file.filename + '.jpg')
            image.save(file_path, format="JPEG")
        
        # Open and process the image
        image = Image.open(file_path)
        image = image.convert('L')  # Optional: convert to grayscale
        text = pytesseract.image_to_string(image)
        text_lower = text.lower()
        found_sugars = [
            sugar for sugar in sugar_list
            if re.search(r'\b' + re.escape(sugar) + r'\b', text_lower)
        ]
        
        result = "there are sugars in your food" if found_sugars else "there are no sugars in your food"
        
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the file(s)
        if os.path.exists(file_path):
            os.remove(file_path)



if __name__ == '__main__':
    # Retrieve the port from the environment variable (Heroku sets this) or default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    # Enable debug mode if the DEBUG environment variable is set to a truthy value
    debug_mode = os.environ.get("DEBUG", "False").lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

