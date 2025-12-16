import logging

from fastapi import FastAPI

from app.dependencies.db_dependency import SessionDep

from app.cats.models.cat_model import Cat
from app.cats.schemas.cat_schema import CatCreateResponse


logging.getLogger().setLevel(level=logging.INFO)


app = FastAPI()


@app.get(path="/api/cats")
def cats(session: SessionDep):
    stmt = select(Cat).limit(500).offset(0)
    result = session.execute(stmt)
    return result.scalars().all()


@app.get(path="/api/cats/create", response_model=CatCreateResponse)
def cats_create(session: SessionDep):
    try:
        new_cat = Cat(name="Kat")
        session.add(instance=new_cat)

        session.commit()
        session.refresh(instance=new_cat)

        return new_cat
    except Exception as e:
        logging.exception(msg=f"Failed to create a cat: {e}", exc_info=True)
        session.rollback()
        raise e


######################################################################

from app.db.session_async import AsyncSession, get_async_db
from sqlalchemy import select
from fastapi import Depends


@app.get("/api/cats/async")
async def cats_async(session: AsyncSession = Depends(get_async_db)):
    stmt = select(Cat).limit(500).offset(0)

    result = await session.execute(stmt)
    return result.scalars().all()


@app.get("/api/cats/create/async", response_model=CatCreateResponse)
async def cats_create_async(session: AsyncSession = Depends(get_async_db)):
    try:
        new_cat = Cat(name="Kat")
        session.add(new_cat)

        await session.commit()
        await session.refresh(new_cat)

        return new_cat

    except Exception:
        logging.exception("Failed to create a cat")
        await session.rollback()
        raise
