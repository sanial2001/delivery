from fastapi import APIRouter, status, HTTPException, Depends, Response
from .. import schemas, oauth2, models
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.get("/")
def hello():
    return {"hello": "world"}


@router.post("/order", status_code=status.HTTP_201_CREATED)
def place_order(order_details: schemas.Order, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)):
    # print(user_id.id)
    new_order = models.Order(
        quantity=order_details.quantity,
        pizza_size=order_details.pizza_size
    )
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    new_order.user = user
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/all_orders", status_code=status.HTTP_200_OK)
def get_all_orders(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_staff:
        orders = db.query(models.Order).all()
        return orders
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized as not super user")


@router.get("/order/{id}", status_code=status.HTTP_200_OK)
def get_order_by_id(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_staff:
        order = db.query(models.Order).filter(models.Order.id == id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"order with id : {id} was not found")
        return order
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized as not super user")


@router.get("/user_orders", status_code=status.HTTP_200_OK)
def get_users_orders(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user_orders = db.query(models.Order).filter(models.Order.user_id == user_id.id).all()
    if not user_orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order found for user")
    return user_orders


@router.get("/user_order/{id}", status_code=status.HTTP_200_OK)
def user_specific_order(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    user_orders = user.order
    for order in user_orders:
        if order.id == id:
            return order
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"No order with the given id")


@router.put("/update/{id}", status_code=status.HTTP_200_OK)
def update_order(id: int, updated_order: schemas.Order, db: Session = Depends(get_db),
                 user_id: int = Depends(oauth2.get_current_user)):
    order_to_update = db.query(models.Order).filter(models.Order.id == id).first()
    if not order_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"order {id} not found")
    if int(order_to_update.user_id) != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    order_to_update.quantity = updated_order.quantity
    order_to_update.pizza_size = updated_order.pizza_size
    db.commit()
    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "order_status": order_to_update.order_status,
        "pizza_size": order_to_update.pizza_size
    }
    return response


@router.patch("/update_status/{id}", status_code=status.HTTP_200_OK)
def update_status(id: int, updated_status: schemas.UpdateStatus, db: Session = Depends(get_db),
                  user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id.id).first()
    if user.is_staff:
        order_to_update = db.query(models.Order).filter(models.Order.id == id).first()
        if not order_to_update:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with id : {id} not found")
        order_to_update.order_status = updated_status.order_status
        db.commit()
        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "order_status": order_to_update.order_status,
            "pizza_size": order_to_update.pizza_size
        }
        return response
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not super user")


@router.delete("/delete_order/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    order_to_delete = db.query(models.Order).filter(models.Order.id == id).first()
    if not order_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order : {id} not found")
    if int(order_to_delete.user_id) != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized")
    db.delete(order_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
