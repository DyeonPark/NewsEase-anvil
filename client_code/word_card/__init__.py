from ._anvil_designer import word_cardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class word_card(word_cardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.cd_title.content = self.item["title"]
    self.cd_txt.content = self.item["abstract"]
    self.card_img.source = self.item["img_url"]

    self.word.
    
    self.cd_link.set_event_handler('click', self.card_click)
