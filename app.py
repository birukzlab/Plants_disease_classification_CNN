from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
# Ensure the PredictionPipeline import path is correct
from cnnClassifier.pipeline.predict import PredictionPipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        # Initialize the PredictionPipeline without a filename,
        # since the model will now be loaded once in the PredictionPipeline's constructor.
        self.classifier = PredictionPipeline()

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/train", methods=['GET', 'POST'])
@cross_origin()
def trainRoute():
    # Assuming "dvc repro" is correct for your training pipeline.
    # Ensure this command runs as expected in your environment.
    os.system("dvc repro")
    return "Training done successfully!"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # Define your save directory for uploaded images
        save_directory = 'uploads'
        os.makedirs(save_directory, exist_ok=True)  # Create the directory if it does not exist
        filepath = os.path.join(save_directory, secure_filename(file.filename))
        file.save(filepath)  # Save the uploaded image to the filesystem
        
        # Use the classifier to predict the class of the uploaded image
        result = clApp.classifier.predict(filepath)
        return jsonify(result)

if __name__ == "__main__":
    # Initialize the client app here to ensure it's done once
    clApp = ClientApp()
    app.run(host='0.0.0.0', port=8080, debug=False)  # Set debug=False for production use


