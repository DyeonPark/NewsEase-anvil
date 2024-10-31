import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json

from datetime import datetime


@anvil.server.callable
def get_articles_list():
  return app_tables.article_tb.search(level=1)


@anvil.server.callable
def get_article_by_id(title_id):
  article_row = list(app_tables.article_tb.search(title_id=title_id, level=1))

  if article_row:
    return {
      "title": article_row[0]["title"],
      "article": article_row[0]["article"],
      "date": article_row[0]["date"],
      "img_url": article_row[0]["img_url"],
      "tts_audio": article_row[0]["tts_audio"],
      "origin_url": article_row[0]["origin_url"]
    }
  return "조건에 맞는 데이터를 찾을 수 없습니다"


@anvil.server.callable
def get_article_by_title_n_level(title_id, level):
  article_row = list(app_tables.article_tb.search(title_id=title_id, level=level))
  if article_row:
    return {
      "article": article_row[0]["article"],
      "img_url": article_row[0]["img_url"],
      "tts_audio": article_row[0]["tts_audio"]
    }
  return "조건에 맞는 데이터를 찾을 수 없습니다"


@anvil.server.http_endpoint("/add_article", methods=["POST"])
def add_article_api():
  try:
    from datetime import datetime
    metadata = anvil.server.request.body_json
    # date_obj = datetime.fromisoformat(metadata.get("date").date()

    app_tables.article_tb.add_row(
      title_id=metadata.get("title_id"),
      date=datetime.now().date(),
      title=metadata.get("title"),
      level=metadata.get("level"),
      article=metadata.get("article"),
      img_url=metadata.get("img_url"),
      origin_url=metadata.get("origin_url"),
      abstract=metadata.get("abstract"),
      # tts_audio=anvil.media.from_file(tts_audio, name=f"tts_audio_{metadata.get("level")}.mp3")
    )
    
    return {"status": "success", "message": "Article added successfully!"}
    
  except Exception as e:
    return {"status": "error", "message": str(e)}    
  
@anvil.server.http_endpoint("/max_id", methods=['GET'])
def get_max_id():
    rows = app_tables.article_tb.search()
    max_id = max([row['title_id'] for row in rows])
    return {"max_id": max_id}