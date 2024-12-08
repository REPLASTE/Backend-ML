# REPLASTE - C242-PS448
## Table of Contents

1. [Team C242-PS448 - CC](#Team-C242-PS448---CC)
2. [What is REPLASTE?](#REPLASTE)
3. [Technology](#Technology)
4. [Installation](#Installation)
5. [Database Configuration](#Database-Configuration)
6. [Running the Project](#Running-the-Project)
7. [API Endpoints](#API-Endpoints)


## Team ENTS-H1137 - CC

| Bangkit ID | Name | Learning Path | University |LinkedIn |
| ---      | ---       | ---       | ---       | ---       |
| C488B4KY0483 | Anantha Marcellino Hidayat | Cloud Computing | Universitas Darma Persada | [![text](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/ananthamarcellino/) |
| C001B4KX0664 | Arneleonita Putri Arinto | Cloud Computing |	Institut Pertanian Bogor  | [![text](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arneleonita/) |

## REPLASTE

this application can detect and classify various plastic waste items using computer vision and a Convolutional Neural Network (CNN) model. By integrating this AI-powered recognition capability into the app, we can offer users real-time guidance on the appropriate recycling or disposal methods for each type of plastic. This will empower individuals to make more informed decisions and develop sustainable waste management habits.

## Technology
The REPLASTE project is built using the following technologies:
Flask: A lightweight WSGI web application framework in Python used to build the web server.

TensorFlow and Keras    : Machine learning libraries used to load and make predictions with a pre-trained model (model.h5).

NumPy                   : A library for numerical computations in Python, used here for handling array operations.

Google Cloud Storage    : A service for storing and retrieving files on Google Cloud, used to upload and manage image files.

Pillow                  : A Python Imaging Library (PIL) fork, used for image processing.

Gunicorn                : A Python WSGI HTTP server for running web applications in production.

Flask-cors              : An extension for Flask that allows cross-origin resource sharing (CORS).

Python-dotenv           : A library used to load environment variables from a .env file into the application.

io                      : A module for handling the byte streams, used to manage in-memory binary streams.

# Installation and Usage of Flask Application

This application uses Flask as a web framework to create an image prediction API using a TensorFlow model. Several dependencies must be installed before running the application.

## Requirement
Make sure you have installed:

Python 3.9 or newer
pip (package installer for Python)
Virtual environment (optional but recommended)

## Installation Steps

1. Clone the Repository
Clone the repository from GitHub to your computer.

```bash
git clone https://github.com/REPLASTE/Backend-ML.git
cd Backend-ML
```

2. Create and Activate a Virtual Environment

```
python -m venv .venv
```

- Windows:

```
.venv\Scripts\activate
```

- Linux & MacOS:

```
source .venv/bin/activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```
4. Ensure Model and Data Availability
Make sure the model file (model.h5) is available in the project's root directory.

5. Run the Application
Run the Flask application using the following command:

```bash
python local.py
```

Open your browser and go to http://0.0.0.0:8080 to check the API.

## API Endpoints

Predict
This endpoint is used to upload an image and get a prediction.

URL: /predict
Method: POST
Content-Type: multipart/form-data
Form Data:
image: File gambar (jpg, jpeg, png)

## Usage

Use the /predict endpoint to make predictions based on the input image.

```
curl -X POST -F "image=@path/to/your/image.jpg" http://0.0.0.0:8080/predict
```

Replace path/to/your/image.jpg with the path to the image file you want to predict.

## Example Response

```
{
    "confidence": "94.24%",
    "plastic_info": {
        "Description": "LDPE adalah plastik fleksibel yang sering digunakan untuk kantong plastik dan film pembungkus.",
        "name": "Low-Density Polyethylene (LDPE)",
        "recycling_symbol": "4",
        "recycling_time": "10-100 tahun,
        "uses": [
            "kantong plastik"
            "film pembungkus"
            "Lapisan karton minuman"
        ]
}
```
