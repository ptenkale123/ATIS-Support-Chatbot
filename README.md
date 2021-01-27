# Air Travel Support Chatbot

Chatbot that you can use to find flight/travel information

Steps to run the project:

1. Install the Rasa python package https://rasa.com/docs/rasa/installation. As of January 18, it does not work on Python 3.9 so you might have to downgrade to a lower Python version (I used Python 3.7).
2. Open a terminal, cd into '/rasa_train_test' and run 'rasa run --enable-api -m models/nlu-originalTrainingData.tar.gz'
3. Open another terminal, cd into '/chatbot_code' and run 'python3 chatbot.py'. You can type in this terminal for all your queries

I use Google Places + Google Distance Matrix + Bing Search APIs. 
The API keys that I use are not available on this public repository, so you will need to request those from Google Cloud Platform and Microsoft Azure.
