from epood import *

def test__create_product():
    apple = Product("Apple", 0.76)
    assert apple.name == "Apple" 
    assert apple.price == 0.76
    assert repr(apple) == "Apple"

def test__add_products_to_shopping_cart():
    apple = Product("Apple", 0.76)
    pineapple = Product("Pineapple", 2.15)

    shopping_cart = ShoppingCart()

    shopping_cart.add(apple, 10)
    shopping_cart.add(pineapple, 2)
    shopping_cart.add(apple, 2)

    assert shopping_cart.items == {apple: 12, pineapple: 2}

def test__remove_products_from_shopping_cart():
    apple = Product("Apple", 0.76)
    banana = Product("Banana", 0.89)
    pineapple = Product("Pineapple", 1.12)

    shopping_cart = ShoppingCart()

    shopping_cart.add(apple, 5)
    shopping_cart.add(banana, 10)

    shopping_cart.remove(apple, 3)
    shopping_cart.remove(banana, 1)

    item_wasnt_in_shopping_cart = False
    try:
        shopping_cart.remove(pineapple, 2)
    except:
        item_wasnt_in_shopping_cart = True

    assert shopping_cart.items == {apple: 2, banana: 9}
    assert item_wasnt_in_shopping_cart == True

def test__remove_too_many_items_from_shopping_cart():
    apple = Product("Apple", 0.76)
    banana = Product("Banana", 0.89)

    shopping_cart = ShoppingCart()

    shopping_cart.add(apple, 1)
    shopping_cart.add(banana, 2)

    assert shopping_cart.items == {apple: 1, banana: 2}

    shopping_cart.remove(apple, 1)

    assert shopping_cart.items == {banana: 2}


    not_enough_items_to_remove_in_shopping_cart = False
    try:
        shopping_cart.remove(banana, 3)
    except:
        not_enough_items_to_remove_in_shopping_cart = True

    assert shopping_cart.items == {banana: 2}
    assert not_enough_items_to_remove_in_shopping_cart == True

def test__create_client():
    bob = Client(1, False, 100)
    assert bob.id == 1
    assert repr(bob) == "1"
    assert bob.membership == False
    assert bob.money == 100

    james = Client(2, True, 1000)
    assert james.id == 2
    assert repr(james) == "2"
    assert james.membership == True
    assert james.money == 1000

def test__add_and_remove_products_from_shopping_cart_with_shop():

    shop = Shop()

    bob = Client(29, False, 19)

    apple = Product("Apple", 1)
    pineapple = Product("Pineapple", 3)

    shop.register_client(bob)
    shop.add_product(apple, 50)
    shop.add_product(pineapple, 10)
    assert shop.inventory == {apple: 50, pineapple: 10}

    shop.add_product(apple, 50)
    assert shop.inventory == {apple: 100, pineapple: 10}

    shop.add_to_cart(bob, apple, 15)
    shop.add_to_cart(bob, pineapple, 3)
    shop.remove_from_cart(bob, apple, 5)

    shopping_cart = ShoppingCart()
    shopping_cart.add(apple, 10)
    shopping_cart.add(pineapple, 3)

    assert bob.shopping_cart.items == shopping_cart.items
    assert shop.inventory == {apple: 90, pineapple: 7}

    james = Client(3, True, 453)

    client_has_not_registered_but_tried_to_remove_from_cart = False
    try:
        shop.remove_from_cart(james, apple, 1)
    except:
        client_has_not_registered_but_tried_to_remove_from_cart = True

    assert client_has_not_registered_but_tried_to_remove_from_cart


def test__buy_products_normal_client_has_enough_money_but_not_enough_items():

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

    not_enough_items_to_add_to_shopping_cart = False
    try:
        shop.add_to_cart(ferdinand, tv, 10)
    except:
        not_enough_items_to_add_to_shopping_cart = True

    assert not_enough_items_to_add_to_shopping_cart

    item_not_in_inventory = False
    try:
        shop.add_to_cart(ferdinand, Product("banana", 1.21), 10)
    except:
        item_not_in_inventory = True

    assert item_not_in_inventory

def test__buy_products_normal_client_not_enough_money_and_client_not_registered():
    shop = Shop()

    ferdinand = Client(345, True, 100)
    shop.register_client(ferdinand)

    tv = Product("TV", 1399)
    hdmi_cable = Product("HDMI cable", 10.99)

    shop.add_product(tv, 6)
    shop.add_product(hdmi_cable, 11)

    shop.add_to_cart(ferdinand, tv, 5)
    shop.add_to_cart(ferdinand, hdmi_cable, 10)

    client_has_insufficient_funds = False
    try:
        shop.buy(ferdinand, datetime.date(2020,8,20))
    except:
        client_has_insufficient_funds = True
    assert client_has_insufficient_funds

    assert ferdinand.money == 100
    assert ferdinand.shopping_cart.items == {tv: 5, hdmi_cable: 10}
    assert shop.inventory == {tv: 1, hdmi_cable: 1}

    james = Client(12, False, 342)
    client_not_registered_but_tried_buying = False
    try:
        shop.buy(james, datetime.date.today())
    except:
        client_not_registered_but_tried_buying = True
    
    assert client_not_registered_but_tried_buying

def test__add_and_remove_client_from_shop_database():
    shop = Shop()

    alfred = Client(832, False, 3274)
    berda = Client(4377, True, 237)
    hugo = Client(123, True, 123)

    client_not_registered_but_tried_to_add_to_cart = False
    try:
        shop.add_to_cart(hugo, Product("banana", 2), 2)
    except:
        client_not_registered_but_tried_to_add_to_cart = True

    assert client_not_registered_but_tried_to_add_to_cart

    shop.register_client(alfred)
    shop.register_client(berda)

    assert shop.clients == [alfred, berda] or [berda, alfred]

    shop.delete_client(alfred)

    assert shop.clients == [berda]

    shop.delete_client(berda)

    assert shop.clients == []

    william = Client(12, False, 2193)
    remove_client_but_client_is_not_in_shop_database = False
    try:
        shop.delete_client(william)
    except:
        remove_client_but_client_is_not_in_shop_database = True
    
    assert remove_client_but_client_is_not_in_shop_database

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
    
    assert client1.get_history_verbal() == 'On 2020-01-02, you bought: \n\t2x apple\n\t5x banana\nOn 2020-01-01, you bought: \n\t2x apple\n\t5x banana'
    
    assert client2.history == {datetime.date(2020, 1, 1): {apple: 1, banana: 4}, 
                               datetime.date(2020, 1, 2): {apple: 2, banana: 4}}
    
    assert client2.get_history_verbal() == "On 2020-01-02, you bought: \n\t2x apple\n\t4x banana\nOn 2020-01-01, you bought: \n\t1x apple\n\t4x banana"
    
    assert shop.get_history_descending_date() == {datetime.date(2020, 1, 1): 
                                                      {1: {apple: 2, banana: 5}, 
                                                       2: {apple: 1, banana: 4}}, 
                                                  datetime.date(2020, 1, 2): 
                                                      {1: {apple: 2, banana: 5}, 
                                                       2: {apple: 2, banana: 4}}} 