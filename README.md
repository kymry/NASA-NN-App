# Nasa-ML-API

A work in progress. Check back soon!

A web app that aggregates data and images from various NASA and other astronomical APIs and allows users to create accounts and subscribe to the APIs of their choosing. Once subscribed, a daily email with the newest data from the user's subscriptions will be sent to their inbox.  

The app also allows a user to upload an unlabeled image of a planet from our solar system. A trained convolutional neural network will then be used to classify the planet image. 

- Built in Python using Flask and Bootstrap
- MongoDB used to store raw JSON from NASA apis
- SQLite used to store processed data in a relational manner 
- Local file system used to store images
- Python built web crawler to obtain images of planets in our solar system to be used for training a CNN
- TensorFlow used to train a CNN to classify images of planets in our solar system 

Flask Details 

- flask_sqlalchemy for SQL ORM 
- flask_pymongo for MongoDb 
- flask_apscheduler for scheduling daily API calls
- flask_wtf for user forms
- Flask-Login for user account creation and management
