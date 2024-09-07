from ._anvil_designer import item_cardTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class item_card(item_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.cd_title.content = self.item["title"]
    self.cd_txt.content = self.item["article"]

    self.set_event_handler('', self.cd_link_click)

  def cd_link_click(self, **event_args):
    article_id = self.item["id"]
    open_form("Articles", article_id=article_id)
    