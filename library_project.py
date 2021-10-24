import datetime
import sys
import gspread  # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pprint
from time import sleep
from tqdm import tqdm, trange  # pip install tqdm


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
cred = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)
client = gspread.authorize(cred)

sheet1 = client.open('database').worksheet('Sheet1')
sheet2 = client.open('database').worksheet('Sheet2')
history = client.open('database').worksheet('history')
cart = client.open('database').worksheet('cart')

data_book = sheet2.get_all_values()

class Node:
    def __init__(self, data = None, next = None, prev = None):
        self.data = data
        self.next = next
        self.prev = prev


class Function(Node):
    def __init__(self, data):
        super().__init__(data)
        self.username = None
        self.borrow = 'borrow'
        self.return_ = 'return'
        self.head1 = None

    def login(self):
        print("♥ ▌▌=======Login=======▌▌ ♥")
        Username = input("Enter Username: ")
        password = input("Enter password: ")
        try:
            check_Username = sheet1.find(Username)
            check_Password = sheet1.find(password)
            if check_Username != None:
                if check_Username.row == check_Password.row:
                    print("Successfully logged in!")
                    for _ in tqdm(range(10), desc='Loading ...', ascii=False):
                        time.sleep(0.1)
                    self.username = Username
                    print('\n !!Connect!! \n')
                    return True
                else:
                    print("\n Invalid email or password \n")
                    return False
            else:
                print("\n Invalid email or password \n")
                return False
        except:
            print("\n Invalid email or password \n")
            return False

    def register(self):
        print("♥ ▌▌============Register============▌▌ ♥")
        print('!Password must be 6 characters long.')
        Username = input("Enter Username: ")
        Password = input("Enter password: ")
        Check_Username = sheet1.find(Username)
        if not len(Password) <= 5:
            if not Username == None:
                if len(Username) < 1:
                    print("Please provide a username \n")
                    return False
                elif not Check_Username == None:
                    print("Username exists \n")
                    return False
                else:
                    user = [Username, Password]
                    sheet1.append_row(user)
                    for _ in tqdm(range(10), desc='Loading ...', ascii=False):
                        time.sleep(0.1)
                    print("\n Successfully \n")
                    return True
        else:
            print("Password too short")
            return False

    # HISTORY
    def history_insert(self, user, type, name, amount):
        data = [user, type, name, amount, str(datetime.datetime.now().ctime())]
        history.append_row(data)

    def history_print_fromUser(self, user):
        values_list = history.get_all_records()
        his_list = []
        for i in values_list:
            if i['User'] == user:
                temp_list = [i['User'], i['Type'], i['Name'], i['Amount'], i['time_stamp']]
                his_list.append(temp_list)
        return his_list

    # CART
    def cart_insert(self, user, type, name, amount):
        data = [user, type, name, amount, str(datetime.datetime.now().ctime())]
        cart.append_row(data)

    def cart_print(self, user):
        value_list = cart.get_all_records()
        cart_list = []
        for i in value_list:
            if i['User'] == user and int(i['Amount']) > 0:
                temp_list = [i['User'], i['Type'], i['Name'], i['Amount'], i['time_stamp']]
                cart_list.append(temp_list)
        return cart_list

    def find_cell(self, user, name):
        cell1 = cart.findall(user)
        cell2 = cart.findall(name)
        x = None
        for i in cell1:
            for j in cell2:
                if i.row == j.row:
                    x = i.row
        cell = 'D' + str(x)
        return cell

    def cart_update(self, user, name, amount):
        data = self.cart_print(user)
        for i in data:
            if name == i[2]:
                i[3] = i[3] + amount
                cell = self.find_cell(user, name)
                cart.update(cell, i[3])
                return

        self.cart_insert(user, self.borrow, name, amount)
        return

    # BOOK
    def book_manager(self, user, type, name, amount):
        if type == "borrow":
            self.book_update(name, -amount)
            self.history_insert(user, type, name, amount)
            self.cart_update(user, name, amount)
        elif type == "return":
            self.book_update(name, amount)
            self.history_insert(user, type, name, amount)
            self.cart_update(user, name, -amount)

    def book_update(self, name, amount):
        cell_list = sheet2.findall(name)
        cell_update = 'D' + str(cell_list[0].row)
        val = sheet2.acell(cell_update).value
        x = int(val) + amount
        sheet2.update(cell_update, x)

    # SEARCH
    def search(self, search_term):
        Name_Book = []
        values_list_Book = sheet2.col_values(2)
        for i in values_list_Book[1:]:
            if i not in Name_Book:
                Name_Book.append(i)

        search_term.strip().lower()
        match_books = []
        for book in Name_Book:
            if search_term in book.lower():
                match_books.append(book)
        count = 1
        for x in match_books:
            Namebook = x
            match_books_Type_lower = [[j.lower() for j in i] for i in sheet2.get_all_values()]
            for o, v in zip(sheet2.get_all_values(), match_books_Type_lower):
                if Namebook.lower() in v:
                    print('\n', count, ')', 'Name', '>>', o[1], '\n     Description : ', o[2], '\n     Amount : ',
                          o[3], '\n     Serial Number : ', o[4])
                    count = count + 1
        return match_books

    def store_book(self):
        data = sheet2.get_all_records()
        for i in data:
            self.appendDLL(i)

    def book_select_manager(self, option, name = None):
        self.store_book()
        if option == 'detail':
            data = self.get_dataDll_by_name(self.head1, name)
            return data
        elif option == 'book_list':
            data = self.get_dataDll_all(self.head1)
            return data


    # LINKED LIST
    def appendDLL(self, new_data ):
        new_node = Node(new_data)
        if self.head1 is not None:
            self.appendDLLre(self.head1, new_data)
        else:
            self.head1 = new_node

    def appendDLLre(self, linked_list, new_data ):
        last = linked_list
        if last.next is None:
            new_node = Node(data = new_data)
            last.next = new_node
            new_node.prev = last
            return
        else:
            return self.appendDLLre(linked_list.next, new_data)

    def get_dataDll_all(self, linked_list):
        node = linked_list
        list1 = []
        while node:
            list1.append(node.data)
            last = node
            node = node.next
        return list1

    def get_dataDll_by_name(self, linked_list, name):
        node = linked_list
        list1 = []
        while node:
            if node.data["Name"] == name:
                list1.append(node.data)
                return list1
            else:
                last = node
                node = node.next

    def clear_head(self):
        self.head1 = None

    # Additional functions
    def check_amount_book(self, name, amount_W):
        values_list = sheet2.col_values(2)
        temp = 0
        for i in values_list:
            temp = temp +1
            if i == name:
                str1 = 'D'+str(temp)
                val = sheet2.acell(str1).value
                if amount_W > int(val):
                    return False
                else:
                    return True




