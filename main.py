import os
import tensorflow as tf
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from google.cloud import storage
from io import BytesIO
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

model = tf.keras.models.load_model("model.h5")
class_names = ['HDPE', 'LDPE', 'PET', 'PP', 'PS', 'PVC']

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        
    def __enter__(self):
        self.connection = mysql.connector.connect(**db_config)
        return self.connection
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()

def save_prediction(user_id, image_url, file_name, jenis_plastik, confidence_score):
    try:
        with DatabaseConnection() as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO hasil_prediksi 
                (user_id, image_url, file_name, jenis_plastik, confidence_score) 
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, image_url, file_name, jenis_plastik, confidence_score))
            connection.commit()
            prediction_id = cursor.lastrowid
            cursor.close()
            return prediction_id
    except Error as e:
        print(f"Error saving prediction to database: {e}")
        raise

class PlasticInfo:
    def __init__(self, nama, simbol_kode, description, recycling_time, produk_penggunaan, environmental_impact):
        self.nama = nama
        self.simbol_kode = simbol_kode
        self.description = description
        self.recycling_time = recycling_time
        self.produk_penggunaan = produk_penggunaan
        self.environmental_impact = environmental_impact

    def to_dict(self):
        return {
            "Nama plastik": self.nama,
            "Simbol Kode": self.simbol_kode,
            "Deskripsi": self.description,
            "Recycling time": self.recycling_time,
            "Produk penggunaan": self.produk_penggunaan,
            "Environmental impact": self.environmental_impact
        }

plastic_info = {
    "PET": PlasticInfo(
        nama="Polyethylene Terephthalate (PET)",
        simbol_kode="1",
        description="PET adalah plastik yang sering digunakan untuk botol minuman dan wadah makanan karena sifatnya yang kuat dan ringan.",
        recycling_time="20-500 tahun",
        produk_penggunaan=["Botol minuman", "Wadah makanan", "Serat tekstil"],
        environmental_impact="Dapat mencemari tanah dan air, berpotensi menghasilkan mikroplastik yang berbahaya bagi ekosistem laut. Jika terbakar dapat menghasilkan gas beracun."
    ),
    "HDPE": PlasticInfo(
        nama="High-Density Polyethylene (HDPE)",
        simbol_kode="2",
        description="HDPE adalah plastik yang keras dan tahan terhadap berbagai zat kimia, sering digunakan untuk botol susu dan wadah produk pembersih.",
        recycling_time="30-500 tahun",
        produk_penggunaan=["Botol susu", "Wadah produk pembersih", "Kantong belanja"],
        environmental_impact="Lebih aman dari PET namun tetap sulit terurai. Memiliki tingkat toksisitas yang rendah tetapi tetap berkontribusi pada pencemaran lingkungan jika tidak didaur ulang."
    ),
    "PVC": PlasticInfo(
        nama="Polyvinyl Chloride (PVC)",
        simbol_kode="3",
        description="PVC memiliki ketahanan tinggi terhadap kelembaban dan bahan kimia, sering digunakan dalam pipa dan kemasan medis.",
        recycling_time="50-500 tahun",
        produk_penggunaan=["Pipa air", "Kemasan medis", "Vinil lantai"],
        environmental_impact="Sangat berbahaya jika dibakar karena menghasilkan dioksin. Mengandung berbagai bahan kimia berbahaya yang dapat mencemari tanah dan air tanah."
    ),
    "LDPE": PlasticInfo(
        nama="Low-Density Polyethylene (LDPE)",
        simbol_kode="4",
        description="LDPE adalah plastik fleksibel yang sering digunakan untuk kantong plastik dan film pembungkus.",
        recycling_time="10-100 tahun",
        produk_penggunaan=["Kantong plastik", "Film pembungkus", "Lapisan karton minuman"],
        environmental_impact="Sulit terurai secara alami, sering ditemukan mencemari lautan dan merusak kehidupan laut. Penggunaan berlebihan berkontribusi pada masalah sampah plastik global."
    ),
    "PP": PlasticInfo(
        nama="Polypropylene (PP)",
        simbol_kode="5",
        description="PP adalah plastik yang tahan panas dan banyak digunakan dalam wadah makanan, sedotan, dan produk medis.",
        recycling_time="20-30 tahun",
        produk_penggunaan=["Wadah makanan", "Sedotan", "Alat medis"],
        environmental_impact="Relatif lebih ramah lingkungan dibanding jenis plastik lain, namun tetap membutuhkan waktu lama untuk terurai. Dapat mencemari lingkungan jika tidak didaur ulang dengan benar."
    ),
    "PS": PlasticInfo(
        nama="Polystyrene (PS)",
        simbol_kode="6",
        description="PS adalah plastik yang umum ditemukan dalam bentuk styrofoam dan digunakan untuk kemasan sekali pakai serta isolasi.",
        recycling_time="50-500 tahun",
        produk_penggunaan=["Kemasan styrofoam", "Cangkir sekali pakai", "Isolasi"],
        environmental_impact="Sangat berbahaya bagi lingkungan, sulit didaur ulang, mudah hancur menjadi mikroplastik. Mengandung bahan karsinogenik yang dapat mencemari makanan saat terkena panas."
    )
}

