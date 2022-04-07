import pandas as pd
import sys
import datetime
import os

ITEM_MASTER_CSV_PATH="./item_master.csv"
RECEIPT_FOLDER="./receipt"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_count_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        
    def add_item_order(self,item_code,item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
    
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
    
    # 1.オーダー番号から商品情報を取得する
    def get_item_data(self,item_code):
        for m in self.item_master:
            if item_code==m.item_code:
                return m.item_name,m.price
    
    # 2, 4.オーダー入力
    def input_order(self):
        print("いらっしゃいませ！")
        while True:
            buy_item_code=input("購入したい商品を入力してください。登録を完了する場合は、0を入力してください >>> ")
            if int(buy_item_code)!=0:
                # マスタに存在するかチェック
                check=self.get_item_data(buy_item_code)
                if check!=None:
                    print("{}が登録されました".format(check[0]))
                    buy_item_count=input("個数を入力してください >>> ")
                    self.add_item_order(buy_item_code,buy_item_count)
                else:
                    print("「{}」は商品マスタに存在しません".format(buy_item_code))
            else:
                print("商品登録を終了します。")
                break
    
    def view_order(self):
        number=1
        self.sum_price=0
        self.sum_count=0
        self.receipt_name="receipt_{}.log".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        for item_order,item_count in zip(self.item_order_list,self.item_count_list):
            result=self.get_item_data(item_order)
            self.sum_price+=result[1]*int(item_count)
            self.sum_count+=int(item_count)
            receipt_data="{0}.{2}({1}) : ¥{3:,} {4}個 = ¥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)
            number+=1
            
            # 5.合計金額、個数の表示
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("合計金額:¥{:,} {}個".format(self.sum_price,self.sum_count))

    def input_and_change_money(self):
        if len(self.item_order_list)>=1:
            while True:
                self.money=int(input("お預かり金を入力してください >>> "))
                self.change_money = self.money - self.sum_price #おつり
                if self.change_money>=0:
                    self.write_receipt("お預かり金:¥{:,}".format(self.money))
                    self.write_receipt("お釣り:¥{:,}".format(self.change_money))
                    break
                else:
                    print("¥{:,} 不足しています。再度入力してください".format(self.change_money))
            
            print("お買い上げありがとうございました！")
    
    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "\\" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")

# 3.マスタ登録
def add_item_master_by_csv(csv_path):
    print("-------マスタ登録開始---------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"item_code":object})
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print("{}({})".format(item_name,item_code))
            count+=1
        print("{}品の登録が完了しました。".format(count))
        print("-------マスタ登録完了---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("-------マスタ登録完了---------")
        sys.exit()


# メイン処理
def main():
    # 3.マスタ登録
    item_master=add_item_master_by_csv(ITEM_MASTER_CSV_PATH) # CSVからマスタへ登録
    order=Order(item_master) #マスタをオーダーに登録
    # 2.オーダー入力
    order.input_order()
    # 1. 6.オーダー番号から商品情報を取得
    order.view_order()
    order.input_and_change_money()
    
if __name__ == "__main__":
    main()