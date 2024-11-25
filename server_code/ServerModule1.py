import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json

from datetime import datetime


@anvil.server.callable
def get_articles_list(cate: str = None):
  if cate:
    articles = app_tables.article_tb.search(level=1, category=cate)
  else:
    articles = app_tables.article_tb.search(level=1)
  sorted_articles = sorted(articles, key=lambda x: x["date"], reverse=True)
  return sorted_articles

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

    app_tables.article_tb.add_row(
      title_id=metadata.get("title_id"),
      date=datetime.now().date(),
      title=metadata.get("title"),
      level=metadata.get("level"),
      article=metadata.get("article"),
      img_url=metadata.get("img_url"),
      origin_url=metadata.get("origin_url"),
      abstract=metadata.get("abstract"),
    )
    
    return {"status": "success", "message": "Article added successfully!"}
    
  except Exception as e:
    return {"status": "error", "message": str(e)}    

@anvil.server.http_endpoint("/add_audio", methods=["POST"])
def add_audio_api(title_id, level):
  try:
    file_data = anvil.server.request.body.get_bytes()
    audio_file = anvil.BlobMedia("audio/mpeg", file_data, name="audio.mp3")

    # query_params = anvil.server.request.query_params
    # title_id = query_params.get('title_id')
    # level = query_params.get('level')

    row = app_tables.article_tb.search(title_id=int(title_id), level=int(level))
    # 검색된 행이 없거나 여러 개인 경우 처리
    if not row or len(row) > 1:
      return {"status": "error", "message": "Row not found or multiple rows matched"}

    matched_row = row[0]
    matched_row['tts_audio'] = audio_file
    
    return {"status": "success", "message": "Audio file updated successfully!"}
  except Exception as e:
    return {"status": "error", "message": str(e)}    
  
@anvil.server.http_endpoint("/max_id", methods=['GET'])
def get_max_id():
    rows = app_tables.article_tb.search()
    max_id = max([row['title_id'] for row in rows])
    return {"max_id": max_id}

@anvil.server.callable
def log_visit(path):
  app_tables.visitors.add_row(
    timestamp=datetime.now(),
    path=path
  )
  