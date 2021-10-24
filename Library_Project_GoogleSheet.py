import datetime  # เรียกใช้ module ชื่อ datatime
import sys  # เรียกใช้ module ชื่อ sys

import gspread  # pip install gspread เรียกใช้ module ชื่อ gspread
# จาก oauth2client.service_account เรียกใช้ module ชื่อ ServiceAccountCredentials
from oauth2client.service_account import ServiceAccountCredentials
import time  # เรียกใช้ module ชื่อ time

# pip install tqdm  #จาก tqdm เรียกใช้ module ชื่อ tqdm และ trange
from tqdm import tqdm, trange
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',  # scope คือ การกำหนดตัวแปลเพื่อเข้าถึง ati
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

cred = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope)
client = gspread.authorize(cred)

sheet1 = client.open('database').worksheet('Sheet1')
sheet2 = client.open('database').worksheet('Sheet2')
history = client.open('database').worksheet('history')
cart = client.open('database').worksheet('cart')


class Node:  # สร้างclass node
    # สร้างฟังก์ชั่น__init__ รับข้อมูล self, data เป็น None, next เป็น None และ prev เป็น None
    def __init__(self, data=None, next=None, prev=None):
        self.data = data  # self.data รับข้อมูล data
        self.next = next  # self.next รับข้อมูล next
        self.prev = prev  # self.prev รับข้อมูล prev


