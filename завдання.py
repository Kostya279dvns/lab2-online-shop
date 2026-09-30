from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    NEW = "Нове"
    PAID = "Оплачене"
    SHIPPED = "Відправлене"
    CANCELLED = "Скасоване"


@dataclass
class Customer:
    username: str
    email: str
    city: str


class Product:
    def __init__(self, name: str, price: float, stock: int):
        self.name = name
        self.price = price
        self.stock = stock

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or len(value.strip()) < 3:
            raise ValueError("Назва товару має містити щонайменше 3 символи!")
        self._name = value.strip()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Ціна товару має бути числом!")
        if not 0 < value <= 1_000_000:
            raise ValueError("Ціна товару має бути в межах від 0 (не включно) до 1 000 000 грн!")
        self._price = float(value)

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, value: int):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Кількість на складі має бути цілим числом!")
        if value < 0:
            raise ValueError("Кількість на складі не може бути від'ємною!")
        self._stock = value


class Order:
    MAX_QUANTITY = 10

    def __init__(self, customer: Customer, product: Product, quantity: int):
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.status = OrderStatus.NEW
        self.created_at = datetime.now()

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Кількість у замовленні має бути цілим числом!")
        if not 1 <= value <= self.MAX_QUANTITY:
            raise ValueError(f"Кількість у замовленні має бути від 1 до {self.MAX_QUANTITY}!")
        if value > self.product.stock:
            raise ValueError(f"Недостатньо товару на складі (доступно: {self.product.stock})!")
        self._quantity = value

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, value: OrderStatus):
        if not isinstance(value, OrderStatus):
            raise ValueError("Статус має бути елементом OrderStatus!")
        self._status = value

    @property
    def total(self) -> float:
        return self.product.price * self._quantity


if __name__ == "__main__":
    print("--- Інтернет-магазин: система управління замовленнями ---")

    customer = Customer(username="Anna", email="anna@example.com", city="Vinnytsia")

    try:
        print(f"\nПокупець: {customer.username} ({customer.city})")

        name = input("Введіть назву товару: ")
        price = float(input("Введіть ціну товару (грн): "))
        stock = int(input("Введіть кількість на складі: "))
        quantity = int(input("Введіть кількість у замовленні: "))

        product = Product(name, price, stock)
        order = Order(customer, product, quantity)

        print("\n[УСПІХ] Замовлення успішно створено:")
        print(f"Товар: {product.name}")
        print(f"Кількість: {order.quantity}")
        print(f"Сума: {order.total:.2f} грн")
        print(f"Статус: {order.status.value}")
        print(f"Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

        print("\n--- Інспекція внутрішнього стану (vars) ---")
        print(vars(product))
        print(vars(order))

    except ValueError as e:
        print(f"\n[ПОМИЛКА ВАЛІДАЦІЇ] {e}")
    except Exception as e:
        print(f"\n[ПОМИЛКА] Виникла непередбачувана ситуація: {e}")