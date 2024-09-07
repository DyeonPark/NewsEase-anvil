import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable
def get_articles():
  return app_tables.article_tb.search()


@anvil.server.callable
def get_article_by_id(title_id):
  article_row = app_tables.article_tb.get(title_id=title_id)

  if article_row:
    return {
      "title": article_row["title"],
      "article": article_row["article"],
      "date": article_row["date"]
    }
  else:
    alert("Can't find article row")
    return None

@anvil.server.http_endpoint("/add_article", methods=["POST"])
def add_article_api():
  from datetime import datetime
  try:
    data = anvil.server.request.body_json

    title_id = data.get("title_id")
    title = data.get("title")
    date_str = data.get("date")
    level = data.get("level")
    article = data.get("article")
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    app_tables.article_tb.add_row(
      title_id=title_id,
      title=title,
      date=date_obj,
      level=level,
      article=article
    )
    
    return {"status": "success", "message": "Article added successfully!"}
    
  except Exception as e:
    return {"status": "error", "message": str(e)}    
  
