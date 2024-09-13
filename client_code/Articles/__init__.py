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
    self.title_id = title_id
    self.load_article_details(title_id)

  def load_article_details(self, title_id):
    article_data = anvil.server.call("get_article_by_id", title_id)

    if article_data:
      self.article_title.text = article_data["title"]
      self.article_context.text = article_data["article"]
    else:
      print(f"해당 기사를 찾을 수 없습니다: id is {title_id}")

  def link_1_click(self, **event_args):
    text = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=1)
    self.article_context.text = text

  def link_2_click(self, **event_args):
    text = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=2)
    self.article_context.text = text

  def link_3_click(self, **event_args):
    text = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=3)
    self.article_context.text = text
