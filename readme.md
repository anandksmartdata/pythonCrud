FOR MIGRATIONS SCRIPTS AS BELOW.....

export FLASK_APP=init.py
flask db init
flask db migrate
flask db upgrade

flask db migrate -m "Adding column x."
https://copyprogramming.com/howto/sqlalchemy-how-to-add-column-to-existing-table

flask shell
from your_application.models import Userdetails
Userdetails.**table**.columns.keys()
