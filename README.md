## Setup & Run
First, install [Python 3.x](https://www.python.org/downloads/).

### venv
Set up a virtual environment using the following command:
```bash
python -m venv venv
```

Then, activate the virtual environment. 

On windows: 
```bash
.\venv\Scripts\activate
```
On macOS and Linux:
```bash
source env/bin/activate
```
If you want to switch projects or otherwise leave your virtual environment, simply run:
```bash
deactivate
```

### Installing the Requirements
Project is built using Python web framework - Flask.
Flask and all the other dependency modules can be installed from the commandline using `pip` manager:

```bash
pip install -r dev-requirements.txt
```

### Run 
Run the following command:
```bash
flask run
```