app = Flask(__name__)
CORS(app)

storage_client = storage.Client()
BUCKET_NAME = 'replaste_bucket1'
bucket = storage_client.bucket(BUCKET_NAME)

def compress_image(image, max_size=(800, 800), quality=85):
    """Compress and resize image while maintaining aspect ratio"""

    width, height = image.size
    aspect_ratio = width / height
    
    if width > max_size[0] or height > max_size[1]:
        if aspect_ratio > 1:
            new_width = min(width, max_size[0])
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, max_size[1])
            new_width = int(new_height * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    compressed_io = BytesIO()
    
    image.save(compressed_io, format='JPEG', quality=quality, optimize=True)
    compressed_io.seek(0)
    
    return Image.open(compressed_io)

def upload_to_storage(file_bytes, file_name):
    """Upload file to Google Cloud Storage and return public URL"""
    folder_name = "history-prediksi"
    full_path = f"{folder_name}/{file_name}"
    
    image = Image.open(file_bytes).convert("RGB")
    compressed_image = compress_image(image)
    
    upload_io = BytesIO()
    compressed_image.save(upload_io, format='JPEG', quality=85, optimize=True)
    upload_io.seek(0)
    
    blob = bucket.blob(full_path)
    blob.upload_from_string(upload_io.getvalue(), content_type='image/jpeg')
    return f"https://storage.googleapis.com/{BUCKET_NAME}/{full_path}"

def preprocess_image(image, target_size):
    """Resize image to target size and preprocess it for the model."""
    compressed_image = compress_image(image)
    
    img = compressed_image.resize(target_size, Image.Resampling.LANCZOS)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    if "user_id" not in request.form:
        return jsonify({"error": "user_id is required"}), 400
    
    file = request.files["file"]
    user_id = request.form["user_id"]

    try:
        image = Image.open(file.stream).convert("RGB")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"prediction_{user_id}_{timestamp}.jpg"
        
        file.seek(0)
        image_url = upload_to_storage(file, file_name)
        
        target_size = model.input_shape[1:3]
        img_array = preprocess_image(image, target_size)
        
        with tf.device('/CPU:0'):
            predictions = model.predict(img_array, batch_size=1)
        
        predicted_index = np.argmax(predictions)
        predicted_class = class_names[predicted_index]
        confidence = float(np.max(predictions)) * 100
        
        prediction_id = save_prediction(
            user_id=user_id,
            image_url=image_url,
            file_name=file_name,
            jenis_plastik=predicted_class,
            confidence_score=confidence
        )
        
        plastic_detail = plastic_info[predicted_class].to_dict()
        
        return jsonify({
            "predicted_class": predicted_class,
            "confidence": f"{confidence:.2f}%",
            "plastic_info": plastic_detail,
            "prediction_id": prediction_id,
            "image_url": image_url
        })
        
    except Exception as e:
        print(f"Error processing prediction: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))