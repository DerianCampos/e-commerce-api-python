import os
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from typing import Dict, Optional
from .redis_client import connect_redis, close_redis
from .cache.product_cache import get_product, invalidate_product
from .db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product
from .schemas import ProductRead, ProductCreate, ProductUpdate

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await connect_redis()

@app.on_event("shutdown")
async def on_shutdown():
    await close_redis()

async def _load_product_from_db(product_id: int, session: AsyncSession) -> Optional[dict]:
    obj = await session.get(Product, product_id)
    if obj is None:
        return None
    # convert SQLAlchemy object to dict
    return {"id": obj.id, "name": obj.name, "price": float(obj.price), "updated_at": obj.updated_at.isoformat() if obj.updated_at else None}

@app.get("/products/{product_id}", response_model=ProductRead)
async def read_product(product_id: int, session: AsyncSession = Depends(get_session)):
    async def loader(pid: int):
        return await _load_product_from_db(pid, session)

    product = await get_product(product_id, loader, ttl_seconds=300)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=ProductRead)
async def create_product(payload: ProductCreate, session: AsyncSession = Depends(get_session)):
    p = Product(name=payload.name, price=payload.price)
    session.add(p)
    await session.commit()
    await session.refresh(p)
    # invalidate just in case
    await invalidate_product(p.id)
    return {"id": p.id, "name": p.name, "price": float(p.price), "updated_at": p.updated_at.isoformat() if p.updated_at else None}

@app.put("/products/{product_id}")
async def update_product(product_id: int, payload: ProductUpdate, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    p = await session.get(Product, product_id)
    if p is None:
        raise HTTPException(status_code=404, detail="Not found")
    if payload.name is not None:
        p.name = payload.name
    if payload.price is not None:
        p.price = payload.price
    session.add(p)
    await session.commit()
    await session.refresh(p)
    background_tasks.add_task(invalidate_product, product_id)
    return {"ok": True}
