# REPLASTE - C242-PS448
## Table of Contents

1. [Team C242-PS448 - CC](#Team-C242-PS448---CC)
2. [What is REPLASTE?](#REPLASTE)
3. [Technology](#Technology)
4. [Installation](#Installation)
5. [Deployment](#Deployment)


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

## Installation and Usage of Flask Application

This application uses Flask as a web framework to create an image prediction API using a TensorFlow model. Several dependencies must be installed before running the application.

## Requirement
Make sure you have installed:

Python 3.9 or newer
pip (package installer for Python)
Virtual environment (optional but recommended)

## Deployment
### 1. Create a Docker Image
Run the following command to build the Docker image:
```
gcloud builds submit --tag gcr.io/my-firstproject-441503/plastic-classifier
```

### 2. Deploy to Cloud Run
Deploy the Docker image to Cloud Run using the following command:
```
gcloud run deploy plastic-classifier \
  --image gcr.io/replaste-442106/plastic-classifier \
  --platform managed \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars="DB_HOST=your_db_ip,DB_USER=your_db_user,DB_PASS=your_db_pass,DB_NAME=your_db_name"
```
Make sure to replace your_db_ip, your_db_user, your_db_pass, and your_db_name with your actual database credentials.
