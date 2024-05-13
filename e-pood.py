class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add(self, product: Product, amount: int):
        if product not in self.items:
            self.items[product] = amount
        else:
            self.items[product] += amount
    
    def remove(self, product: Product, amount: int):
        if product not in self.items:
            raise Exception(f"Can't remove item that hasn't been added yet: {product.name}")

        if self.items[product] > amount:
            self.items[product] -= amount
        elif self.items[product] == amount:
            self.items.pop(product)
        else:
            raise Exception(f"Not enough items in the cart to be removed: {self.items[product]} < {amount}")
    
    def empty(self):
        self.items = {}

    def products(self):
        product_list = []
        for product in self.items:
            product_list.append(product)
        return product_list

    @property
    def value(self):
        value = 0
        for product in self.items:
            value += product.price * self.items[product]
        return value
    
    @property
    def list_products(self):
        output = ""
        for product in self.items:
            output += f"{product.name}: {self.items[product]}\n"
        return output

class Client:
    def __init__(self, id: int, membership: None | str, money: float):
        self.id = id
        self.shopping_cart = ShoppingCart()
        self.membership = membership
        # Add discount to client if they have a gold membership
        self.discount = (membership == "gold") * 0.1
        self.history = []
        self.money = money

    def view_history(self) -> list:
        """ output = {}
        for date in self.history:
            print(date, self.history[date])
            output[date] = [product.name for product in self.history[date]]
        return output """
        output = {}
        for index in range(len(self.history)):
            items = self.history[index][0]
            date = self.history[index][1]

            items = [product.name for product in items]
            output[date] = items
        return output
    
    def view_history_verbal(self) -> str:
        output = ""
        for index in range(len(self.history)):
            items = self.history[index][0]
            date = self.history[index][1]
            item_text = ""
            for product in items:
                item_text += product.name + ", "
            item_text = item_text.rstrip(", ")
            output += f"On {date} you bought {item_text}.\n"
        output.rstrip("\n")
        return output


class Shop:
    def __init__(self):
        self.inventory = {}
        self.customers = []
    
    def add_to_cart(self, customer: Client, product: Product, amount):

        if product not in self.inventory:
            raise Exception("Product not in inventory")
        
        if self.inventory[product] < amount:
            raise Exception("Not enough items to add to cart")
        
        if product in self.inventory and self.inventory[product] >= amount:
            customer.shopping_cart.add(product, amount)

            # Reserve the item in the cusomer's shopping cart
            self.inventory[product] -= amount

    def remove_from_cart(self, customer: Client, product: Product, amount: int):
        customer.shopping_cart.remove(product, amount)

    def buy(self, customer: Client, date):
        if customer.shopping_cart.value - customer.shopping_cart.value * customer.discount <= customer.money:
            customer.history.insert(0, [customer.shopping_cart.products(), date]) # TODO: add date
            customer.money = customer.money - customer.shopping_cart.value * (1 - customer.discount)
            customer.shopping_cart.empty()
        else:
            assert Exception("Client has insufficient funds")

    def register_customer(self, customer: Client):
        self.customers.append(customer)

    def delete_customer(self, customer: Client):
        self.customers.remove(customer)

    def add_product(self, product: Product, amount: int):
        if product in self.inventory:
            self.inventory[product] += amount
        else:
            self.inventory[product] = amount


shop = Shop()

apple = Product("apple", 0.89)
banana = Product("banana", 0.99)
kiwi = Product("kiwi", 1.34)
milk = Product("milk", 1.00)

shop.add_product(apple, 100)
shop.add_product(banana, 298)
shop.add_product(kiwi, 437)
shop.add_product(milk, 28)

aadu = Client(0, None, 200)
beedu = Client(1, "gold", 100)
ceedu = Client(2, None, 50)
eedu = Client(3, None, 1000)

shop.register_customer(aadu)
shop.register_customer(beedu)
shop.register_customer(ceedu)
shop.register_customer(eedu)

