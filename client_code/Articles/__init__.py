from ._anvil_designer import ArticlesTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Articles(ArticlesTemplate):
  def __init__(self, article_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.load_article_details(article_id)

  def load_article_details(self, article_id):
    article_data = anvil.server.call("get_", article_id)