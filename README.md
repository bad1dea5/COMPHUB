
# COMPHUB
#### version: 0.0.2

### Requirements
- `Python 3.10.2`

### Development

1. `python3 -m venv venv`

  -- `. venv/bin/activate` on **Linux**
  -- `venv\Scripts\activate` on **Windows**

2. `pip install -r requirements.txt`
3. `npm install`
4. `npm run build`

5. `flask db init`
6. `flask db migrate`
7. `flask db upgrade`

  - `export FLASK_ENV=development` on **Linux**
  - `set FLASK_ENV=development` on **Windows**

8. `flask run`
