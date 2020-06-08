Repository om de mismatch op de Nederlandse tech arbeidsmarkt inzichtelijk te maken middels een GAP report. In eerste instantie wordt er gekeken naar de aanbod zijde en dan specifiek voor een vijftal profielen (zie image) die [Tekkieworden](https://tekkieworden.nl/) heeft opgesteld. Hoe de vraagzijde zich daartoe verhoudt wordt apart onderzocht maar zal uiteindelijk in dit project moeten worden bijgevoegd.



![profielen](/home/diederik/projects/tekkieworden/docs/images/tech_profielen.png)



Install the `TEKKIEWORDEN` package

 - `git clone https://github.com/rmania/tekkieworden.git`
 -  git remote set-url origin git+ssh://git@github.com/rmania/tekkieworden.git
 - `python -m venv venv`
 - `virtualenv --python=$(which python=3.7) venv`
 - `source venv/bin/activate`

 - `pip install -e .` (assuming setup.py is in this directory)

 Or with tox:

 `tox -e install_locally`

 To also have access to the tekkieworden virtual env in Jupyter Notebooks or Lab:
 - `pip install ipykernel`
 - `python -m ipykernel install --user --name tekkieworden --display-name "tekkieworden"`

### Different scripts to launch (still separated blocks) 
 **download files**
 - `python tekkieworden/processing/readers.py`

 **clean, join and prepare files**
 - `python tekkieworden/processing/munge.py`

 **create GAP report PFD**
 - `python tekkieworden/processing/create_gap_report.py`

 **launch app**
 - `streamlit run visual_app.py`
