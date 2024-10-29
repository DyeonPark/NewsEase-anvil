import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json


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
    data = anvil.server.request.body_json
    file = anvil.server.request.files.get("file")
    metadata = anvil.server.request.form.get("metadata")

    if metadata:
      metadata = json.loads(metadata)
    else:
      return {"status": "error", "message": "Missing metadata"}

    title_id = metadata.get("title_id")
    # title_id = data.get("title_id")
    title = data.get("title")
    date_str = data.get("date")
    level = data.get("level")
    article = data.get("article")
    tts_audio = data.get("tts_audio")
    img_url = data.get("img_url")
    origin_url = data.get("origin_url")

    app_tables.article_tb.add_row(
      title_id = title_id,
      title = title,
      date = date_obj,
      level = level,
      article = article,
      tts_audio = tts_audio,
      img_url = img_url,
      origin_url = origin_url
    )
    
    return {"status": "success", "message": "Article added successfully!"}
    
  except Exception as e:
    return {"status": "error", "message": str(e)}    
  
@anvil.server.http_endpoint("/max_id", methods=['GET'])
def get_max_id():
    rows = app_tables.article_tb.search()
    max_id = max([row['title_id'] for row in rows])
    return {"max_id": max_id}