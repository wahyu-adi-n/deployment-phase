from flask import request, jsonify, Flask
from libs.model import ClassifierModel
from libs.utils import predict, get_device, readb64
from PIL import Image
import torch
import config
import psycopg2
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
            save_result(pred_proba, pred_label)
            return jsonify({'conf_score': pred_proba,
                            'label': str(pred_label)})
                            
def save_result(pred_proba, pred_label):
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
    print(conn)
    cur = conn.cursor()
    
    # Create a table    
    cur.execute('''CREATE TABLE IF NOT EXISTS prediction_results (
                       id SERIAL PRIMARY KEY,
                       conf_score FLOAT,
                       label TEXT);''')
    conn.commit()
    cur.execute("INSERT INTO prediction_results (conf_score, label) VALUES (%s, %s)", (pred_proba, pred_label)) 
    conn.commit()        
    # cur.close()
    # conn.close()
    
if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