# Aadu's shopping cart
shop.add_to_cart(aadu, apple, 5)
shop.add_to_cart(aadu, banana, 3)
shop.add_to_cart(aadu, kiwi, 10)
shop.add_to_cart(aadu, milk, 1)

# Beedu's shopping cart
shop.add_to_cart(beedu, milk, 12)

# Ceedu's shopping cart
shop.add_to_cart(ceedu, banana, 50)

# Eedu's shopping cart
shop.add_to_cart(eedu, kiwi, 400)
shop.add_to_cart(eedu, milk, 15)

date = "20.01"

shop.buy(aadu, date)
shop.buy(beedu, date)
shop.buy(ceedu, date)
shop.buy(eedu, date)

date = "21.01"
shop.add_to_cart(aadu, kiwi, 10)
shop.buy(aadu, date)

print("Aadu's history: ", aadu.view_history_verbal())
print("Beedu's history: ", beedu.view_history())
print("Ceedu's history: ", ceedu.view_history())
print("Eedu's history: ", eedu.view_history())




def test__create_product():
    apple = Product("Apple", 0.76)
    assert apple.name == "Apple" and apple.price == 0.76

def test__add_products_to_shopping_cart():
    apple = Product("Apple", 0.76)
    pineapple = Product("Pineapple", 2.15)

    shopping_cart = ShoppingCart()

    shopping_cart.add(apple, 10)
    shopping_cart.add(pineapple, 2)

    assert shopping_cart.items == {apple: 10, pineapple: 2}

def test__remove_products_from_shopping_cart():
    apple = Product("Apple", 0.76)
    banana = Product("Banana", 0.89)

    shopping_cart = ShoppingCart()

    shopping_cart.add(apple, 5)
    shopping_cart.add(banana, 10)

    shopping_cart.remove(apple, 3)
    shopping_cart.remove(banana, 1)

    assert shopping_cart.items == {apple: 2, banana: 9}

def test__create_client():
    bob = Client(1, None, 100)
    assert bob.id == 1
    assert bob.membership == None
    assert bob.money == 100

    james = Client(2, "Gold", 1000)
    assert james.id == 2
    assert james.membership == "Gold"
    assert james.money == 1000

def test__add_and_remove_products_from_clients_shopping_cart():

    bob = Client(29, None, 19)
    apple = Product("Apple", 1)
    pineapple = Product("Pineapple", 3)

    bob.add_to_cart(apple, 15)
    bob.add_to_cart(pineapple, 3)
    bob.remove_from_cart(apple, 5)

    shopping_cart = ShoppingCart()
    shopping_cart.add(apple, 10)
    shopping_cart.add(pineapple, 3)

    assert bob.shopping_cart.items == shopping_cart.items

def test__buy_products_normal_client_has_enough_money():
    ferdinand = Client(1273, None, 1410)
    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    ferdinand.add_to_cart(tv, 1)
    ferdinand.add_to_cart(hdmi_cable, 1)
    ferdinand.buy("05.12")

    money_left = 1410 - 1399 - 10.99

    assert round(ferdinand.money, 2) == round(money_left, 2)
    assert ferdinand.shopping_cart.items == {}

def test__buy_products_gold_client_has_enough_money():
    ferdinand = Client(9348, "gold", 10_000)
    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    ferdinand.add_to_cart(tv, 1)
    ferdinand.add_to_cart(hdmi_cable, 1)
    ferdinand.buy("10.04")
    money_left = 10000 - (tv.price + hdmi_cable.price) * 0.9

    assert round(ferdinand.money, 2) == round(money_left, 2)
    assert ferdinand.shopping_cart.items == {}

def test__buy_products_normal_client_not_enough_money():
    ferdinand = Client(345, "Gold", 100)
    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    ferdinand.add_to_cart(tv, 5)
    ferdinand.add_to_cart(hdmi_cable, 10)
    try:
        ferdinand.buy("20.08")
    except:
        pass
    else:
        assert "Client can't be in debt"

    assert ferdinand.money == 100
    assert ferdinand.shopping_cart.items == {tv: 5, hdmi_cable: 10}
