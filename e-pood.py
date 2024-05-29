import datetime

class Product:
    def __init__(self, name: str, price: float) -> None:
        """
        Initialize the product.
 
        :param name: Product's name.
        :param price: Product's price.
        """
        self.name = name
        self.price = price

    def __repr__(self) -> repr:
        """
        Product's representor.

        :return: product's name.
        """

        return self.name

class ShoppingCart:
    def __init__(self) -> None:
        """
        Initialize the shopping cart.
        """
        self.items = {}

    def add(self, product: Product, amount: int) -> None:
        """
        Add product to shopping cart.

        :param product: Product that will be added to the shopping cart.
        :param amount: Amount of specified product that will be added to the shopping cart.
        """
        if product not in self.items:
            self.items[product] = amount
        else:
            self.items[product] += amount
    
    def remove(self, product: Product, amount: int) -> None:
        """
        Remove the specified amount of products from the shopping cart.

        :param product: Product that will be removed from the shopping cart.
        :param amount: Amount of specified product taht will be removed from the shopping cart.
        """
        if product not in self.items:
            raise Exception("Can't remove item that hasn't been added yet.")

        if self.items[product] > amount:
            self.items[product] -= amount
        elif self.items[product] == amount:
            self.items.pop(product)
        else:
            raise Exception("Not enough items in the cart to be removed.")
    
    def empty(self) -> None:
        """
        Remove all products from the shopping cart.
        """
        self.items = {}

    @property
    def value(self) -> float:
        """
        Calculate the shopping cart's value.

        :return: Value of the shopping cart.
        """

        value = 0
        for product in self.items:
            value += product.price * self.items[product]
        return value
    
    def get_products_verbal(self) -> str:
        """
        Return a readable list of products in the shopping cart.

        :return: A string of products and their respecitve amounts.
        """
        output = ""
        for product in self.items:
            output += f"{product.name}: {self.items[product]}\n"
        return output

class Client:
    def __init__(self, id: int, membership: bool, money: float) -> None:
        """
        Initialize the client.

        :param id: The unique id of the client
        :param membership: If client has a gold membership, then they will get a discount of 10%
        :param money: How much money the client has
        """
        self.id = id
        self.shopping_cart = ShoppingCart()
        self.membership = membership
        # Add discount to client if they have a gold membership
        self.discount = membership * 0.1
        self.history = {}
        self.money = money

    def __repr__(self) -> repr:
        """
        Representor of client.

        :return: client's id.
        """
        return self.id
    
    def get_history_verbal(self) -> str:
        """
        History in human readable way.
        
        :return: A string that has readable formatting for viewing client's history.
        """
        history = dict(reversed(list(self.history.items())))
        output = ""
        for date in history:
            output += f"On {date}, you bought: \n"
            for product in history[date]:
                output += f"\t{history[date][product]}x {product}\n"
        output.rstrip("\n")
        return output

