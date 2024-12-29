import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables, query
import anvil.server

import json
import pytz
from datetime import datetime, timedelta

@anvil.server.callable
def get_articles_list(cate: str = None):
  if cate:
    articles = app_tables.article_meta_tb.search(category=cate)
  else:
    articles = app_tables.article_meta_tb.search()
  sorted_articles = sorted(articles, key=lambda x: x["date"], reverse=True)
  return sorted_articles

@anvil.server.callable
def get_word_list(title_id: int, level: int):
  response = app_tables.article_words.search(title_id=title_id, level=level)
  word_ids = [row['word_id'] for row in response]

  items = []
  for id in word_ids:
    row = app_tables.word_tb.get(word_id=id)
    items.append({"word": row["word"], "meaning": row["meaning"], "synonyms": row["synonyms"]})
  sorted_items = sorted(items, key=lambda x: x["word"], reverse=True)
  return sorted_items

@anvil.server.callable
def get_article_by_id(title_id):
  meta_row = list(app_tables.article_meta_tb.search(title_id=title_id))
  if meta_row:
    return {
      "title": meta_row[0]["title"],
      "date": meta_row[0]["date"],
      "img_url": meta_row[0]["img_url"],
    }
  return "조건에 맞는 데이터를 찾을 수 없습니다"


@anvil.server.callable
def get_article_by_title_n_level(title_id, level):
  article_row = list(app_tables.article_level_tb.search(title_id=title_id, level=level))
  if article_row:
    return {
      "article": article_row[0]["article"],
      "tts_audio": article_row[0]["tts_audio"]
    }
  return "조건에 맞는 데이터를 찾을 수 없습니다"


@anvil.server.http_endpoint("/add_article_meta", methods=["POST"])
def add_article_meta_api():
  try:
    from datetime import datetime
    metadata = anvil.server.request.body_json
    app_tables.article_meta_tb.add_row(
      title_id=metadata.get("title_id"),
      title=metadata.get("title"),
      date=datetime.now(pytz.timezone("Asia/Seoul")),
      category=metadata.get("category"),
      img_url=metadata.get("img_url"),
      origin_url=metadata.get("origin_url"),
      abstract=metadata.get("abstract")
    )
    return {"status": "success", "message": "Article meta data added successfully!"}
  except Exception as e:
    return {"status": "error", "message": str(e)} 


@anvil.server.http_endpoint("/add_article_level", methods=["POST"])
def add_article_level_api():
  try:
    from datetime import datetime
    metadata = anvil.server.request.body_json
    app_tables.article_level_tb.add_row(
      title_id=metadata.get("title_id"),
      article=metadata.get("article"),
      level=metadata.get("level")
    )
    return {"status": "success", "message": "Article level data added successfully!"}
  except Exception as e:
    return {"status": "error", "message": str(e)} 


@anvil.server.http_endpoint("/add_article_audio", methods=["POST"])
def add_article_audio(title_id, level):
  try:
    file_data = anvil.server.request.body.get_bytes()
    audio_file = anvil.BlobMedia("audio/mpeg", file_data, name="audio.mp3")

    row = app_tables.article_level_tb.search(title_id=int(title_id), level=int(level))
    # 검색된 행이 없거나 여러 개인 경우 처리
    if not row or len(row) > 1:
      return {"status": "error", "message": "Row not found or multiple rows matched"}

    matched_row = row[0]
    matched_row['tts_audio'] = audio_file
    
    return {"status": "success", "message": "Audio file updated successfully!"}
  except Exception as e:
    return {"status": "error", "message": str(e)}    


@anvil.server.http_endpoint("/add_article_words", methods=["POST"])
def add_article_words_api():
  try:
    from datetime import datetime
    metadata = anvil.server.request.body_json

    row = app_tables.word_tb.search(word=metadata.get("word"))
    if len(row) == 0:
      app_tables.word_tb.add_row(
        word_id=metadata.get("word_id"),
        word=metadata.get("word"),
        meaning=metadata.get("meaning"),
        synonyms=metadata.get("synonyms")
      )

    row = app_tables.word_tb.search(word=metadata.get("word"))
    if not row or len(row) > 1:
      return {"status": "error", "message": "Row not found or multiple rows matched"}

    matched_row = row[0]
    word_id = matched_row['word_id']
    
    app_tables.article_words.add_row(
      title_id=metadata.get("title_id"),
      level=metadata.get("level"),
      word_id=word_id,
    )
    return {"status": "success", "message": "Word data added successfully!"}
  except Exception as e:
    return {"status": "error", "message": str(e)} 


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
  rows = app_tables.article_meta_tb.search()
  if len(rows):
    max_id = max([row['title_id'] for row in rows])
    return {"max_id": max_id}
  return {"max_id": -1}


@anvil.server.http_endpoint("/existed_word", methods=['POST'])
def is_existed_word(word: str):
  rows = app_tables.word_tb.search(word=word)
  if len(rows):
    return {"exist": True}
  return {"exist": False}


@anvil.server.http_endpoint("/max_word_id", methods=['GET'])
def get_max_word_id():
  rows = app_tables.word_tb.search()
  if len(rows):
    max_id = max([row['word_id'] for row in rows])
    return {"max_word_id": max_id}
  return {"max_word_id": -1}
  

@anvil.server.http_endpoint("/daily", methods=['POST'])
def get_daily_visitors(date: str):
  try:
    target_date = datetime.strptime(date, "%Y%m%d").date()
    start_of_day = target_date
    end_of_day = target_date + timedelta(days=1) - timedelta(seconds=1)

    rows = app_tables.visitors.search(timestamp=query.between(start_of_day, end_of_day))
    formatted_rows = [datetime.strftime(row['timestamp'], '%Y-%m-%d %H:%M:%S') for row in list(rows)]
    return {"count": len(formatted_rows), "logs": formatted_rows}
  except Exception as e:
    return {"error": str(e)}

  
@anvil.server.callable
def log_visit(path):
  utc_now = datetime.now(pytz.utc)
  kst_now = utc_now.astimezone(pytz.timezone('Asia/Seoul'))
  app_tables.visitors.add_row(
    timestamp=kst_now,
    path=path
  )