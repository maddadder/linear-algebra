sudo apt-get install python3-tk
cd ~/linear-algebra
python3 -m venv ./env
source env/bin/activate
pip install -r requirements.txt

cd ~/linear-algebra
source env/bin/activate
python app.py