class Shop:
    def __init__(self) -> None:
        """Create an e-shop class that will handle purchases and history."""
        self.inventory = {}
        self.clients = []
        self.history = {}
    
    def add_to_cart(self, client: Client, product: Product, amount) -> None:
        """
        Add specified amount of product to client's cart.

        :param client: the client object to whose cart an item will be added.
        :param product: the product object that will be added to cart.
        :param amount: the amount of product that is added to the client's cart
        """

        if client not in self.clients:
            print("Client has not registered")
            return

        if product not in self.inventory:
            raise Exception("Product not in inventory")
        
        if self.inventory[product] < amount:
            raise Exception("Not enough items to add to cart")
        
        if product in self.inventory and self.inventory[product] >= amount:
            client.shopping_cart.add(product, amount)

            # Reserve the item in the cusomer's shopping cart
            self.inventory[product] -= amount

    def remove_from_cart(self, client: Client, product: Product, amount: int) -> None:
        """
        Remove specified amount of items from client's shopping cart.

        :param client: the client object from whose cart items will be removed.
        :param product: the product object that will be removed from cart.
        :param amount: the amount of products that are removed from the client's cart.
        """

        if client not in self.clients:
            print("Client has not registered")
            return

        client.shopping_cart.remove(product, amount)

    def buy(self, client: Client, date: datetime.date) -> None:
        """
        Go through the process of buying the items in client's shopping cart.

        :param client: The client that is performing the purchase.
        :param date: date when the purcahse was made.
        """
        if client not in self.clients:
            print("Client has not registered")
            return

        # If client deosn't have enough money
        if client.shopping_cart.value - client.shopping_cart.value * client.discount > client.money:
            print("Client has insufficient funds")
            return

        # Add the current shopping cart to client's history as {date: {product: amount, ...}, ...}
        if date in client.history:
            for product in client.shopping_cart.items:
                if product in client.history[date]:
                    client.history[date][product] += client.shopping_cart.items[product]
                else:
                    client.history[date][product] = client.shopping_cart.items[product]
        # First time that day buying
        else:
            client.history[date] = client.shopping_cart.items

        client.money = client.money - client.shopping_cart.value * (1 - client.discount)

        
        if date in self.history:
            if client.id in self.history[date]:
                for product in client.shopping_cart.items:
                    if product in self.history[date][client.id]:
                        self.history[date][client.id][product] += client.shopping_cart.items[product]  
                    else:
                        self.history[date][client.id][product] = client.shopping_cart.items[product]
            else:
                # First time to buy for the client to buy on that day
                self.history[date][client.id] = client.shopping_cart.items
        # First purchase of the day
        else:
            self.history[date] = {client.id: client.shopping_cart.items.copy()}

        client.shopping_cart.empty()
            
    def register_client(self, new_client: Client) -> None:
        """
        Add client to the e-shop's database.

        :param new_client: The client that is going to be registered
        """
        for client in self.clients:
            if client.id == new_client.id:
                print("client with that id already exists")
                return
        self.clients.append(new_client)

    def delete_client(self, client: Client) -> None:
        """
        Remove client from e-shop's database.

        :param client: The client that is going to be removed
        """
        for temp_client in self.clients:
            if temp_client == client:
                for product in client.shopping_cart.items:
                    self.add_product(product, client.shopping_cart.items[product])
                self.clients.remove(client)
        else:
            print("client does not exist, thus can't remove client from e-shop")

    def add_product(self, product: Product, amount: int) -> None:
        """
        Add secified amount of product to the e-shop's inventory.

        :param product: Product that will be added to teh e-shop's inventory.
        :param amount: The amount of specified product that will be asses to the inventory.
        """
        if product in self.inventory:
            self.inventory[product] += amount
        else:
            self.inventory[product] = amount
    
    def get_history_descending_date(self) -> dict:
        """
        Reverse the history to make the dates descending

        :return: History dictionary, that is reversed (I trust that there is no time traveling going on) 
        """
        return dict(reversed(list(self.history.items())))
    
    def get_history_verbal(self) -> str:
        history = self.get_history_descending_date()
        output = ""
        for date in history:
            output += f"On {date}, these purchases were made:\n"
            for x, client in enumerate(history[date]):
                last_client = len(history[date]) - x == 1
                if last_client:
                    output += f"└id: {client}\n"
                else:
                    output += f"├id: {client}\n"
                
                for y, product in enumerate(history[date][client]):
                    last_product = len(history[date][client]) - y == 1
                    if last_client:
                        if last_product:
                            output += f" └{history[date][client][product]}x {product}\n"
                        else:
                            output += f" ├{history[date][client][product]}x {product}\n"
                    else:
                        if last_product:
                            output += f"│└{history[date][client][product]}x {product}\n"
                        else:
                            output += f"│├{history[date][client][product]}x {product}\n"

        output.rstrip("\n")

        return output
    


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
    bob = Client(1, False, 100)
    assert bob.id == 1
    assert bob.membership == False
    assert bob.money == 100

    james = Client(2, True, 1000)
    assert james.id == 2
    assert james.membership == True
    assert james.money == 1000

