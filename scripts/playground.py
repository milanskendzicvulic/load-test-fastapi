from app.cats.models.cat_model import Cat

from app.db.session import session_context

with session_context() as session:
    result = session.query()

    debugger = 1