class Display(Function):

    def __init__(self,data = None):

        super().__init__(data)

    # USER
    def welcome_page(self):
        print("Welcome to your dashboard")
        option = input("Login | Register:")
        if option.upper() == "LOGIN":
            if self.login():
                self.menu_page()

        elif option.upper() == "REGISTER":
            self.register_page()
        else:
            print("Please enter a valid parameter")
            self.welcome_page()

    def login_page(self):
        if self.login():
            self.menu_page()
        else:
            self.login_page()

    def register_page(self):
        if self.register():
            self.login()
        else:
            self.register_page()

    # MAIN APPLICATION
    def menu_page(self):
        print("""==============LIBRARY MENU===============
            1. Library
            2. Request a book ###sus
            3. Cart
            4. Exit
            5. History
            =========================================""")
        option = int(input("Enter your option: "))
        if option == 1:
            self.library_page()
        elif option == 2:
            pass
        elif option == 3:
            self.cart_page()
        elif option == 4:
            sys.exit()
        elif option == 5:
            self.history_page()
        else:
            print("=" * 41, "\nInvalid option.", "\n" * 7)
            print("=" * 41)
            self.menu_page()

    def library_page(self):
        print('====LIBRARY PAGE====')
        print('  + Search key 1\n  + See all books key 2 \n  + Back to menu key 0')
        option = int(input("Choose how to access the book"))
        if option == 1:
            self.search_page()
        elif option == 2:
            self.main_all_book_page()
        elif option == 0:
            self.menu_page()
            self.head1 = None
        else:
            print('Valid key')
            self.library_page()

    def history_page(self):
        print('')
        print("HISTORY USER {} PAGE".format(self.username))
        data = self.history_print_fromUser(self.username)
        for i in data:
            print('')
            print("{}  {} Book :{} Amount : {} Time : {}".format(i[0], i[1], i[2], i[3], i[4]))
        if int(input("Key 0 for exit ")) == 0:
            self.menu_page()
        else:
            print("Invalid key")
            self.history_page()

    def cart_page(self):
        print('')
        print("CART PAGE")
        data = self.cart_print(self.username)
        temp = 0
        for i in data:
            temp = temp + 1
            print('')
            print("{}  {} Book :{} Amount : {} Time : {}".format(temp, i[1], i[2], i[3], i[4]))
        option = int(input("Return key 1 ,  Exit key 0 : "))
        if option == 1:
            print()
            book_number = int(input("Choose a book number to return : "))
            if book_number > int(temp) or book_number < 1:
                print('Invalid Choose ')
                self.cart_page()
            amount = int(input("How many books will you return ? : "))

            if amount > int(data[book_number - 1][3]) or amount <= 0:
                print("Invalid amount")
                self.cart_page()
            else:
                book_name = data[book_number - 1][2]
                self.book_manager(self.username, self.return_, book_name, amount)
                print("Success !!")
                self.cart_page()

        elif option == 0:
            self.menu_page()
        else:
            print("Invalid key")
            self.cart_page()

    # SUBPAGE
    def search_page(self):
        search_term = str(input("Please enter a book title to search for: "))
        data = self.search(search_term)
        if data == []:
            print("Not found")
            self.search_page()

        print("===Choose option===")
        option = int(input("Key 1 for borrow or key 0 for back"))
        if option == 1:
            number_book = int(input('Choose number fo book or 0 for exit : '))
            amount = int(input("How many books do you want to borrow? : "))
            if self.check_amount_book(data[number_book-1], amount) is True:
                self.book_manager(self.username, 'borrow', data[number_book-1], amount)
                print('Success !!!')
                self.search_page()
            else:
                print('Not enough books')
                self.search_page()
        elif option > len(data) or option < 0:
            print("Input invalid")
            self.search_page()
        elif option == 0:
            self.menu_page()

    def main_all_book_page(self):
        self.head1 = None
        list_all_B = self.book_select_manager('book_list')
        temp = 0
        list_n_name = []
        for i in list_all_B:
            temp = temp+1
            t1 = [temp, i['Name']]
            list_n_name.append(t1)
            print('{}  {}  '.format(temp, i["Name"]))
        option = int(input("Choose number fo book or 0 for exit"))
        if option == 0:
            self.menu_page()
        elif option > temp or option < 0:
            print("Valid input")
            self.clear_head()
            self.main_all_book_page()
        else:
            name_book = None
            for i in list_n_name:
                if i[0] == option:
                    name_book = i[1]
            self.book_detail_page(name_book)

    def book_detail_page(self, name):
        list_a_B = self.book_select_manager('detail', name)
        print('+ {} \n number of books left : {}'.format(list_a_B[0]['Name'],list_a_B[0]['amount']))
        print(list_a_B[0]['Description'])
        print('borrow books key 1')
        option = int(input("Key 0 for back"))
        if option == 0:
            self.main_all_book_page()
        elif option < 0 :
            print("Invalid key")
            self.book_detail_page(name)
        elif option == 1:
            amount = int(input("How many books do you want to borrow? : "))
            if self.check_amount_book(name, amount) is True:
                self.book_manager(self.username, 'borrow', name, amount)
                print("Success !!!")
                self.main_all_book_page()
            else:
                print('Not enough books')
                self.main_all_book_page()



if __name__ == '__main__':
    a = Display()
    a.welcome_page()













    #    def cart_page(self):
    #       print('')
    #       print("CART USER {} PAGE".format(self.username))
    #       data = self.cart_print(self.username)
    #       for i in data:
    #           print('')
    #          print("{} Book :{} Amount : {} Time : {}".format(i[1], i[2], i[3], i[4]))
    #     if int(input("Key 1 for exit ")) == 1:
    #        self.menu_page()
    #   else:
    #      print("Invalid key")
    #     self.cart_page()