def test__add_and_remove_products_from_shopping_cart_with_shop():

    shop = Shop()

    bob = Client(29, False, 19)
    apple = Product("Apple", 1)
    pineapple = Product("Pineapple", 3)

    shop.register_client(bob)
    shop.add_product(apple, 100)
    shop.add_product(pineapple, 10)

    shop.add_to_cart(bob, apple, 15)
    shop.add_to_cart(bob, pineapple, 3)
    shop.remove_from_cart(bob, apple, 5)

    shopping_cart = ShoppingCart()
    shopping_cart.add(apple, 10)
    shopping_cart.add(pineapple, 3)

    assert bob.shopping_cart.items == shopping_cart.items
    assert shop.inventory == {apple: 85, pineapple: 7}

def test__buy_products_normal_client_has_enough_money():

    shop = Shop()

    ferdinand = Client(1273, False, 1410)
    shop.register_client(ferdinand)

    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    shop.add_product(tv, 10)
    shop.add_product(hdmi_cable, 15)

    shop.add_to_cart(ferdinand, tv, 1)
    shop.add_to_cart(ferdinand, hdmi_cable, 1)
    shop.buy(ferdinand, datetime.date(2009,5,12))

    money_left = 1410 - tv.price - hdmi_cable.price

    assert round(ferdinand.money, 2) == round(money_left, 2)
    assert ferdinand.shopping_cart.items == {}

def test__buy_products_normal_client_not_enough_money():
    shop = Shop()

    ferdinand = Client(345, True, 100)
    shop.register_client(ferdinand)

    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    shop.add_product(tv, 6)
    shop.add_product(hdmi_cable, 11)

    shop.add_to_cart(ferdinand, tv, 5)
    shop.add_to_cart(ferdinand, hdmi_cable, 10)

    # Should PRINT an error
    shop.buy(ferdinand, datetime.date(2020,8,20))


    assert ferdinand.money == 100
    assert ferdinand.shopping_cart.items == {tv: 5, hdmi_cable: 10}
    assert shop.inventory == {tv: 1, hdmi_cable: 1}

def test__add_and_remove_client_from_shop_database():
    shop = Shop()

    alfred = Client(832, False, 3274)
    berda = Client(4377, True, 237)

    shop.register_client(alfred)
    shop.register_client(berda)

    assert shop.clients == [alfred, berda] or [berda, alfred]

    shop.delete_client(alfred)

    assert shop.clients == [berda]

    shop.delete_client(berda)

    assert shop.clients == []

def test__shop_add_clients_with_same_id():
    shop = Shop()

    james = Client(12, True, 3274)
    fred = Client(12, True, 943)

    shop.register_client(james)
    shop.register_client(fred)

    assert shop.clients == [james]

    fred.id = 13

    shop.register_client(fred)
    shop.delete_client(james)

    assert shop.clients == [fred]
    
def test__shop_history_and_client_history_multiple_days():
    shop = Shop()

    apple = Product("apple", 1)
    banana = Product("banana", 1)

    client1 = Client(1, False, 10000)
    client2 = Client(2, False, 10000)

    shop.register_client(client1)
    shop.register_client(client2)

    shop.add_product(apple, 100)
    shop.add_product(banana, 100)

    year = 2020
    month = 1
    for day in range(1,3):
        shop.add_to_cart(client1, apple, 1)

        shop.add_to_cart(client2, apple, day)
        shop.add_to_cart(client2, banana, 2)

        shop.buy(client1, datetime.date(year, month, day))
        shop.buy(client2, datetime.date(year, month, day))

        shop.add_to_cart(client1, apple, 1)
        shop.add_to_cart(client1, banana, 5)

        shop.add_to_cart(client2, banana, 1)
        
        
        shop.buy(client1, datetime.date(year, month, day))
        shop.buy(client2, datetime.date(year, month, day))

    assert client1.history == {datetime.date(2020, 1, 1): {apple: 2, banana: 5}, 
                               datetime.date(2020, 1, 2): {apple: 2, banana: 5}}
    
    assert client2.history == {datetime.date(2020, 1, 1): {apple: 1, banana: 4}, 
                               datetime.date(2020, 1, 2): {apple: 2, banana: 4}}
    
    assert shop.get_history_descending_date() == {datetime.date(2020, 1, 1): 
                                                      {1: {apple: 2, banana: 5}, 
                                                       2: {apple: 1, banana: 4}}, 
                                                  datetime.date(2020, 1, 2): 
                                                      {1: {apple: 2, banana: 5}, 
                                                       2: {apple: 2, banana: 4}}} 
    

