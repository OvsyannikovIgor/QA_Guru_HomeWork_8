"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture()
def empty_cart():
    return Cart()


@pytest.fixture()
def cart_with_product(product):
    cart = Cart()
    cart.add_product(product, 5)
    return cart, product


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert not product.check_quantity(1500), "Некорректный расчет когда запрашиваемое значение больше"
        assert product.check_quantity(100), "Некорректный запрос когда запрашиваемое значение меньше"
        assert product.check_quantity(product.quantity), "Некорректный запрос когда запрашиваемое " \
                                                         "значение равно количеству"

    def test_product_buy(self, product):
        #  напишите проверки на метод buy
        product.buy(100)
        assert product.quantity == 900

    def test_product_buy_more_than_available(self, product):
        #  напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1500)


class TestCart:
    """
    Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, empty_cart, product):
        empty_cart.add_product(product=product)
        assert empty_cart.products[product] == 1

    def test_remove_one_product(self, cart_with_product):
        cart, product = cart_with_product
        cart.remove_product(product, 1)
        assert cart.products[product] == 4

    def test_remove_all_products(self, cart_with_product):
        cart, product = cart_with_product
        cart.add_product(product, 20)
        cart.remove_product(product, 25)
        assert cart.products.get(product, 0) == 0

    def test_clear(self, cart_with_product):
        cart, product = cart_with_product
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart_with_product):
        cart, product = cart_with_product
        price = cart.get_total_price()
        assert price == 500

    def test_buy(self, cart_with_product):
        cart, product = cart_with_product
        cart.buy()
        assert len(cart.products) == 0
        assert product.quantity == 995

    def test_deficit_products(self, cart_with_product):
        cart, product = cart_with_product
        cart.add_product(product, 1000)
        with pytest.raises(ValueError):
            cart.buy()
