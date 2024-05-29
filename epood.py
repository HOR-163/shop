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
        self.inventory[product] += amount

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