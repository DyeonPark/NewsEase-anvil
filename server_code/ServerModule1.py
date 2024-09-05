import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#https://mellow-blond-external.anvil.app/_/api/test_connection
# @anvil.server.callable
# def get_articles():
#   return app_

# @anvil.server.http_endpoint("test_connection", methods=["POST"])
# def get_test_connection():
#   return {"status": "Success", "message": "return-from-get"}

@anvil.server.route('/add/:a/:b')
def add_numbers(a, b):
  a = int(a)
  b = int(b)
  return {
    'originals': [a, b],
    'sum': a + b,
  }