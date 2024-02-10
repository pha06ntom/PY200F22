import re
import random
from typing import Union

DATA_BASE = [{"password": "12345abc"}]  # База данных


class idCounter:
    """ Класс, в котором хранится значение id """
    id_count = 0

    def __init__(self):
        idCounter.id_count += 1


class Password:
    """ Класс, который проверяет корректность пароля пользователя """

    def check(self, password: str):
        if not isinstance(password, str):  # Проверка типа переданного значения
            raise TypeError(" The password must be of string type ")

        if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}',
                        password) is None:  # Проверка на соответсвие минимальным правилам: -длина не менее 8 символов; - в пароле есть как цифры, так и буквы
            raise ValueError("Password has incorrect format")

        # Проверяется соотносится ли передаваемый пароль с его значением в базе
        for data in DATA_BASE:
            if password == data["password"]:
                print("Сorrect password")
            else:
                print("Incorrect password")


class Product:
    """ Класс, который хранит информацию о продукте """

    def __init__(self, name: str, price: Union[int, float], rating: Union[int, float]):
        self.__set_name(name)
        self._price = price
        self._rating = rating

        id = idCounter()
        self._id = id.id_count

    # Атрибут 'name' не может изменяться из вне
    def get_name(self):
        return self.__name

    def __set_name(self, name_value: str):
        if not isinstance(name_value, str):
            raise TypeError()
        self.__name = name_value

    # Атрибут 'id' не может изменяться из вне
    def __get_id(self):
        return self.__id

    def __set_id(self, value: str):
        self.__id = value

    def is_valid(self, value):
        """ Метод для проверки корректности значения """
        if not isinstance(value, (int, float)):
            raise TypeError("The value must be of type int or float")
        if value <= 0:
            raise ValueError("The value must be a positive number")

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price_value):
        self.is_valid(price_value)
        self.__price = price_value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, rating_value):
        self.is_valid(rating_value)
        self.__rating = rating_value

    def __str__(self) -> str:
        return f'{self._id}_{self.__name}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.__name}, price={self._price}, rating={self._rating})' #Product(name, price, rating)


class Cart:
    """ Класс, в котором хранится информаци о списке товаров """
    cart_products = []  # Список товаров в корзине

    def add(self, add_product: Product):
        """ Метод для добавления товара в корзину """
        Cart.cart_products.append(add_product)

    def remove(self, name_product: str) -> bool:
        """ Метод для удаления товара из корзины """
        for v in Cart.cart_products:
            if v.get_name() == name_product:
                Cart.cart_products.remove(v)
                return True
        return False


class User(Password):
    """ Класс, в котором хранится информация о пользователе """

    def __init__(self, username: str, password: str):
        self.__set_username(username)
        self.__set_password(password)

        id_user = idCounter()
        self._id_user = id_user.id_count

    # Атрибут 'username' не может изменяться из вне, задается только при инициализации
    def __get_username(self):
        return self.__username

    def __set_username(self, user_value):
        if not isinstance(user_value, str):
            raise TypeError()
        self.__username = user_value

    # Создание корзины пользователя
    def get_cart_user(self):
        cart_user = Cart()
        return cart_user.cart_products

    # Атрибут пораля хранится в хэш-значении и закрыт.
    def __set_password(self, value: str):
        self.__password = hash(super().check(value))

    def __str__(self) -> str:
        return f'{self._id_user}_{self.__username}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id: {self._id_user}, username: {self.__username}, password: \'password1\')'


# Магазин обуви

def create_product():
    """ Функция генерирует случайный товар """
    list_shoes = ['Ботинки', 'Сапоги', 'Туфли', 'Босоножки', 'Кроссовки', 'Кеды', 'Мокасины', 'Слипоны', 'Тапочки',
                  'Лоферы']
    random_shoes = random.choice(list_shoes)

    price_shoes = round(random.uniform(1200, 3500), 2)
    rating_shoes = round(random.uniform(0, 5), 2)

    return Product(name=random_shoes, price=price_shoes, rating=rating_shoes)


class Store(Cart):
    def __init__(self):
        self.authentication()

    def authentication(self):
        """ Метод аутентификации пользователя через консоль"""
        login_user = input("Enter the login: ")
        password_user = input("Enter the password: ")
        self.user = User(login_user, password_user)

    def add_product(self):
        """ Метод добавлени случайного продукта в корзину ппользователя"""
        product = create_product()
        super().add(product)

    def remove_product(self, product):
        """ Метод удаления продукта из корзины пользователя """
        result = super().remove(product)
        if not result:
            print("There product was not found in the shopping cart")

    def view_cart(self):
        """ Метод для просмотра продуктов в корзине пользователя """
        print("List of products in the shopping cart")
        if super().cart_products is not None:
            #print(super().cart_products)
            print(self.user.get_cart_user())
        else:
            print('Your shopping cart is currently empty')

if __name__ == '__main__':
    s = Store()
    s.add_product()
    s.add_product()
    s.add_product()
    s.view_cart()
    prod = input('Введите имя продукта. который нужно удалить из корзины: ')
    s.remove_product(prod)
    s.view_cart()
