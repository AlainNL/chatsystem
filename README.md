### Install Back-End with Flask ###
"Create virtual environement & activate"
`cd back`
`python3 -m venv env`
`source env/bin/activate`

#Install the requirements
`pip install -r requirements.txt`

#run Flask with Gevent
`python app.py`

adress server at "http://127.0.0.1:5000/chat

### Run Front-End with React ###

`cd front`
`npm install`
`npm run start`

run the server at "http://localhost:3000"

### Run API test ###
`pytest api_test.py`
