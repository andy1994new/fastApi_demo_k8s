# main.py
"""This module provides order-related APIs for order creation and retrieval."""

import logging
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import models
from database import engine, get_db
from schemas import OrderRequestSchema, OrderItemSchema, OrderSchema
import httpx
from utils import validate_product_stock, generate_order, generate_order_items, product_update, user_update


models.Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.get("/order")
def get_index():
    """Handle GET request for the root endpoint."""
    return {"msg": "Order service"}

@app.post("/order")
async def post_order(request: OrderRequestSchema, db: Session = Depends(get_db)):
    try:
        products = await validate_product_stock(request, "http://localhost:8001/product/getlist", client=httpx.AsyncClient())
        order = generate_order(products, request)
        db.add(order)
        db.commit()
        db.refresh(order)

        items = generate_order_items(products, order)
        for item in items:
            db.add(item)
            db.commit()
            db.refresh(item)
        
        await product_update(products,  "http://localhost:8001/product", client=httpx.AsyncClient())

        await user_update(order, "http://localhost:8000/user", client=httpx.AsyncClient())
        
        return order

    except HTTPException as e:
        # Handle the exception if any product is missing
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
@app.get("/order/{order_id}", response_model=OrderSchema)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="User not found")
    return order

@app.get("/order/items/{order_id}", response_model=list[OrderItemSchema])
def get_items_by_id(order_id: int, db: Session = Depends(get_db)):
    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).first()
    if not items:
        raise HTTPException(status_code=404, detail="User not found")
    return items