class Function(Node):   # สร้างclass Function รับข้อมูลจาก class Node
    def __init__(self, data):  # สร้างฟังก์ชั่น__init__ รับข้อมูล self และ data
        super().__init__(data)  # เป็นพารามิเตอร์ รับข้อมูลจาก data
        self.username = None  # self.username รับข้อมูลเป็น None
        self.borrow = 'borrow'  # self.borrow รับข้อมูล string 'borrow'
        self.return_ = 'return'  # self.return_ รับข้อมูล string 'return'
        self.head1 = None  # self.head1 รับข้อมูลเป็น None

    def login(self):  # สร้างฟังก์ชั่น login รับข้อมูล self
        print("♥ ▌▌=======Login=======▌▌ ♥")  # แสดงผลข้อความ login
        Username = input("Enter Username: ")  # Username รับข้อมูลจาก user
        password = input("Enter password: ")  # password รับข้อมูลจาก user
        try:  # ทำการเช็ค error
            # check_Username ค้นหาคำใน sheet1 จาก Username
            check_Username = sheet1.find(Username)
            # check_Password ค้าหาคำใน sheet1 จาก password
            check_Password = sheet1.find(password)
            if check_Username != None:  # ถ้า check_Username ไม่เท่ากับ None
                if check_Username.row == check_Password.row:  # ถ้า check_Username.row เท่ากับ check_Password.row
                    # แสดงผลข้อความ Successfully logged in!
                    print("Successfully logged in!")
                    # ใช้การวนลูปเพื่อโหลดและแสดงข้อความ Loading,ค่า ascii เป็น False
                    for _ in tqdm(range(10), desc='Loading ...', ascii=False):
                        time.sleep(0.1)  # เวลานับถอยหลัง 0.1 วินาที
                    self.username = Username  # self.username รับข้อมูล Username
                    print('\n !!Connect!! \n')  # แสดงผลข้อความ !!Connect!!
                    return True  # ส่งคืนค่า True
                else:  # เขื่อนไขอื่นนอกจาก if
                    # แสดงผลข้อความ Invalid email or password
                    print("\n Invalid email or password \n")
                    return False  # ส่งคืนค่า False
            else:  # เงื่อนไขอื่นนอกจาก if
                # แสดงผลข้อความ Invalid email or password
                print("\n Invalid email or password \n")
                return False  # ส่งคืนค่า False
        except:  # ทำการเช็ค error
            # แสดงผลข้อความ Invalid email or password
            print("\n Invalid email or password \n")
            return False  # ส่งคืนค่า False

    def register(self):  # สร้างฟังก์ชั่น register รับข้อมูล self
        # แสดงผลข้อความ Register
        print("♥ ▌▌============Register============▌▌ ♥")
        # แสดงผลข้อความ !Password must be 6 characters long.
        print('!Password must be 6 characters long.')
        Username = input("Enter Username: ")  # Username รับข้อมูลจาก user
        Password = input("Enter password: ")  # Password รับข้อมูลจาก user
        # Check_Username ค้นหาคำใน sheet1 จากตัวแปร Username
        Check_Username = sheet1.find(Username)
        if not len(Password) <= 5:  # ถ้าความยาว string ของ Password น้อยกว่าหรือเท่ากับ 5
            if not Username == None:  # ถ้า Username ไม่เท่ากับ None
                if len(Username) < 1:  # ถ้าความยาว string ของ Username น้อยกว่า 1
                    # แสดงผลข้อความ Please provide a username
                    print("Please provide a username \n")
                    return False  # ส่งคืนค่า False
                elif not Check_Username == None:  # ถ้า Check_Username ไม่ใช่ค่า None
                    print("Username exists\n")  # แสดงผลข้อความ Username exists
                    return False  # ส่งคืนค่า False
                else:  # เงื่อนไขอื่นนอกจาก if
                    # user รับข้อมูลมาเก็บในรูปแบบ array
                    user = [Username, Password]
                    # เพิ่มแถวใน sheet1 รับข้อมูลจาก user
                    sheet1.append_row(user)
                    # ใช้การวนลูปเพื่อโหลดและแสดงข้อความ Loading,ค่า ascii เป็น False
                    for _ in tqdm(range(10), desc='Loading ...', ascii=False):
                        time.sleep(0.1)  # เวลานับถอยหลัง 0.1 วินาที
                    print("\n Successfully \n")  # แสดงผลข้อความ Successfully
                    return True  # ส่งคืนค่า True
        else:  # เงื่อนไขอื่นนอกจาก if
            print("Password too short")  # แสดงผลข้อความ "Password too short"
            return False  # ส่งคืนค่า False

    # HISTORY
    # สร้างฟังก์ชั่น history_insert รับค่า self ,user ,type ,name , amount
    def history_insert(self, user, type, name, amount):
        # data รับข้อมูลมาเก็บในรูปแบบ array
        data = [user, type, name, amount, str(datetime.datetime.now().ctime())]
        history.append_row(data)  # เพิ่มแถวใน history รับข้อมูลจาก data

    # สร้างฟังก์ชั่น history_print_fromUser รับค่า self และ user
    def history_print_fromUser(self, user):
        # values_list รับข้อมูลมาเก็บในรูปแบบ HashMaps
        values_list = history.get_all_records()
        his_list = []  # his_list รับข้อมูลเป็น list ว่าง
        for i in values_list:  # ใช้การวนลูปค่า i ใน values_list
            if i['User'] == user:  # ถ้าค่า i['User'] เท่ากับ user
                # temp_list รับข้อมูลมาเก็บในรูปแบบ array
                temp_list = [i['User'], i['Type'],
                             i['Name'], i['Amount'], i['time_stamp']]
                his_list.append(temp_list)  # เพิ่มข้อมูล temp_list ใน his_list
        return his_list  # ส่งคืนค่า his_list

    # CART
    # สร้างฟังก์ชั่น cart_insert รับค่า self ,user ,type ,name , amount
    def cart_insert(self, user, type, name, amount):
        # data รับข้อมูลมาเก็บในรูปแบบ array
        data = [user, type, name, amount, str(datetime.datetime.now().ctime())]
        cart.append_row(data)  # เพิ่มแถวใน cart รับข้อมูลจาก data

    def cart_print(self, user):  # สร้างฟังก์ชั่น cart_print รับค่า self,user
        # values_list รับข้อมูลมาเก็บในรูปแบบ HashMaps
        value_list = cart.get_all_records()
        cart_list = []      # cart_list รับข้อมูลเป็น list ว่าง
        for i in value_list:  # ใช้การวนลูปค่า i ใน values_list
            # ถ้าค่า i['User'] เท่ากับ user และ int ของ i['Amount']
            if i['User'] == user and int(i['Amount']) > 0:
                # temp_list รับข้อมูลมาเก็บในรูปแบบ array
                temp_list = [i['User'], i['Type'],
                             i['Name'], i['Amount'], i['time_stamp']]
                # เพิ่มข้อมูล temp_list ใน cart_list
                cart_list.append(temp_list)
        return cart_list  # ส่งคืนค่า cart_list

    def find_cell(self, user, name):  # สร้างฟังก์ชั่น find_call รับค่า self ,user ,name
        # cell1 รับข้อมูลจากการค้นหาข้อมูล cart รับข้อมูลจาก user
        cell1 = cart.findall(user)
        # cell2 รับข้อมูลจากการค้นหาข้อมูล cart รับข้อมูลจาก name
        cell2 = cart.findall(name)
        x = None  # ค่า x เป็น None
        for i in cell1:  # ใช้การวนลูปค่า i ใน cell1
            for j in cell2:  # ใช้การวนลูปค่า j ใน cell2
                if i.row == j.row:  # ถ้าข้อมูลแถว i เท่ากับ ข้อมูลแถว j
                    x = i.row  # ค่า x รับข้อมูลจาก i.row
        cell = 'D' + str(x)  # cell รับข้อมูล string D รวมกับ string x
        return cell  # ส่งคืนค่า cell

    # สร้างฟังก์ชั่น cart_update รับค่า self ,user ,name ,amount
    def cart_update(self, user, name, amount):
        # data รับข้อมูลจากการสร้าง cart_print รับข้อมูลจาก user
        data = self.cart_print(user)
        for i in data:  # ใช้การวนลูปค่า i ใน data
            if name == i[2]:  # ถ้า name เท่ากับ i[2]
                i[3] = i[3] + amount        # i[3] รับข้อมูลจาก i[3] + amount
                # cell รับข้อมูลจากการสร้าง find_cell รับข้อมูลจาก user และ name
                cell = self.find_cell(user, name)
                # ทำการ update ข้อมูล cart จากค่า cell และ i[3]
                cart.update(cell, i[3])
                return  # ส่งคืนค่า

        # self.cart_insert รับข้อมูลจาก user ,self.borrow ,name ,amount
        self.cart_insert(user, self.borrow, name, amount)
        return  # ส่งคืนค่า

    # BOOK
    # สร้างฟังก์ชั่น book_manager รับค่า self ,user ,type ,name , amount
    def book_manager(self, user, type, name, amount):
        if type == "borrow":  # ถ้า type เท่ากับ "borrow"
            self.book_update(name, -amount)  # update ข้อมูล
            self.history_insert(user, type, name, amount)  # เพิ่มข้อมูล
            self.cart_update(user, name, amount)  # update ข้อมูล
        elif type == "return":  # ถ้า type เท่ากับ "return"
            self.book_update(name, amount)  # update ข้อมูล
            self.history_insert(user, type, name, amount)  # เพิ่มข้อมูล
            self.cart_update(user, name, -amount)  # update ข้อมูล

    # สร้างฟังก์ชั่น book_update รับค่า self ,name , amount
    def book_update(self, name, amount):
        # cell_list รับข้อมูลจากการค้นหาข้อมูล sheet2 รับข้อมูลจาก name
        cell_list = sheet2.findall(name)
        # cell_update รับข้อมูลจาก string D รวมกับ String ของแถว cell_list ตัวที่ 0
        cell_update = 'D' + str(cell_list[0].row)
        # val รับข้อมูลจาก sheet2 จาก acell ของ cell_update
        val = sheet2.acell(cell_update).value
        x = int(val) + amount  # ค่า x รับข้อมูล int val
        # update sheet2 รับข้อมูลจาก cell_update และ x
        sheet2.update(cell_update, x)

    # SEARCH
    def search(self, search_term):  # สร้างฟังก์ชั่น search รับข้อมูล self และ search_term
        Name_Book = []  # Name_Book รับข้อมูลเป็น list ว่าง
        # values_list_Book รับข้อมูลจากคอลั่มที่ 2 ของ sheet2
        values_list_Book = sheet2.col_values(2)
        # ใช้การวนลูปค่า i ใน values_list_Book[1:]
        for i in values_list_Book[1:]:
            if i not in Name_Book:  # ถ้า i ไม่อยู่ใน Name_Book
                Name_Book.append(i)  # เพิ่มข้อมูล i ใน Name_Book

        # ทำการตัดช่องว่างและแปลงเป็นอักษรพิมพ์เล็กของ search_term
        search_term.strip().lower()
        match_books = []  # match_books รับข้อมูลเป็น list ว่าง
        for book in Name_Book:  # ใช้การวนลูปข้อมูล book ใน Name_Book
            if search_term in book.lower():  # ถ้า search_term ใน book.lower()
                match_books.append(book)  # เพิ่มข้อมูล book ใน match_books
        count = 1   # count มีค่าเป็น 1
        for x in match_books:  # ใช้การวนลูปค่า x ใน match_books
            Namebook = x     # Namebook รับข้อมูลจาก x
            # match_books_Type_lower รับข้อมูลมาเก็บในรูปแบบ array
            match_books_Type_lower = [[j.lower() for j in i]
                                      for i in sheet2.get_all_values()]
            # ใช้การวนรูปค่า o,v ใน zip ของ sheet2.get_all_values() และ match_books_Type_lower
            for o, v in zip(sheet2.get_all_values(), match_books_Type_lower):
                if Namebook.lower() in v:  # ถ้าตัวอักษรพิมพ์เล็กของ Namebook อยู่ใน v
                    print('\n', count, ')', 'Name', '>>', o[1], '\n     Description : ', o[2], '\n     Amount : ',
                          o[3], '\n     Serial Number : ', o[4])  # แสดงผลข้อมูล count และแสดงผลข้อความ 'Name', '>>' Description : 'Amount : ' Serial Number : '
                    count = count + 1  # count รับข้อมูลจาก count+1
        return match_books  # ส่งคืนค่า match_books

    def store_book(self):  # ฟังก์ชั่น store_book
        data = sheet2.get_all_records()  # เก็บข้อมูลไว้ในรูปแบบ array
        for i in data:  # ลูปข้อมูลในอะเรย์
            self.appendDLL(i)

    def book_select_manager(self, option, name=None):  # ฟังก์ชั่น book_select_manager
        self.store_book()  # เรียกใช้ store_book
        if option == 'detail':  # ถ้า option เหมือนคำว่า detail
            # รับข้อมูลส่วน head และ name
            data = self.get_dataDll_by_name(self.head1, name)
            return data
        elif option == 'book_list':  # ถ้า option เหมือนคำว่า book_list
            data = self.get_dataDll_all(self.head1)  # รับข้อมูลส่วน head
            return data

    # LINKED LIST
    def appendDLL(self, new_data):  # ฟังก์ชั่น appendDLL
        new_node = Node(new_data)  # กำหนดตัวแปร ข้อมูลใหม่ ใน โนด
        if self.head1 is not None:  # ข้อมูล head1 ไม่เท่ากับ none
            self.appendDLLre(self.head1, new_data)  # เพิ่มข้อมูล
        else:
            self.head1 = new_node  # กำหนดตัวแปร เท่ากับ new node

    def appendDLLre(self, linked_list, new_data):  # ฟังก์ชั่น appendDLLre
        last = linked_list  # กำหนดตัวแปร
        if last.next is None:  # เช็คข้อมูลใน node
            new_node = Node(data=new_data)
            last.next = new_node
            new_node.prev = last
            return
        else:  # นอกเหนือกรณี
            return self.appendDLLre(linked_list.next, new_data)

    def get_dataDll_all(self, linked_list):  # ฟังก์ชั่น get_dataDll_all
        node = linked_list  # กำหนดตัวแปร
        list1 = []  # สร้าง array list
        while node:  # ถ้าเป็นจริง
            list1.append(node.data)
            last = node
            node = node.next
        return list1  # คืนค่า list1

    def get_dataDll_by_name(self, linked_list, name):  # ฟังก์ชั่น get_dataDll_by_name
        node = linked_list  # node เท่ากับ linked_list
        list1 = []  # สร้าง array list
        while node:  # ถ้าเป็นจริง
            if node.data["Name"] == name:  # เช็คข้อมูล
                list1.append(node.data)  # ถ้าใช้จะเพิ่มข้อมูล
                return list1
            else:  # นอกเหนือกรณี
                last = node
                node = node.next

    def clear_head(self):  # ฟังก์ชั่น clear_head
        self.head1 = None  # กำหนด head เท่ากับ None

    # Additional functions
    def check_amount_book(self, name, amount_W):  # ฟังก์ชั่น check_amount_book
        values_list = sheet2.col_values(2)  # รับข้อมูลมาเก็บในรูปแบบอะเรย์
        temp = 0  # กำหนดตัวแปร
        for i in values_list:  # ลูปแล้วเช็คเงื่อนไข
            temp = temp + 1
            if i == name:
                str1 = 'D'+str(temp)
                val = sheet2.acell(str1).value
                if amount_W > int(val):
                    return False
                else:
                    return True


