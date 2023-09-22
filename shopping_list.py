#!/usr/bin/python3
import os
import jsonpickle

#Exception for item not found error
class ItemNotFoundError(Exception):
    pass

#main class for managing the shopping lists
class ShoppingList:
    def __init__(self, name):
        self.name = name
        self.items = {}

    #add item to shopping list
    def add_item(self, item, amount, price=0):
        #add item, if it exists ask user if they want to update the amount
        if item not in self.items:
            self.items[item] = {'amount': amount, 'price': price}
            print(f"{item} added\n")
        else:
            update_choice = str(input("Item is already in the list, do you want to update the amount? (y/n): "))
            if update_choice.lower() == "y":
                self.alter_item_amount(item, amount)
            elif update_choice.lower() == "n":
                print("Nothing updated\n")
            else:
                print("Please enter 'y' or 'n'\n")

    #remove item from shopping list
    def remove_item(self, item):
        if item in self.items:
            del self.items[item]
            print(f"{item} removed\n")
        else:
            raise ItemNotFoundError(f"\nItem '{item}' is not in the list\n")

    #change the amount of an item
    def alter_item_amount(self, item, amount):
        if item in self.items:
            self.items[item]['amount'] = amount
            print(f"{item} updated to {amount}\n")
        else:
            raise ItemNotFoundError(f"\nItem '{item}' is not in the list\n")

    #change the price of an item
    def alter_item_price(self, item, price):
        if item in self.items:
            self.items[item]['price'] = price * self.items[item]['amount']
        else:
            raise ItemNotFoundError(f"\nItem '{item}' is not in the list\n")

    #print out list name and items within including amounts and prices
    def view_items_in_list(self):
        total = 0
        items_with_price = 0
        items_without_price = 0
        shopping_list = f"\nShopping List: {self.name}\n"
        for item, details in self.items.items():
            amount = details["amount"]
            price = details["price"]
            shopping_list += f"    {item}: amount: {amount}, price: ${price}\n"
            #calculate total price if item was given a price by the user
            if price > 0:
                total += amount * price
                items_with_price += 1
            if price == 0:
                items_without_price += 1
        shopping_list += f"\nTotal: ${total} from {items_with_price} items given a price and {items_without_price} items with no price\n"
        return shopping_list

#save shopping lists to json file to load on next script run
def save_shopping_list_to_json_file(dict_of_shopping_lists, shopping_list_name, shopping_list):
    while True:
        choice = input("\nWould you like to save your list? (y/n): ")
        print()
        if choice.lower() == "y":
            dict_of_shopping_lists[shopping_list_name] = shopping_list
            with open("saved_shopping_lists.json", "w") as json_file:
                json_file.write(jsonpickle.encode(dict_of_shopping_lists))
            break
        elif choice.lower() == "n":
            break
        else:
            print("\nSorry, please enter 'y' or 'n'\n")

#main function to create or update and manage current shopping list
def create_or_update_shopping_list(dict_of_shopping_lists, shopping_list=None, update='no'):
    #if the user is not updating an existing list, create a new one
    if update == "no":
        shopping_list_name = str(input("Please enter a name for the new shopping list: ")).lower()
        print()
        shopping_list = ShoppingList(shopping_list_name)

    while True:
        #use menu for managing shopping list
        print("Enter 1 to add an item")
        print("Enter 2 to remove an item")
        print("Enter 3 to alter an item amount")
        print("Enter 4 to alter an item price")
        print("Enter 5 to view your list")
        print("Enter 6 to create new list")
        print("Enter 7 to exit to main menu")

        #make sure user entered an integer
        while True:
            try:
                menu_choice = int(input())
                break
            except ValueError:
                print("Please enter a valid number")

        #create new list option
        if menu_choice == 6:
            save_shopping_list_to_json_file(dict_of_shopping_lists, shopping_list_name, shopping_list)
            create_or_update_shopping_list(dict_of_shopping_lists) 
        #exit to main menu
        elif menu_choice == 7:
            save_shopping_list_to_json_file(dict_of_shopping_lists, shopping_list_name, shopping_list)
            break
        #Handle user options 1 to 5
        else:
            handle_choice(shopping_list, menu_choice)

#main function for updating an existing shopping list
def update_shopping_list(dict_of_shopping_lists):
    list_name = input("Enter the name of the shopping list to update: ")
    if list_name in dict_of_shopping_lists:
        shopping_list = dict_of_shopping_lists[list_name]
        create_or_update_shopping_list(dict_of_shopping_lists, shopping_list, "yes")
    else:
        print("Shopping list not found\n")