# Not a test
def tree_shop_history():
    shop = Shop()

    client1 = Client(1,0,1000)
    client2 = Client(2,0,1000)

    shop.register_client(client1)
    shop.register_client(client2)

    banana = Product("banana", 1)
    apple = Product("apple", 0.5)

    shop.add_product(banana, 10)
    shop.add_product(apple, 10)


    shop.add_to_cart(client1, banana, 2)
    shop.add_to_cart(client1, apple, 4)

    shop.add_to_cart(client2, apple, 1)
    shop.add_to_cart(client2, banana, 1)

    shop.buy(client1, datetime.date(2024,5,19))
    shop.buy(client2, datetime.date(2024,5,19))

    shop.add_to_cart(client1, banana, 4)
    shop.add_to_cart(client1, apple, 2)

    shop.add_to_cart(client2, apple, 1)
    shop.add_to_cart(client2, banana, 1)

    shop.buy(client1, datetime.date.today())
    shop.buy(client2, datetime.date.today())

    print(client1.get_history_verbal())

    print(shop.get_history_verbal())

# Non-compatible test (old)
""" def __test__shop_buy_and_add_items_different_dates_check_history():
    shop = Shop()

    apple = Product("apple", 0.89)
    banana = Product("banana", 0.99)
    kiwi = Product("kiwi", 1.34)
    milk = Product("milk", 1.00)

    shop.add_product(apple, 100)
    shop.add_product(banana, 298)
    shop.add_product(kiwi, 437)
    shop.add_product(milk, 28)

    aadu = Client(0, False, 200)
    beedu = Client(1, True, 100)
    ceedu = Client(2, False, 50)
    eedu = Client(3, False, 1000)

    shop.register_client(aadu)
    shop.register_client(beedu)
    shop.register_client(ceedu)
    shop.register_client(eedu)

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

    date = datetime.date(2022, 1, 20)

    shop.buy(aadu, date)
    shop.buy(beedu, date)
    shop.buy(ceedu, date)
    shop.buy(eedu, date)

    assert shop.inventory == {apple: 95, banana: 245, kiwi: 27, milk: 0}

    date = datetime.date(2022, 1, 21)
    shop.add_product(milk, 100)
    shop.add_product(kiwi, 150)
    shop.add_to_cart(aadu, milk, 10)
    shop.buy(aadu, date)

    assert shop.inventory == {apple: 95, banana: 245, kiwi: 177, milk: 90}

    date = datetime.date(2023,12,24)
    shop.add_product(apple, 100)
    shop.add_to_cart(beedu, banana,  10)
    shop.add_to_cart(beedu, kiwi, 10)
    shop.add_to_cart(beedu, apple, 46)
    shop.buy(beedu, date)

    assert shop.inventory == {apple: 149, banana: 235, kiwi: 167, milk: 90}

    # Doesn't have enough money
    date = datetime.date(2024,1,1)
    shop.add_to_cart(ceedu, milk, 2)
    shop.buy(ceedu, date)

    shopping_cart = ShoppingCart()
    shopping_cart.add(milk, 2)

    assert ceedu.shopping_cart.items == shopping_cart.items


    assert aadu.view_history() == {datetime.date(2022, 1, 21): [milk], datetime.date(2022, 1, 20): [apple, banana, kiwi, milk]}
    assert beedu.view_history() == {datetime.date(2023, 12, 24): [banana, kiwi, apple], datetime.date(2022, 1, 20): [milk]}
    assert ceedu.view_history() == {datetime.date(2022, 1, 20): [banana]}
    assert eedu.view_history() == {datetime.date(2022, 1, 20): [kiwi, milk]}

    assert shop.history == {datetime.date(2022, 1, 20): 
                                {0: [apple, banana, kiwi, milk],    # aadu
                                 1: [milk],                         # beedu
                                 2: [banana],                       # ceedu
                                 3: [kiwi, milk]},                  # eedu

                            datetime.date(2022, 1, 21): 
                                {0: [milk]},                        # aadu

                            datetime.date(2023, 12, 24): 
                                {1: [banana, kiwi, apple]}}         # beedu """