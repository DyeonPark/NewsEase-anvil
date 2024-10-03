from ._anvil_designer import ArticlesTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Articles(ArticlesTemplate):
  def __init__(self, article_data, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    #Load data using article_id
    self.title_id = article_data["title_id"]
    self.origin_url = article_data["origin_url"]
    self.load_article_details(self.title_id)

  
  def load_article_details(self, title_id):
    article_data = anvil.server.call("get_article_by_id", title_id)

    if article_data:
      self.article_title.text = article_data["title"]
      self.article_context.text = article_data["article"]
      self.title_img.source = article_data["img_url"]
      self.audio_player.src = article_data["tts_audio"].get_url(True)
    else:
      print(f"해당 기사를 찾을 수 없습니다: id is {title_id}")

  
  def link_1_click(self, **event_args):
    article_data = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=1)
    self.article_context.text = article_data["article"]
    self.title_img.source = article_data["img_url"]
    self.call_js('setAudioSource', article_data["tts_audio"].get_url(True))

  
  def link_2_click(self, **event_args):
    article_data = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=2)
    self.article_context.text = article_data["article"]
    self.title_img.source = article_data["img_url"]
    self.call_js('setAudioSource', article_data["tts_audio"].get_url(True))

  
  def link_3_click(self, **event_args):
    article_data = anvil.server.call('get_article_by_title_n_level', title_id=self.title_id, level=3)
    self.article_context.text = article_data["article"]
    self.title_img.source = article_data["img_url"]
    self.call_js('setAudioSource', article_data["tts_audio"].get_url(True))