#function to view all saved shopping lists
def view_shopping_lists(dict_of_shopping_lists):
    if dict_of_shopping_lists:
        for key, value in dict_of_shopping_lists.items():
            print(value.view_items_in_list())
    else:
        print("You currently have no shopping lists\n")

#get user input for item name
def get_item_name_from_user():
    while True:
        item_name = str(input("\nEnter item name: ")).lower()
        if not item_name:
            print("Please enter a name")
        else:
            break
    return item_name

#get user input for item amount
def get_item_amount_from_user():
    while True:
        try:
            item_amount =  int(input("Enter amount: "))
            if item_amount < 1:
                print("Please enter an amount great than 0")
            else:
                break
        except ValueError:
            print("Please enter a whole number")
    return item_amount

#get user input for item price
def get_item_price_from_user():
    while True:
        try:
            item_price = input("Enter price (Optional): ")
            if item_price:
                item_price = float(item_price)
                break
            else:
                item_price = 0.00
                break
        except ValueError:
            print("Please enter a valid price or leave empty")
    return item_price

#Delete a shopping list and then save
def delete_shopping_lists(dict_of_shopping_lists, shopping_list_name):
    shopping_list_found = False
    for key, value in dict_of_shopping_lists.items():
        if shopping_list_name == key:
            del dict_of_shopping_lists[key]
            print(f"Shopping list {key} deleted\n")
            with open("saved_shopping_lists.json", "w") as json_file:
                json_file.write(jsonpickle.encode(dict_of_shopping_lists))
            shopping_list_found = True
            break
    if not shopping_list_found:
        print(f"Shopping list {shopping_list_name} not found\n")

#function to handle input of user from the selection of
#of the shopping list menu in create_or_update_shopping_list()
def handle_choice(list_name, value):
    try:
        #add item to shopping list
        if value == 1:
            item_name = get_item_name_from_user()
            item_amount = get_item_amount_from_user()
            item_price = get_item_price_from_user()
            list_name.add_item(item_name, item_amount, item_price)
        #remove item from shopping list
        elif value == 2:
            item_name = get_item_name_from_user()
            list_name.remove_item(item_name)
        #alter item amount in shopping list
        elif value == 3:
            item_name = get_item_name_from_user()
            item_amount = get_item_amount_from_user()
            list_name.alter_item_amount(item_name, item_amount)
        #alter item price
        elif value == 4:
            item_name = get_item_name_from_user()
            item_price = get_item_price_from_user()
            list_name.alter_item_price(item_name, item_price)
        elif value == 5:
            print(list_name.view_items_in_list())
        else:
            print("\nSorry, not a valid option\n")
    except ItemNotFoundError as e:
        print(e)

def user_menu_main(dict_of_shopping_lists):
    while True:
        #main user menu
        print("Enter 1 to update existing shopping lists")
        print("Enter 2 to create a new shopping list")
        print("Enter 3 to view all shopping lists")
        print("Enter 4 to delete shopping lists")
        print("Enter 5 to exit")

        #make sure user entered a integer
        while True:
            try:
                menu_choice = int(input())
                print()
                break
            except ValueError:
                print("Please enter a valid number")
        
        if menu_choice == 1:
            if not dict_of_shopping_lists:
                print("No shopping lists to update\n")
            else:
                update_shopping_list(dict_of_shopping_lists)
        elif menu_choice == 2:
            create_or_update_shopping_list(dict_of_shopping_lists)    
        elif menu_choice == 3:
            if not dict_of_shopping_lists:
                print("No shopping lists to view\n")
            else:
                view_shopping_lists(dict_of_shopping_lists)
        elif menu_choice == 4:
            if not dict_of_shopping_lists:
                print("No shopping lists to delete\n")
            else:
                shopping_list_name = input("Enter name of shopping list to delete: ")
                delete_shopping_lists(dict_of_shopping_lists, shopping_list_name)
        elif menu_choice == 5:
            exit()
        else:
            print("Invalid choice.")

def main():
    dict_of_shopping_lists = {}
    shopping_list_file_path = "saved_shopping_lists.json"
    if os.path.exists(shopping_list_file_path):
        with open("saved_shopping_lists.json") as json_file:
            dict_of_shopping_lists = jsonpickle.decode(json_file.read())
    user_menu_main(dict_of_shopping_lists)

if __name__ == "__main__":
    main()
