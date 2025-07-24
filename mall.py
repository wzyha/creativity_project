import sqlite3

class MallSys:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def start(self):
        print("欢迎来到达亿瓦商城渔具系统")
        self.show_menu()

    def show_menu(self):
        print("a.进入商家页面")
        print("b.进入买家页面")
        choice = input()
        if choice == 'a':
            self.merchant_menu()
        elif choice == 'b':
            self.buyer_menu()
        else:
            print("无效选项，请重新输入")
            self.show_menu()

    def merchant_menu(self):
        print("欢迎来到商家登录界面")
        print("a.登录")
        print("b.注册")
        print("c.返回")
        choice = input()
        if choice == 'a':
            self.merchant_login()
        elif choice == 'b':
            self.merchant_register()
        elif choice == 'c':
            self.start()
        else:
            print("无效选项，请重新输入")
            self.merchant_menu()

    def merchant_login(self):
        user = input("请输入用户名：")
        pwd = input("请输入密码：")
        self.check_merchant(user, pwd)

    def merchant_register(self):
        user = input("请输入新用户名：")
        pwd = input("请输入新密码：")
        self.cur.execute("SELECT * FROM merchanttable WHERE username=?", (user,))
        if self.cur.fetchone():
            print("该用户名已被注册，请选择其他用户名。")
            self.merchant_register()
        else:
            self.cur.execute("INSERT INTO merchanttable (username, password) VALUES (?,?)", (user, pwd))
            self.conn.commit()
            print("注册成功，请返回登录页面。")
            self.merchant_menu()

    def check_merchant(self, user, pwd):
        self.cur.execute("SELECT * FROM merchanttable WHERE username=? AND password=?", (user, pwd))
        m_user = self.cur.fetchone()
        if m_user:
            print("登录成功")
            self.show_inventory(user)
        else:
            print("用户名不存在或密码错误")
            self.merchant_menu()

    def show_inventory(self, user):
        self.cur.execute("SELECT productname, number FROM store WHERE username=? ORDER BY number DESC", (user,))
        inv = self.cur.fetchall()
        if not inv:
            print("我的库存：无")
            self.handle_inventory(user)
        else:
            print("我的库存：")
            for i, item in enumerate(inv, start=1):
                print(f"{i}、{item[0]}   {item[1]}个")
            self.handle_inventory(user)

    def handle_inventory(self, user):
        print("a、下架")
        print("b、补货")
        print("c、返回")
        choice = input()
        if choice == 'a':
            self.remove_product(user)
        elif choice == 'b':
            self.restock_product(user)
        elif choice == 'c':
            self.merchant_menu()
        else:
            print("无效选项，请重新输入")
            self.handle_inventory(user)

    def remove_product(self, user):
        print("我的库存：")
        self.cur.execute("SELECT productname, number FROM store WHERE username=? ORDER BY number DESC", (user,))
        inv = self.cur.fetchall()
        for i, item in enumerate(inv, start=1):
            print(f"{i}、{item[0]}   {item[1]}个")
        prod_index = int(input("请输入要下架的商品编号：")) - 1
        if 0 <= prod_index < len(inv):
            self.cur.execute("DELETE FROM store WHERE productname=? AND username=?", (inv[prod_index][0], user))
            self.conn.commit()
            print("商品下架成功。")
            self.show_inventory(user)
        else:
            print("无效的商品编号。")
            self.remove_product(user)

    def restock_product(self, user):
        self.cur.execute("SELECT productname FROM product")
        prods = self.cur.fetchall()
        for i, prod in enumerate(prods, start=0):
            print(f"{i + 1}、{prod[0]}")
        prod_index = int(input("请输入要补货的商品编号：")) - 1
        if 0 <= prod_index < len(prods):
            prod_name = prods[prod_index][0]
            qty = int(input("请输入补货数量："))
            self.cur.execute("SELECT * FROM store WHERE productname=? AND username=?", (prod_name, user))
            if self.cur.fetchone():
                self.cur.execute("UPDATE store SET number=number+? WHERE productname=? AND username=?",
                                (qty, prod_name, user))
            else:
                self.cur.execute("INSERT INTO store (productname, number, username) VALUES (?,?,?)",
                                (prod_name, qty, user))
            self.conn.commit()
            print("补货成功。")
            self.show_inventory(user)
        else:
            print("无效的商品编号。")
            self.restock_product(user)

    def buyer_menu(self):
        print("欢迎来到买家登录界面")
        print("a.登录")
        print("b.注册")
        print("c.返回")
        choice = input()
        if choice == 'a':
            self.buyer_login()
        elif choice == 'b':
            self.buyer_register()
        elif choice == 'c':
            self.start()
        else:
            print("无效选项，请重新输入")
            self.buyer_menu()

    def buyer_login(self):
        user = input("请输入用户名：")
        pwd = input("请输入密码：")
        self.check_buyer(user, pwd)

    def buyer_register(self):
        user = input("请输入新用户名（新建）：")
        pwd = input("请输入新密码：")
        self.cur.execute("SELECT * FROM customertable WHERE username=?", (user,))
        if self.cur.fetchone():
            print("该用户名已被注册，请选择其他用户名。")
            self.buyer_register()
        else:
            self.cur.execute("INSERT INTO customertable (username, password) VALUES (?,?)", (user, pwd))
            self.conn.commit()
            print("注册成功")
            self.buyer_menu()

    def check_buyer(self, user, pwd):
        self.cur.execute("SELECT * FROM customertable WHERE username=? AND password=?", (user, pwd))
        b_user = self.cur.fetchone()
        if b_user:
            print(f"欢迎, {user}")
            self.buyer_interface(user)
        else:
            print("用户名不存在或密码错误")
            self.buyer_menu()

    def buyer_interface(self, user):
        print(f"a.我的购买")
        print("b.商城")
        print("c.返回")
        choice = input()
        if choice == 'a':
            self.show_purchases(user)
        elif choice == 'b':
            self.show_store(user)
        elif choice == 'c':
            self.start()
        else:
            print("无效选项，请重新输入")
            self.buyer_interface(user)

    def show_purchases(self, user):
        self.cur.execute("SELECT productname, number FROM storage WHERE username=?", (user,))
        pur = self.cur.fetchall()
        if not pur:
            print("0、返回")
            print("我的购买：无")

            self.handle_purchases(user)
        else:
            print("0、返回")
            print(f"{user}的购买：")
            for i, item in enumerate(pur, start=1):
                print(f"{i}、{item[0]}   {item[1]}个")
            self.handle_purchases(user)

    def handle_purchases(self, user):
        choice = input()
        if choice == '0':
            self.buyer_interface(user)
        else:
            print("无效选项，请重新输入")
            self.handle_purchases(user)

    def show_store(self, user):
        self.cur.execute("SELECT username, productname, number FROM store")
        stor_items = self.cur.fetchall()
        if not stor_items:
            print("商城：无商品")
        else:
            print("商城（若想买先输入1，不想购买直接按0）：")
            for i, item in enumerate(stor_items, start=1):
                print(f"{i}、{item[0]}   {item[1]}   {item[2]}个")
            self.handle_store(user)

    def handle_store(self, user):
        choice = input()
        if choice == '0':
            self.buyer_interface(user)
        elif choice == '1':
            self.buy_product(user)
        else:
            print("无效选项，请重新输入")
            self.handle_store(user)

    def buy_product(self, user):
        seller_user = input("你想买谁家的商品？")
        prod_name = input("买他家什么产品")
        qty = int(input("买几个"))
        self.cur.execute("SELECT number FROM store WHERE username=? AND productname=?", (seller_user, prod_name))
        avail_qty_res = self.cur.fetchone()
        if avail_qty_res:
            avail_qty = avail_qty_res[0]
            if avail_qty >= qty:
                # 检查storage表中是否已有相同商品的记录
                self.cur.execute("SELECT * FROM storage WHERE username=? AND productname=?", (user, prod_name))
                stor_res = self.cur.fetchone()
                if stor_res:
                    # 如果已有记录，则更新数量
                    self.cur.execute("UPDATE storage SET number = number + ? WHERE username=? AND productname=?",
                                     (qty, user, prod_name))
                else:
                    # 如果没有记录，则插入新记录
                    self.cur.execute("INSERT INTO storage (username, productname, number) VALUES (?, ?, ?)",
                                     (user, prod_name, qty))
                self.conn.commit()  # 提交事务，确保storage表的更新
                # 更新store表中商品的数量
                self.cur.execute("UPDATE store SET number = number - ? WHERE username=? AND productname=?",
                                 (qty, seller_user, prod_name))
                self.conn.commit()  # 提交事务，确保store表的更新
                self.cur.execute("SELECT number FROM store WHERE username=? AND productname=?",
                                 (seller_user, prod_name))
                upd_qty = self.cur.fetchone()[0]
                if upd_qty <= 0:
                    self.cur.execute("DELETE FROM store WHERE username=? AND productname=?", (seller_user, prod_name))
                    self.conn.commit()  # 提交事务，确保商品数量为0时从store表中删除
                print("购买成功。")
                self.show_store(user)
            else:
                print("库存不足，购买失败。")
                self.show_store(user)
        else:
            print("商品不存在或卖家不存在。")
            self.show_store(user)