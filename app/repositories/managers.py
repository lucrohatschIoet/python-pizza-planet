from typing import Any, List, Optional, Sequence

from sqlalchemy.sql import text, column
from sqlalchemy import func, desc

from .models import Beverage, BeverageDetail, Ingredient, Order, OrderDetail, Size, db
from .serializers import (IngredientSerializer, OrderDetailSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((BeverageDetail(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()

class OrderDetailManager(BaseManager):
    model = OrderDetail

    @classmethod
    def get_most_requestd(cls):
        most_requested =  cls.session.query(
            func.count(cls.model.ingredient_id).label('count'), 
            Ingredient.name).join(Ingredient).group_by(
                cls.model.ingredient_id
                ).order_by(desc('count')).all()
        result = [{'name': ingredient.name, 'requested_times': ingredient.count} for ingredient in most_requested]

        return result


class BeverageDetailManager(BaseManager):
    model = BeverageDetail

    @classmethod
    def get_most_requestd(cls):
        most_requested =  cls.session.query(
            func.count(cls.model.beverage_id).label('count'), 
            Beverage.name).join(Beverage).group_by(
                cls.model.beverage_id
                ).order_by(desc('count')).all()
        result = [{'name': beverage.name, 'requested_times': beverage.count} 
                for beverage in most_requested]
        return result or []