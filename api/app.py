from flask import Blueprint, request, jsonify, Flask
import torch
from PIL import Image
import database as db
import config
from libs.model import ClassifierModel
from libs.utils import predict, get_device

app = Flask(__name__)
api = Blueprint('api', __name__)

model_name = 'deployed_model.pth'
model_path = f'./libs/models/{model_name}'
model = ClassifierModel()

trained_weights = torch.load(model_path, map_location=get_device)
model.load_state_dict(trained_weights)
model.eval()

print('PyTorch model loaded !')

@api.route('/predict', methods=['POST'])
def classify():
    if request.method == 'POST':
        if 'image' not in request.form:
            return jsonify({'error': 'no image in body'}), 400
        else:
            parameters = model.get_model_parameters()
            image_path = request.form['image']
            image = Image.open(image_path)
            pred_proba, pred_label = predict(model, image, **parameters)
            return jsonify({'conf_score':float(pred_proba),
                            'label': str(pred_label)})

@api.route('/save_results', methods=['POST'])
def post_classifier_results():
    if request.method == 'POST':
        expected_fields = [
            'image',
            'label',
            'conf_score',
            'user_agents',
            'ip_address',
        ]
        if any(field not in request.form for field in expected_fields):
            return jsonify({'error': 'Missing field in body'}), 400
        query = db.Classify.create(**request.form)
        return jsonify(query.serialize())


@api.route('/get_results', methods=['GET'])
def get_classifier_results():
    if request.method == 'GET':
        query = db.Clasify.select().order_by(db.Clasify.created_date.desc())
        return jsonify([r.serialize() for r in query])

app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST)