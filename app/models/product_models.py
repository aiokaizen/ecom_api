from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import REAL, DateTime, Double, String, JSON, Integer
from typing import Any, Dict, List, Optional
from decimal import Decimal

from enums.enums import OrderTypeEnum
from faslava.config.configuration import settings
from faslava.models import BaseModel
from faslava.models.user_models import Address, BasePerson, UserAccount


class Product(BaseModel):
    """Primary Product table."""

    __tablename__ = "product"
    __display_name__ = "Product"

    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[Decimal] = mapped_column(REAL(precision=2))
    description: Mapped[Optional[str]] = mapped_column(default=None)
    custom_properties: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, default=None
    )
    tags: Mapped[Optional[List[str]]] = mapped_column(JSON, default=None)
    # categories: Mapped[List["Category"]] = relationship(
    #     secondary="CategoryProductAssociation",
    # )
    # categories: Mapped[List["CategoryProductAssociation"]] = relationship(back_populates="product_id")
    # orders: Mapped[List["Order"]] = relationship(secondary="OrderProductAssociation")
    sku: Mapped[Optional[str]] = mapped_column(String(16), default=None)
    brand: Mapped[Optional[str]] = mapped_column(String(64), default=None)
    manufacturer: Mapped[Optional[str]] = mapped_column(String(256), default=None)

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    __tablename__ = "category"
    __display_name__ = "Category"

    name: Mapped[str] = mapped_column(String(256))
    # products: Mapped[List[Product]] = relationship(
    #     secondary="CategoryProductAssociation"
    # )
    # products: Mapped[List["CategoryProductAssociation"]] = relationship(back_populates="category_id")

    def __str__(self) -> str:
        return self.name


class CategoryProductAssociation(BaseModel):
    __tablename__ = "category_product_association"

    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text("CURRENT_TIMESTAMP")
    )


class Tag(BaseModel):
    __tablename__ = "tag"
    __display_name__ = "Tag"

    name: Mapped[str] = mapped_column(String(256), unique=True)


# class CustomerAddress(Address):
#     __tablename__ = "address"
#     __display_name__ = "Address"
#     __mapper_args__ = {
#         "polymorphic_identity": "customer_address",
#         "inherit_condition": (
#             Address.id == mapped_column(Integer, ForeignKey("address.id")),
#         ),  # Explicit inheritance condition
#     }
#     __table_args__ = {
#         "extend_existing": True,
#     }
#
#     customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
#     customer: Mapped["Customer"] = relationship(back_populates="orders")


class Customer(BaseModel):
    __tablename__ = "customer"
    __display_name__ = "Customer"

    user_id: Mapped[int] = mapped_column(ForeignKey(UserAccount.id))
    user: Mapped[UserAccount] = relationship()
    orders: Mapped[List["Order"]] = relationship(back_populates="customer")
    # addresses: Mapped[List[CustomerAddress]] = relationship(back_populates="customer")


class Order(BaseModel):
    __tablename__ = "order"
    __display_name__ = "Order"

    currency: Mapped[str] = mapped_column(String(3), default="USD")
    order_type: Mapped[OrderTypeEnum] = mapped_column(
        String(256), default=OrderTypeEnum.ORDER
    )
    order_date: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now())
    # products: Mapped[List[Product]] = relationship(secondary="OrderProductAssociation")
    total_price: Mapped[Decimal] = mapped_column(Double(precision=2))
    discount: Mapped[Decimal] = mapped_column(Double(precision=2), default=0)
    tax: Mapped[Decimal] = mapped_column(Double(precision=2), default=0)
    total_quantity: Mapped[Decimal] = mapped_column(Double(precision=2))
    products_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    customer_id: Mapped[int] = mapped_column(ForeignKey(Customer.id))
    trigger_event: Mapped[Optional[Dict]] = mapped_column(
        JSON(none_as_null=True), default=None
    )

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="orders")


class OrderProductAssociation(BaseModel):
    __tablename__ = "order_product_association"

    product_id: Mapped[int] = mapped_column(ForeignKey(Product.id), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey(Order.id), primary_key=True)
    sell_price: Mapped[Decimal] = mapped_column(Double(precision=2))
    discount: Mapped[Optional[Decimal]] = mapped_column(
        Double(precision=2), default=None
    )
    tax: Mapped[Optional[Decimal]] = mapped_column(Double(precision=2), default=None)
