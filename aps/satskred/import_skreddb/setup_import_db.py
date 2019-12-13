# Creates an SQLite database with three tables that should hold the avalanche information
# check: https://thinkdiff.net/python/how-to-use-python-sqlite3-using-sqlalchemy/
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# Global Variables
SQLITE = 'sqlite'

# Table Names
H = 'hendelse' # contains point data
U = 'utloputlosningsomr' # contains polygon data
T = 'tekniske' # contains technical parameters

