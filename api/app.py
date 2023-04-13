from flask import request, jsonify, Flask
from libs.model import ClassifierModel
from libs.utils import predict, get_device, readb64
from PIL import Image
import torch
import database as db
import config

app = Flask(__name__)

model_name = 'deployed_model.pth'
model_path = f'./libs/models/{model_name}'
model = ClassifierModel(input_shape=3, hidden_units=10,
                        output_shape=10).to(get_device())

trained_weights = torch.load(model_path, map_location=get_device())
model.load_state_dict(trained_weights)
model.eval()
print('PyTorch model loaded !')


@app.route("/")
def index():
    return "Image Classification Project"


@app.route('/predict', methods=['POST'])
def classify():
    if request.method == 'POST':
        if 'image' not in request.json:
            return jsonify({'error': 'no image in body'}), 400
        else:
            data = request.json
            image_read = readb64(data['image'])
            image = Image.fromarray(image_read)
            pred_proba, pred_label = predict(model, image)
            return jsonify({'conf_score': pred_proba,
                            'label': str(pred_label)})


@app.route('/save_results', methods=['POST'])
def post_classifier_results():
    if request.method == 'POST':
        expected_fields = [
            'image',
            'conf_score',
            'label',
            'user_agents',
            'ip_address',
        ]
        if any(field not in request.form for field in expected_fields):
            return jsonify({'error': 'Missing field in body'}), 400
        query = db.Classify.create(**request.form)
        return jsonify(query.serialize())


@app.route('/get_results', methods=['GET'])
def get_classifier_results():
    if request.method == 'GET':
        query = db.Classify.select().order_by(db.Classify.created_date.desc())
        return jsonify([r.serialize() for r in query])


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST)
