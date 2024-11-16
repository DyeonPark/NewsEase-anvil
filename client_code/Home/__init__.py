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
    
    # Put data to repeating panel
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Articles"

  def title_link_click(self, **event_args):
    open_form('Home')

  def news_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'news')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "News"

  def sports_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'sports')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Sports"

  def business_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'business')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Busineess"

  def innovation_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'innovation')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Innovation"

  def culture_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'culture')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Culture"

  def travel_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'travel')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Travel"

  def earth_link_click(self, **event_args):
    articles = anvil.server.call('get_articles_list', 'earth')
    self.news_repeating_panel.items = articles
    self.sub_title.text = "Earth"