## 惑星・Wakusei - Astronomy API aggregation web application

A work in progress.

A web app that aggregates data and images from various third-party astronomical APIs (e.g. NASA) and allows users to create accounts and subscribe to the APIs of their choosing. Once subscribed, a daily email with the newest data from the user's subscriptions will be sent to their inbox.  

### Tech Stack
- Built in Python
- Flask for the backend
- Bootstrap, HTML5, Javascript (AJAX) for the frontend
- MongoDB used to store raw JSON files from the various APIs
- SQLite used to store user profiles and structured API data
- File system used to store images
- Docker for easy deployment and maintenance
- Mailchimp for daily emails from distribution list

### Features
- [x] User profile creation
- [x] Users can tailor their subscriptions to fit their tastes
- [x] New data from third-party APIs is retrieved daily
- [x] Error handling handled gracefully
- [x] Logging

### Flask Details
- flask_sqlalchemy for SQL ORM
- flask_pymongo for MongoDb
- flask_apscheduler for scheduling daily API calls
- flask_wtf for user forms
- Flask-Login for user account creation and management
