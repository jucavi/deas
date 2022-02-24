
# Nearest DEAS

Find nearest deas based on data from [Datos abiertos de la comunidad de madrid](https://www.comunidad.madrid/gobierno/datos-abiertos)

## Usage

1. Clone repository
 
       $ git clone https://github.com/jucavi/deas.git
  
2. Create virtual enviroument and activate it

        $ python3 -m venv .venv
  
        $ source .venv/bin/activate
  
3. Install dependencies

        $ pip3 install -r requirements.txt
  
4. Setup database

        $ flask init-db
        
5. Populate database

        $ python3 dea.py
        
6. Start api server

        $ python3 api.py
        
7. In other terminal run app

        $ python3 server.py
        
8. Go to [honey app](http://127.0.0.1:5000/)
9. You can found a project [here](https://jucavi.eu.pythonanywhere.com/)
 
