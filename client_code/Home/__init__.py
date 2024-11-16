from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Load datas from server
    articles = anvil.server.call('get_articles_list')

    self.adsense_html_1.html = "<div></div>"
    
    # Put data to repeating panel
    self.news_repeating_panel.items = articles

  def title_link_click(self, **event_args):
    open_form('Home')
