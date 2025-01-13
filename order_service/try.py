@app.post("/order")
async def post_order(request: OrderRequestSchema, db: Session = Depends(get_db)):
    """
    Create a new order with associated items.

    Steps:
    1. Validate user existence.
    2. Validate product existence and stock.
    3. Calculate prices and totals.
    4. Save order and order items in the database (transactional).
    5. Update product stock.
    6. Update user order history.
    """

    user_service_url = "http://user-service"
    product_service_url = "http://product-service"

    # Step 1: Validate user
    await validate_user(request.user_id, user_service_url)

    # Step 2: Validate products and stock, and fetch product data (including price)
    products = await validate_products_and_stock(request.items, product_service_url)
    product_map = {product["id"]: product for product in products}

    # Step 3: Calculate prices and totals
    order_items = []
    order_total = 0.0
    for item in request.items:
        product = product_map[item.product_id]
        price = product["price"]
        item_total = price * item.number
        order_total += item_total

        order_items.append({
            "product_id": item.product_id,
            "product_num": item.number,
            "price": price,
            "item_total": item_total,
        })

    # Step 4: Save order and items in the database (transactional)
    try:
        with db.begin_nested():  # Ensure atomicity with nested transactions
            order = models.Order(user_id=request.user_id, order_total=order_total)
            db.add(order)
            db.flush()  # Get the order ID without committing

            for item in order_items:
                order_item = models.OrderItem(
                    order_id=order.id,
                    product_id=item["product_id"],
                    product_num=item["product_num"],
                    price=item["price"],
                    item_total=item["item_total"]
                )
                db.add(order_item)

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save order: {str(e)}")

    # Step 5: Update product stock
    await update_product_stock(request.items, product_service_url)

    # Step 6: Update user order history
    await update_user_orders(request.user_id, order.id, user_service_url)

    return {"order_id": order.id, "message": "Order placed successfully"}
