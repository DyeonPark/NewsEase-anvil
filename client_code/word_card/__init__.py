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

    self.word.text = self.item["word"]
    self.word_meaning.text = self.item["meaning"]
    self.word_synonyms.text = self.item["synonyms"]
    
    # self.cd_link.set_event_handler('click', self.card_click)
