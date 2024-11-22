pip install -r requirements.txt
python app.py
#gunicorn -w 4 -b 0.0.0.0:5000 app:app