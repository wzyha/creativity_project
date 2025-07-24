from mall import MallSys

if __name__ == "__main__":
    db_name = 'shop.db'
    mall_sys = MallSys(db_name)
    mall_sys.start()