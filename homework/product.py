class Product:
    __name: str
    __code: int
    __kolvo: int
    __price: float

    def __init__(self, name: str, code: int, kolvo: int, price: float):
        self.__name = name
        self.__code = code
        self.__kolvo = kolvo
        self.__price = price

    def get_name(self):
        return self.__name
    
    def get_code(self):
        return self.__code

    def get_kolvo(self):
        return self.__kolvo

    def get_price(self):
        return self.__price


    # def set_name(self, name: str):
    #     self.__name = name

    # def set_code(self, code: int):
    #     self.__code = code

    # def set_kolvo(self, kolvo: int):
    #     self.__kolvo = kolvo

    # def set_price(self, price: int):
    #     self.__price = price



    def update_quantity(self, amount: int):
        self.__kolvo += amount

    def update_price(self, price: float):
        self.__price = price

class Warehouse:
    __products: list

    def __init__(self):
        self.__products = []

    def add_product(self, product: Product):
        self.__products.append(product)

    def get_product_by_code(self, code: int):
        for product in self.__products:
            if product.get_code() == code:
                return product
        return None
    def remove_product_by_code(self, code: int):
        for product in self.__products:
            if product.get_code() == code:
                self.__products.remove(product)
                return True
        return False
    
    def print_all_products(self):
        for product in self.__products:
            print(f"Название: {product.get_name()}, Код: {product.get_code()}, Кол-во: {product.get_kolvo()}, Цена: {product.get_price()}")