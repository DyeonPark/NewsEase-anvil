from ._anvil_designer import ArticlesTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Articles(ArticlesTemplate):
  def __init__(self, title_id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # # Load data using article_id
    self.load_article_details(title_id)

  def load_article_details(self, title_id):
    article_data = anvil.server.call("get_article_by_id", title_id)

    if article_data:
      self.article_title.text = article_data["title"]
      self.article_context.text = article_data["article"]
    else:
      print(f"해당 기사를 찾을 수 없습니다: id is {title_id}")