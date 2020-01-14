# Nasa-ML-API

A work in progress. Check back soon!

A web app that aggregates astronomical data from the NASA api, feeds the data to ML models and allows the user to explore predictions. E.g. a user can enter a future data and the predicted temperature on Mars on that date will be returned. 

- Built in Python using Flask and Bootstrap
- MongoDB used to store raw JSON from NASA apis
- SQLite used to store processed data in a relational manner that allows it to be consumed by ML models
- Python built web crawler to obtain images of planets in our solar system to be used for training NN
- Scikit Learn and TensorFlow used for model creation and training (e.g Mars temperature data prediction)
- Python's Pickle used to serialize and store the learned models
- A custom built (albeit simple) deep neural network built in Python that allows planet image classification (from our solar system) 