class Display(Function):  # สร้างclass Display

    def __init__(self, data=None):  # สร้างฟังก์ชั่น__init__

        super().__init__(data)  # เป็นพารามิเตอร์รับค่า data

    # USER
    def welcome_page(self):  # สร้างฟังก์ชั่น welcome_page รับค่าจาก self
        print("Welcome to  library")  # แสดงผลข้อขวาม Welcome to  library
        option = input("Login | Register:")  # option รับค่าจาก input
        if option.upper() == "LOGIN":  # ถ้าoption.upper() = LOGIN
            if self.login():  # เรียกใช้ ฟังก์ชัน login
                self.menu_page()  # เรียกใช้ ฟังก์ชัน menu_page

        elif option.upper() == "REGISTER":  # ถ้าไม่ตรงเงื่อนไขด้านบนให้ option.upper() == REGISTER
            self.register_page()  # เรียกใช้ ฟังก์ชัน register_page
        else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
            # แสดงผลข้อขวาม Please enter a valid parameter
            print("Please enter a valid parameter")
            self.welcome_page()  # เรียกใช้ ฟังก์ชัน welcome_page

    def login_page(self):  # สร้างฟังก์ชั่น login_page รับค่าจาก self
        if self.login():  # ถ้าเรียกใช้ ฟังก์ชัน login
            self.menu_page()  # เรียกใช้ ฟังก์ชัน menu_page
        else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
            self.login_page()  # เรียกใช้ ฟังก์ชัน login_page

    def register_page(self):  # สร้างฟังก์ชั่น register_page รับค่าจาก self
        if self.register():  # ถ้าเรียกใช้ ฟังก์ชัน register
            self.login()  # เรียกใช้ ฟังก์ชัน login
        else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
            self.register_page()  # เรียกใช้ ฟังก์ชัน register

    # MAIN APPLICATION
    def menu_page(self):  # สร้างฟังก์ชั่น menu_page รับค่าจาก self
        print("""==============LIBRARY MENU===============
            [1] Library
            [2] Request a book
            [3] Cart
            [4] History
            [5] Exit
=========================================""")  # แสดงข้อความ
        option = int(input("Enter your option: "))  # option รับค่าจาก input
        if option == 1:  # ถ้า option == 1
            self.library_page()  # เรียกใช้ ฟังก์ชัน library_page
        elif option == 2:  # ถ้า option == 2
            self.main_all_book_page()  # เรียกใช้ ฟังก์ชัน main_all_book_page
        elif option == 3:  # ถ้า option == 2
            self.cart_page()  # เรียกใช้ ฟังก์ชัน cart_page
        elif option == 4:  # ถ้า option == 2
            self.history_page()  # เรียกใช้ ฟังก์ชัน history_page
        elif option == 5:  # ถ้า option == 2
            # แสดงข้อความ Thank you for using the service.
            print('Thank you for using the service.')
            sys.exit()  # เรียกใช้ ฟังก์ชัน exit
        else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
            print("=" * 41, "\nInvalid option.", "\n" * 7)  # แสดงข้อความ.
            print("=" * 41)  # แสดงข้อความ
            self.menu_page()  # เรียกใช้ ฟังก์ชัน menu_page

    def library_page(self):  # สร้างฟังก์ชั่น library_page รับค่าจาก self
        print("""==============LIBRARY MENU===============
            [1] Search        
            [2] See all books 
            [0] Back to menu  
=========================================""")  # แสดงข้อความ
        option = int(input("Choose how to access the book: ")
                     )  # option รับค่าจาก input
        print("="*41)  # แสดงข้อความ

        if option == 1:  # ถ้า option == 1
            self.search_page()  # เรียกใช้ ฟังก์ชัน search_page
        elif option == 2:  # ถ้า option == 2
            self.main_all_book_page()  # เรียกใช้ ฟังก์ชัน main_all_book_page
        elif option == 0:  # ถ้า option == 0
            self.menu_page()  # เรียกใช้ ฟังก์ชัน menu_page
            self.head1 = None   # self.head1 รับค่า None
        else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
            print('Valid key')  # แสดงข้อความ Valid key
            self.library_page()  # เรียกใช้ ฟังก์ชัน library_page

    def history_page(self):  # สร้างฟังก์ชัน history_page รับค่า self
        print('')  # แสดงผลข้อความ
        # แสดงผลข้อความชื่อผู้ใช้
        print("HISTORY USER {} PAGE".format(self.username))
        # data รับค่า self.history_print_fromUser(self.username)
        data = self.history_print_fromUser(self.username)
        for i in data:  # สร้างลูป i in data
            print('')  # แสดงผมข้อความ
            print("{}  {} Book :{} Amount : {} Time : {}".format(i[0], i[1], i[2], i[3], i[
                4]))  # แสดงผมข้อความ ชื่อหนังสือ จำนวน เวลา ตามประวัติ
        try:  # สร้างคำสั่ง try ตรวจสอบข้อผิดพลาด
            # ถ้ารับค่า int จาก input เท่ากับ 1
            if int(input("\n Enter Key [1] for bake page: ")) == 1:
                self.menu_page()  # เรียกใช้ฟังก์ชัน menu_page
            else:  # ถ้าไม่เข้าเงื่อนไข
                print(
                    "=======================Invalid key==========================\n")  # แสดงผลข้อความ
                self.history_page()  # เรียกใช้ฟังก์ชัน history_page
        except:  # ถ้าเกิดข้อผิดพลาด
            print(
                "=======================Invalid key==========================\n")  # แสดงผลข้อความ
            self.history_page()  # เรียกใช้ฟังก์ชัน history_page

    def cart_page(self):  # สร้างฟังก์ชัน cart_page รับค่า self
        print('')  # แสดงผลข้อความ
        print("CART PAGE")  # แสดงผลข้อความ CART PAGE
        # data รับค่า self.cart_print(self.username)
        data = self.cart_print(self.username)
        temp = 0  # ให้ tamp = 0
        for i in data:  # สร้างลูป i in data
            temp = temp + 1  # temp รับค่า temp + 1
            print('')  # แสดงผลข้อความ
            print("{}  {} Book :{} Amount : {} Time : {}".format(temp, i[1], i[2], i[3], i[
                4]))  # แสดงผลข้อความ ชื่อหนังสือ จำนวน เวลา ตามประวัติ
        # option รับค่า int จาก input
        option = int(input("Return key [1] ,  Exit key [0]: "))
        if option == 1:  # ถ้า option = 1
            # book_number รับค่า int จาก input
            book_number = int(input("Choose a book number to return: "))
            if book_number > int(
                    temp) or book_number < 1:  # ถ้า book_number มากกว่า temp หรือ book_number น้อยกว่า 1
                print('Invalid Choose ')  # แสดงผลข้อความ Invalid Choose
                self.cart_page()  # เรียกใช้ฟังก์ชัน cart_page
            # amount รับค่า int จาก input
            amount = int(input("How many books will you return ?: "))

            # ถ้า amount มากกว่า (data[book_number - 1][3]) หรือ amount น้อยกว่าหรือเท่ากับ 0
            if amount > int(data[book_number - 1][3]) or amount <= 0:
                # แสดงผลข้อความ ================Invalid amount=================
                print("================Invalid amount=================")
                self.cart_page()  # เรียกใช้ฟังก์ชัน cart_page
            else:  # ถ้าไม่เข้าเงื่อนไข
                # ให้ book_name = data[book_number - 1][2]
                book_name = data[book_number - 1][2]
                self.book_manager(self.username, self.return_, book_name,
                                  amount)  # เรียกใช้ฟังก์ชัน book_manager(self.username, self.return_, book_name, amount)
                # แสดงผลข้อความ ===================Success=====================
                print("===================Success=====================")
                self.cart_page()  # เรียกใช้ฟังก์ชัน cart_page

        elif option == 0:  # ถ้า option = 0
            self.menu_page()  # เรียกใช้ฟังก์ชัน menu_page
        else:  # ถ้าไม่เข้าเงื่อนไข
            print("Invalid key")  # แสดงผลข้อความ Invalid key
            self.cart_page()  # เรียกใช้ฟังก์ชัน cart_page

    # SUBPAGE
    def search_page(self):  # สร้างฟังก์ชัน search_page รับค่า self
        # search_term รับค่า str จาก input
        search_term = str(input("Please enter a book title to search for: "))
        data = self.search(search_term)  # data รับค่า self.search(search_term)
        if data == []:  # ถ้า data = list
            print(
                "=================Not found==================")  # แสดงผลข้อความ
            self.search_page()  # เรียกใช้ฟังก์ชัน search_page

        option = int(input("""==============Choose option===============
            [1] Borrow       
            [2] Back         
=========================================\nEnter you Select: """))  # option รับค่า int จาก input
        if option == 1:  # ถ้า option = 1
            number_book = int(
                input('Choose number fo book or Enter [0] for exit : '))  # number_book รับค่า int จาก input
            # amount รับค่า int จาก input
            amount = int(input("How many books do you want to borrow? : "))
            if self.check_amount_book(data[number_book - 1],
                                      amount) is True:  # ถ้า self.check_amount_book(data[number_book-1], amount) เป็นจริง
                self.book_manager(self.username, 'borrow', data[number_book - 1],
                                  amount)  # เรียกใช้ฟังก์ชัน self.book_manager(self.username, 'borrow', data[number_book-1], amount)
                print('!!! Success !!! \n')  # แสดงผลข้อความ !!! Success !!!
                self.menu_page()  # เรียกใช้ฟังก์ชัน menu_page
            else:  # ถ้าไม่เข้าเงื่อนไข
                print(
                    '=========================Not enough books===================')  # แสดงผลข้อความ =========================Not enough books===================
                self.search_page()  # เรียกใช้ฟังก์ชัน search_page
        # ถ้า option มากกว่า data หรือ option น้อยกว่า 0
        elif option > len(data) or option < 0:
            print(
                "========================Input invalid=========================")  # แสดงผลข้อความ
            self.search_page()  # เรียกใช้ฟังก์ชัน search_page
        elif option == 0:  # ถ้า option = 0
            self.menu_page()  # เรียกใช้ฟังก์ชัน menu_page

    def main_all_book_page(self):  # สร้างฟังก์ชัน main_all_book_page รับค่า self
        self.head1 = None  # ให้ self.head1 = None
        list_all_B = self.book_select_manager(
            'book_list')  # list_all_B รับค่า self.book_select_manager('book_list')
        temp = 0  # ให้ temp = 0
        list_n_name = []  # ให้ list_n_name = list
        for i in list_all_B:  # สร้างลูป i in list_all_B
            temp = temp + 1  # ให้ temp = temp+1
            t1 = [temp, i['Name']]  # t1 รับค่า [temp, i['Name']]
            list_n_name.append(t1)  # เพิ่ม t1 ใน list_n_name
            # แสดงผลข้อความ temp และ ชื่อ
            print('{})  {}  '.format(temp, i["Name"]))
        # option รับค่า int จาก intput
        option = int(input("Choose number fo book or [0] for exit: "))
        if option == 0:  # ถ้า option = 0
            self.menu_page()  # เรียกใช้ฟังก์ชัน menu_page
        elif option > temp or option < 0:  # ถ้า option มากกว่า temp หรือ option น้อยกว่า 0
            # แสดงผลข้อความ
            print("=======================Valid input==========================")
            self.clear_head()   # เรียกใช้ฟังก์ชัน clear_head
            self.main_all_book_page()   # เรียกใช้ฟังก์ชัน main_all_book_page
        else:   # ถ้าไม่เข้าเงื่อนไข
            name_book = None    # ให้ name_book = None
            for i in list_n_name:   # สร้างลูป i in list_n_name
                if i[0] == option:  # ถ้า i[0] = option
                    name_book = i[1]    # ให้ name_book = i[1]
            # เรียกใช้ฟังก์ชัน book_detail_page(name_book)
            self.book_detail_page(name_book)

    def book_detail_page(self, name):  # สร้างฟังก์ชั่น book_detail_page รับค่าจาก self
        list_a_B = self.book_select_manager(
            'detail', name)  # รับข้อมูลมาเก็บในรูปแบบ array
        # แสดงข้อความ ชื่อหนังสือ และจำนวนที่เหลือ
        print(
            '+ {} \n number of books left : {}'.format(list_a_B[0]['Name'], list_a_B[0]['amount']))
        print(list_a_B[0]['Description'])  # แสดงข้อความ อธิบาย
        # แสดงข้อความ borrow books Enter key [1]
        print('borrow books Enter key [1]')
        # option รับค่าจาก input
        option = int(input("Enter Key [0] for back: "))
        if option == 0:  # ถ้า option == 0
            self.main_all_book_page()  # เรียกใช้ ฟังก์ชัน main_all_book_page
        elif option < 0:  # ถ้า option == 0
            # แสดงข้อความ ===========================Invalid key========================
            print("===========================Invalid key========================")
            self.book_detail_page(name)  # เรียกใช้ book_detail_page
        elif option == 1:  # ถ้า option == 1
            # amount รับค่า int จากinput
            amount = int(input("How many books do you want to borrow? : "))
            # ถ้าเรียกใช้ ฟังก์ชัน check_amount_book(name, amount) เป็นจริง
            if self.check_amount_book(name, amount) is True:
                # เรียกใช้ ฟังก์ชัน book_manager(self.username, 'borrow', name, amount)
                self.book_manager(self.username, 'borrow', name, amount)
                # แสดงข้อความ ========================Success==========================
                print("\n========================Success==========================")
                self.main_all_book_page()  # เรียกใช้ ฟังก์ชัน main_all_book_page
            else:  # ถ้าไม่เข้าเงื่อนไขอะไรเลย
                # แสดงข้อความ ====================Not enough books========================
                print('====================Not enough books========================')
                self.main_all_book_page()  # เรียกใช้ ฟังก์ชัน main_all_book_page


if __name__ == '__main__':
    a = Display()
    a.welcome_page()
