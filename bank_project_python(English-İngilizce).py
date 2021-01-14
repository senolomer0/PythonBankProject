from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
import sys
import sqlite3
import time
from datetime import datetime
import locale
import random
import requests
from bs4 import BeautifulSoup
import sip

login_account_number = list()
unregister_account_number = list()

foreign_currency_url = "https://www.x-rates.com/table/?from=USD&amount=1"
response = requests.get(foreign_currency_url)
html_content = response.content
soup = BeautifulSoup(html_content,"html.parser")
list1 = soup.find_all("td",{"class":"rtRates"})
main_page_turkish_lira_information = list1[119].text
main_page_euro_information = list1[1].text
main_page_pound_information = list1[3].text
turkish_lira_information = float(list1[119].text.replace(",","."))
euro_information = float(list1[1].text.replace(",","."))
pound_information = float(list1[3].text.replace(",","."))
swiss_franc_information = float(list1[13].text.replace(",","."))
canadian_dollar_information = float(list1[9].text.replace(",","."))
russian_rouble_information = float(list1[101].text.replace(",","."))
swedish_krona_information = float(list1[109].text.replace(",","."))
japanese_yen_information = float(list1[65].text.replace(",","."))
kuwaiti_dinar_information  = float(list1[71].text.replace(",","."))
china_yuan_information = float(list1[89].text.replace(",","."))
list_of_currency_values = [["Turkish Liras",turkish_lira_information],["Euro",euro_information],["British Pound",pound_information],["Swiss Franc",swiss_franc_information],["Canadian Dollar",canadian_dollar_information],["Russian Rouble",russian_rouble_information],["Swedish Krona",swedish_krona_information],["Japan Yen",japanese_yen_information],["Kuwaiti Dinar",kuwaiti_dinar_information],["China Yuan",china_yuan_information]]

investment_url = "https://tradingeconomics.com/united-states/stock-market"
response = requests.get(investment_url)
html_content = response.content
soup = BeautifulSoup(html_content,"html.parser")
list2 = soup.find_all("td",{"id":"p"})
msft_information = float(list2[4].text)
aapl_information = float(list2[5].text)
jnj_information = float(list2[6].text)
v_information = float(list2[7].text)
wmt_information = float(list2[8].text)
pg_information = float(list2[9].text)
jpm_information = float(list2[10].text)
unh_information = float(list2[11].text)
intc_information = float(list2[12].text)
hd_information = float(list2[13].text)
stock_list = [["MSFT",msft_information],["AAPL",aapl_information],["JNJ",jnj_information],["V",v_information],["WMT",wmt_information],["PG",pg_information],["JPM",jpm_information],["UNH",unh_information],["INTC",intc_information],["HD",hd_information]]

class Main_Menu(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_login_page()
        self.setWindowTitle("Alize Bank")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))

    def get_info(self):
        self.connection = sqlite3.connect("bankdatabase.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("select * from BANK_CUSTOMERS where Account_No = ?",(login_account_number[0],))
        info_list = self.cursor.fetchall()
        self.account_name = info_list[0][0]
        self.account_balance = info_list[0][3]
        self.account_balance = round(self.account_balance,2)
        self.account_debt = float(info_list[0][4])
        self.account_debt = round(self.account_debt,2)
        self.cursor.execute("select * from CURRENCY where Account_No = ?",(login_account_number[0],))
        currency_list = self.cursor.fetchall()
        self.account_turkishlira = currency_list[0][1]
        self.account_euro = currency_list[0][2]
        self.account_pound = currency_list[0][3]
        self.account_swissfranc = currency_list[0][4]
        self.account_canadiandollar = currency_list[0][5]
        self.account_russianrouble = currency_list[0][6]
        self.account_swedishkrona = currency_list[0][7]
        self.account_japaneseyen = currency_list[0][8]
        self.account_kuwaitidinar = currency_list[0][9]
        self.account_chinayuan = currency_list[0][10]
        self.cursor.execute("select * from INVESTMENT where Account_No = ?",(login_account_number[0],))
        investment_list = self.cursor.fetchall()
        self.account_msft = investment_list[0][1]
        self.account_aapl = investment_list[0][2]
        self.account_jnj = investment_list[0][3]
        self.account_v = investment_list[0][4]
        self.account_wmt = investment_list[0][5]
        self.account_pg = investment_list[0][6]
        self.account_jpm = investment_list[0][7]
        self.account_unh = investment_list[0][8]
        self.account_intc= investment_list[0][9]
        self.account_hd = investment_list[0][10]

        self.total_currency_balance = (self.account_turkishlira+self.account_euro+self.account_pound+self.account_swissfranc+self.account_canadiandollar+self.account_russianrouble+self.account_swedishkrona+self.account_japaneseyen+self.account_kuwaitidinar+self.account_chinayuan)
        self.total_currency_balance = round(self.total_currency_balance,2)

        self.total_investment_balance = (self.account_msft+self.account_aapl+self.account_jnj+self.account_v+self.account_wmt+self.account_pg+self.account_jpm+self.account_unh+self.account_intc+self.account_hd)
        self.total_investment_balance = round(self.total_investment_balance,2)

    def add_right_account_widgets(self):
        self.remove_right_widgets()
        self.get_info()
        self.balance = QtWidgets.QLabel()
        self.balance.setText("Balance: $"+str(self.account_balance))
        self.balance.setFont(QtGui.QFont("arial",20))
        self.debt = QtWidgets.QLabel()
        self.debt.setText("Debt: $"+str(self.account_debt))
        self.debt.setFont(QtGui.QFont("arial",20))
        self.currency = QtWidgets.QLabel()
        self.currency.setText("Currency Balance: $"+str(self.total_currency_balance))
        self.currency.setFont(QtGui.QFont("arial",20))
        self.investment = QtWidgets.QLabel()
        self.investment.setText("Investment Balance: $"+str(self.total_investment_balance))
        self.investment.setFont(QtGui.QFont("arial",20))
        self.error= QtWidgets.QLabel()
        self.error.setFont(QtGui.QFont("arial",11))
        self.error.setStyleSheet("color:red;")

        self.infobox.addStretch()
        self.infobox.addWidget(self.balance)
        self.infobox.addWidget(self.debt)
        self.infobox.addWidget(self.currency)
        self.infobox.addWidget(self.investment)
        self.infobox.addWidget(self.error)
        self.infobox.addStretch()

    def number(self,test):
        a=0
        for i in list(test.text()):
            if(i=="-"):
                return 2
            if((i>="0" and i<="9") or i=="."):
                a+=1
            else:
                a=0
        if(a == len(test.text())):
            return 1
        else:
            return 0

    def remove_right_widgets(self):
        for i in reversed(range(self.infobox.count())):
            layoutItem = self.infobox.takeAt(i)
            if layoutItem.widget() is not None:
                widgetToRemove = layoutItem.widget()
                widgetToRemove.setParent(None)
                self.infobox.removeWidget(widgetToRemove)
        try:
            for i in reversed(range(self.plate_h_box.count())):
                    layoutItem = self.plate_h_box.takeAt(i)
                    if layoutItem.widget() is not None:
                        widgetToRemove = layoutItem.widget()
                        widgetToRemove.setParent(None)
                        self.plate_h_box.removeWidget(widgetToRemove)
        except:
            pass
            
    def create_right_widget_content(self):
        self.amount = QtWidgets.QLineEdit()
        self.amount.setMinimumSize(280,35)
        self.amount_text = QtWidgets.QLabel()
        self.amount_text.setFont(QtGui.QFont("arial",13))
        self.amount_text.setStyleSheet("color:green;")
        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")
        self.butonspacer = QtWidgets.QLabel()
        self.pay_button.setStyleSheet("background-color:green;color:white;")
        self.pay_button.setFont(QtGui.QFont("arial",10))
        self.pay_button.setMinimumSize(300,35)
        self.infobox.addStretch()
        self.infobox.addWidget(self.amount_text)
        self.infobox.addWidget(self.amount)
        self.infobox.addWidget(self.butonspacer)
        self.infobox.addWidget(self.pay_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addStretch()
    
    def account_info(self):
        self.remove_right_widgets()
        self.add_right_account_widgets()

    def deposit_money(self):
        self.remove_right_widgets()

        def control():
            x = self.number(self.amount)
            if(x==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1): 
                if(len(self.amount.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.amount.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.amount.text())%10!=0):
                        self.error_text.setText("**Please enter a value in 10 or multiples.**")
                    elif(int(self.amount.text())>100000):
                        self.error_text.setText("**A maximum of 100.000 TL can be deposited\nat a time.**")
                    else:
                        deposit()

        def deposit():
            new_balance = self.account_balance + float(self.amount.text())
            self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
            self.connection.commit()
            
            self.remove_right_widgets()
            self.add_right_account_widgets()

        self.pay_button = QtWidgets.QPushButton("Deposit Money")
        self.create_right_widget_content()
        self.amount_text.setText("The balance you want to deposit:")

        self.pay_button.clicked.connect(control)

    def withdraw_money(self):
        if(self.account_balance ==0):
            self.remove_right_widgets()
            self.add_right_account_widgets()
            self.error.setText("**You don't have a balance you can\nwithdraw.**")
        else:
            self.remove_right_widgets()
            def control():
                x = self.number(self.amount)
                if(x==0):
                    self.error_text.setText("**Please enter numbers only.**")  
                elif(x==2):
                    self.error_text.setText("**Please enter a positive number.**") 
                elif(x==1): 
                    if(len(self.amount.text())==0):
                        self.error_text.setText("**Please enter a value.**")
                    else:
                        if(self.amount.text()=="0"):
                            self.error_text.setText("**Please enter any value other than '0'.**")
                        elif(int(self.amount.text())%10!=0):
                            self.error_text.setText("**Please enter a value in 10 or multiples.**")
                        else:
                            withdraw()

            def withdraw():
                if(float(self.amount.text())>self.account_balance):
                    self.error_text.setText("**The amount you want to withdraw is\nhigher than the current balance.**")
                else:
                    new_balance = self.account_balance - float(self.amount.text())
                    self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                    self.connection.commit()
                    
                    self.remove_right_widgets()
                    self.add_right_account_widgets()

            self.pay_button = QtWidgets.QPushButton("Withdraw Money")
            self.create_right_widget_content()
            self.amount_text.setText("The balance you want to withdraw from\nthe account:")

            self.pay_button.clicked.connect(control)

    def loans(self):
        self.remove_right_widgets()

        def control():
            x = self.number(self.amount)
            y = self.number(self.month_amount)
            if(x==0 and y==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2 and y==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1 and y==1): 
                if(len(self.amount.text())==0 or len(self.month_amount.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.amount.text()=="0" or self.month_amount.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.amount.text())<10000):
                        self.error_text.setText("**A minimum of $10,000 credit can be\nwithdrawn.**")
                    elif(int(self.amount.text())%10!=0):
                        self.error_text.setText("**Please enter a value in 10 or multiples.**")
                    elif(int(self.month_amount.text())>60):
                        self.error_text.setText("**It can be paid back in a maximum of\n5 years.**")
                    else:
                        withdraw(int(self.month_amount.text()))

        def withdraw(month):
            if(month>=1 and month<=12):
                interest_amount = float(self.amount.text()) * 1.13
            elif(month>=13 and month<=36):
                interest_amount = float(self.amount.text()) * 1.21
            elif(month>=37 and month<=60):
                interest_amount = float(self.amount.text()) * 1.34
            interest_amount= round(interest_amount,3)
            monthly_tutar = round(interest_amount/month,2)
            self.remove_right_widgets()

            self.confirm_information = QtWidgets.QLabel()
            self.confirm_information.setFont(QtGui.QFont("arial",13))
            self.confirm_information.setStyleSheet("color:green;")
            self.confirm_information.setText("Money to deposit: "+str(self.amount.text())+"\nAmount to be paid monthly: "+str(monthly_tutar)+"\nTotal amount to be paid: "+str(interest_amount)+"\n")

            self.confirm_text = QtWidgets.QLabel()
            self.confirm_text.setText("Do you confirm?")
            self.confirm_text.setFont(QtGui.QFont("arial",13))
            self.confirm_text.setStyleSheet("color:green;")

            self.confirm_button = QtWidgets.QPushButton("Confirm")
            self.confirm_button.setStyleSheet("background-color:green;color:white;")
            self.confirm_button.setFont(QtGui.QFont("arial",10))
            self.confirm_button.setMinimumSize(300,35) 

            self.back_button = QtWidgets.QPushButton("Back")
            self.back_button.setStyleSheet("background-color:green;color:white;")
            self.back_button.setFont(QtGui.QFont("arial",10))
            self.back_button.setMinimumSize(300,35) 

            self.space = QtWidgets.QLabel()

            self.infobox.addStretch()
            self.infobox.addWidget(self.confirm_information)
            self.infobox.addWidget(self.confirm_text)
            self.infobox.addWidget(self.space)
            self.infobox.addWidget(self.confirm_button)
            self.infobox.addWidget(self.back_button)
            self.infobox.addStretch()
            
            def confirm():
                new_balance = self.account_balance + float(self.amount.text())
                new_debt = self.account_debt + interest_amount
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Debt = ? where Account_No = ?",(new_debt,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()
            def back():
                self.remove_right_widgets()
                self.loans()

            self.confirm_button.clicked.connect(confirm)
            self.back_button.clicked.connect(back)

        self.remove_right_widgets()

        self.amount_text = QtWidgets.QLabel()
        self.amount_text.setFont(QtGui.QFont("arial",13))
        self.amount_text.setStyleSheet("color:green;")
        self.amount_text.setText("The amount you want to borrow:")

        self.amount = QtWidgets.QLineEdit()
        self.amount.setMinimumSize(280,35)

        self.month_text = QtWidgets.QLabel()
        self.month_text.setFont(QtGui.QFont("arial",13))
        self.month_text.setStyleSheet("color:green;")
        self.month_text.setText("How many months you want to pay:")

        self.month_amount = QtWidgets.QLineEdit()
        self.month_amount.setMinimumSize(280,35)

        self.pay_button = QtWidgets.QPushButton("Loan")
        self.pay_button.setStyleSheet("background-color:green;color:white;")
        self.pay_button.setFont(QtGui.QFont("arial",10))
        self.pay_button.setMinimumSize(300,35)

        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")

        self.loan_information = QtWidgets.QLabel()
        self.loan_information.setFont(QtGui.QFont("arial",12))
        self.loan_information.setStyleSheet("color:green;")
        self.loan_information.setText("\nLoan interest rates:\n1-12 month ~~ %1.13\n13-36 month ~~ %1.21\n37-60 month ~~ %1.34")

        self.buttonspacer = QtWidgets.QLabel()
        self.buttonspacer1 = QtWidgets.QLabel()

        self.infobox.addStretch()   
        self.infobox.addWidget(self.amount_text)
        self.infobox.addWidget(self.amount)
        self.infobox.addWidget(self.buttonspacer1)
        self.infobox.addWidget(self.month_text)
        self.infobox.addWidget(self.month_amount)
        self.infobox.addWidget(self.buttonspacer)
        self.infobox.addWidget(self.pay_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addWidget(self.loan_information)
        self.infobox.addStretch()
            
        self.pay_button.clicked.connect(control)

    def debt_payment(self):
        if(self.account_debt==0):
            self.remove_right_widgets()
            self.add_right_account_widgets()
            self.error.setText("\n**You don't have any debt.**")
        else:
            self.remove_right_widgets()

            def control():
                x = self.number(self.amount)
                if(x==0):
                    self.error_text.setText("**Please enter numbers only.**")
                elif(x==2):
                    self.error_text.setText("**Please enter a positive number.**")
                elif(x==1): 
                    if(len(self.amount.text())==0):
                        self.error_text.setText("**Please enter a value.**")
                    elif(self.amount.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    else:
                        if(float(self.amount.text())> self.account_debt):
                            self.error_text.setText("**The amount you want to pay is more than\nthe current debt.**")
                        else:
                            pay()

            def pay():
                new_debt = self.account_debt - float(self.amount.text())
                new_balance = self.account_balance - float(self.amount.text())
                self.cursor.execute("update BANK_CUSTOMERS set Debt = ? where Account_No = ?",(new_debt,login_account_number[0]))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

            def pay_all():
                new_debt = 0
                new_balance = self.account_balance - self.account_debt
                self.cursor.execute("update BANK_CUSTOMERS set Debt = ? where Account_No = ?",(new_debt,login_account_number[0]))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

            def pay_all_control():
                if(self.account_balance<self.account_debt):
                    self.error_text.setText("**The amount you want to pay is higher than\nthe amount in your account balance.**")
                else:
                    pay_all()

            def create_payment_screen():
                self.remove_right_widgets()
                self.pay_button = QtWidgets.QPushButton("Pay Debt")
                self.create_right_widget_content()
                self.amount_text.setText("The amount you want to pay:")
                self.pay_button.clicked.connect(control)

            self.total_debt = QtWidgets.QLabel()
            self.total_debt.setText("Current Balance: "+str(self.account_balance)+"\nTotal Debt: "+str(self.account_debt)+"\n")
            self.total_debt.setFont(QtGui.QFont("arial",13))
            self.total_debt.setStyleSheet("color:green;")
            self.all_debt = QtWidgets.QPushButton("Pay All Debt")
            self.all_debt.setStyleSheet("background-color:green;color:white;")
            self.all_debt.setFont(QtGui.QFont("arial",10))
            self.all_debt.setMinimumSize(300,35)
            self.certain_debt = QtWidgets.QPushButton("Pay The Certain Amount of Debt")
            self.certain_debt.setStyleSheet("background-color:green;color:white;")
            self.certain_debt.setFont(QtGui.QFont("arial",10))
            self.certain_debt.setMinimumSize(300,35)
            self.error_text = QtWidgets.QLabel()
            self.error_text.setFont(QtGui.QFont("arial",11))
            self.error_text.setStyleSheet("color:red;")

            self.infobox.addStretch()
            self.infobox.addWidget(self.total_debt)
            self.infobox.addWidget(self.all_debt)
            self.infobox.addWidget(self.certain_debt)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            self.certain_debt.clicked.connect(create_payment_screen)
            self.all_debt.clicked.connect(pay_all_control)

    def money_transfer(self):
        self.cursor.execute("select * from BANK_CUSTOMERS")
        contacts = self.cursor.fetchall()
        if(len(contacts)==1):
            self.remove_right_widgets()
            self.add_right_account_widgets()
            self.error.setText("\n**There are no accounts you can send money to**")
        else:
            self.remove_right_widgets()

            def control():
                x = self.number(self.selection_number)
                y = self.number(self.selection_money)
                if(x==0 or y==0):
                    self.error_text.setText("**Please enter numbers only.**")
                elif(x==2 or y==2):
                    self.error_text.setText("**Please enter a positive number.**")
                elif(x==1 or y==1): 
                    if(len(self.selection_number.text())==0 or len(self.selection_money.text())==0):
                        self.error_text.setText("**Please enter a value.**")
                    else:
                        if(len(self.selection_number.text())!=5):
                            self.error_text.setText("**Please enter a 5 digit number in the account\nnumber section.**")
                        elif(self.selection_number.text()=="0" or self.selection_money.text()=="0"):
                            self.error_text.setText("**Please enter any value other than '0'.**")    
                        else:
                            if(int(self.selection_number.text()) in self.contacts_accountno):
                                if(self.account_balance<float(self.selection_money.text())):
                                    self.error_text.setText("**There is no balance you want to send.**") 
                                else:
                                    send()
                            else:
                                self.error_text.setText("**This account number does not exist.**") 

            def send():
                new_balance = self.account_balance - float(self.selection_money.text())
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.cursor.execute("select * from BANK_CUSTOMERS where Account_No = ?",(int(self.selection_number.text()),))
                list1 = self.cursor.fetchall()
                send_balance = float(list1[0][3])
                new_send_balance = send_balance + float(self.selection_money.text())
                send_accountno = float(list1[0][5])
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_send_balance,send_accountno))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

            contacts_name = list()
            self.contacts_accountno = list()
            for i in range(len(contacts)):
                contacts_name.append(contacts[i][0])
                self.contacts_accountno.append(contacts[i][5])
            contacts_name.remove(self.account_name)
            self.contacts_accountno.remove(login_account_number[0])
            self.table = QtWidgets.QTableWidget()
            self.table.setRowCount(len(contacts_name))
            self.table.setColumnCount(2)
            for i in range(len(contacts_name)):
                self.table.setItem(i,0,QTableWidgetItem(contacts_name[i]))
                self.table.setItem(i,1,QTableWidgetItem(str(self.contacts_accountno[i])))
            columns = ['Name', 'Account No']
            self.table.setHorizontalHeaderLabels(columns)
            self.selection = QtWidgets.QLabel()
            self.selection.setText("\nEnter the account number you want to\nsend money to:")
            self.selection.setFont(QtGui.QFont("arial",13))
            self.selection.setStyleSheet("color:green;")
            self.selection_number = QtWidgets.QLineEdit()
            self.selection_number.setMinimumSize(280,35)
            self.selection_button = QtWidgets.QPushButton("Send Money")
            self.selection_button.setStyleSheet("background-color:green;color:white;")
            self.selection_button.setFont(QtGui.QFont("arial",10))
            self.selection_button.setMinimumSize(300,35)
            self.error_text = QtWidgets.QLabel()
            self.error_text.setFont(QtGui.QFont("arial",11))
            self.error_text.setStyleSheet("color:red;")

            self.selection_text = QtWidgets.QLabel()
            self.selection_text.setText("\nEnter the amount you want to send:")
            self.selection_text.setFont(QtGui.QFont("arial",13))
            self.selection_text.setStyleSheet("color:green;")
            self.selection_money = QtWidgets.QLineEdit()
            self.selection_money.setMinimumSize(280,35)

            self.infobox.addStretch()
            self.infobox.addWidget(self.table)
            self.infobox.addWidget(self.selection)
            self.infobox.addWidget(self.selection_number)
            self.infobox.addWidget(self.selection_text)
            self.infobox.addWidget(self.selection_money)
            self.infobox.addWidget(self.selection_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            self.selection_button.clicked.connect(control)

    def foreign_currency(self):
        def buy_currency_control():
            x = self.number(self.selection_number)
            y = self.number(self.selection_money)
            if(x==0 or y==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2 or y==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1 and y==1): 
                if(len(self.selection_number.text())==0 or len(self.selection_money.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.selection_number.text()=="0" or self.selection_money.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.selection_number.text())>0 and int(self.selection_number.text())<11):
                        self.error_text.setText("")
                        buy_currency_compare()
                    else:
                        self.error_text.setText("**Please enter a number between the specified\nvalues.**")

        def sell_currency_control():
            x = self.number(self.selection_number)
            y = self.number(self.selection_money)
            if(x==0 and y==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2 and y==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1 and y==1): 
                if(len(self.selection_number.text())==0 or len(self.selection_money.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.selection_number.text()=="0" or self.selection_money.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.selection_number.text())>0 and int(self.selection_number.text())<11):
                        self.error_text.setText("")
                        sell_currency_compare()
                    else:
                        self.error_text.setText("**Please enter a number between the specified\nvalues**")

        def buy_currency_compare():
            if(self.selection_number.text()=="1"):
                total = turkish_lira_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_turkishlira+=total
                    self.cursor.execute("update CURRENCY set TL = ? where Account_No = ?",(self.account_turkishlira,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="2"):
                total = euro_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_euro+=total
                    self.cursor.execute("update CURRENCY set Euro = ? where Account_No = ?",(self.account_euro,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="3"):
                total = pound_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_pound+=total
                    self.cursor.execute("update CURRENCY set Pound = ? where Account_No = ?",(self.account_pound,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="4"):
                total = swiss_franc_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_swissfranc+=total
                    self.cursor.execute("update CURRENCY set Swiss_Franc = ? where Account_No = ?",(self.account_swissfranc,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="5"):
                total = canadian_dollar_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_canadiandollar+=total
                    self.cursor.execute("update CURRENCY set Canadian_Dollar = ? where Account_No = ?",(self.account_canadiandollar,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="6"):
                total = russian_rouble_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_russianrouble+=total
                    self.cursor.execute("update CURRENCY set Russian_Rouble = ? where Account_No = ?",(self.account_russianrouble,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="7"):
                total = swedish_krona_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_swedishkrona+=total
                    self.cursor.execute("update CURRENCY set Swedish_Krona = ? where Account_No = ?",(self.account_swedishkrona,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="8"):
                total = japanese_yen_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_japaneseyen+=total
                    self.cursor.execute("update CURRENCY set Japan_Yen = ? where Account_No = ?",(self.account_japaneseyen,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="9"):
                total = kuwaiti_dinar_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_kuwaitidinar+=total
                    self.cursor.execute("update CURRENCY set Kuwaiti_Dinar = ? where Account_No = ?",(self.account_kuwaitidinar,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="10"):
                total = china_yuan_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_chinayuan+=total
                    self.cursor.execute("update CURRENCY set China_Yuan = ? where Account_No = ?",(self.account_chinayuan,login_account_number[0]))
                    self.connection.commit()
            else:
                pass
            if(x==1):
                change_balance()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        def sell_currency_compare():
            x=0
            if(self.selection_number.text()=="1"):
                if(float(self.selection_money.text())>float(self.account_turkishlira)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_turkishlira-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Dolar = ? where Account_No = ?",(self.account_turkishlira,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="2"):
                if(float(self.selection_money.text())>float(self.account_euro)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_euro-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Euro = ? where Account_No = ?",(self.account_euro,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="3"):
                if(float(self.selection_money.text())>float(self.account_pound)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_pound-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Pound = ? where Account_No = ?",(self.account_pound,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="4"):
                if(float(self.selection_money.text())>float(self.account_swissfranc)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_swissfranc-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Swiss_Franc = ? where Account_No = ?",(self.account_swissfranc,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="5"):
                if(float(self.selection_money.text())>float(self.account_canadiandollar)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_canadiandollar-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Canadian_Dollar = ? where Account_No = ?",(self.account_canadiandollar,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="6"):
                if(float(self.selection_money.text())>float(self.account_russianrouble)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_russianrouble-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Russian_Rouble = ? where Account_No = ?",(self.account_russianrouble,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="7"):
                if(float(self.selection_money.text())>float(self.account_swedishkrona)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_swedishkrona-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Swedish_Krona = ? where Account_No = ?",(self.account_swedishkrona,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="8"):
                if(float(self.selection_money.text())>float(self.account_japaneseyen)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_japaneseyen-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Japan_Yen = ? where Account_No = ?",(self.account_japaneseyen,login_account_number[0]))
                    self.connection.commit()
                    x=1 
            elif(self.selection_number.text()=="9"):
                if(float(self.selection_money.text())>float(self.account_kuwaitidinar)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_kuwaitidinar-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set Kuwaiti_Dinar = ? where Account_No = ?",(self.account_kuwaitidinar,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="10"):
                if(float(self.selection_money.text())>float(self.account_chinayuan)):
                    self.error_text.setText("**You don't have enough foreign currency to\ndo this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_chinayuan-=float(self.selection_money.text())
                    self.cursor.execute("update CURRENCY set China_Yuan = ? where Account_No = ?",(self.account_chinayuan,login_account_number[0]))
                    self.connection.commit()
                    x=1
            else:
                pass
            if(x==1):
                change_balance()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        def balance_control(total):
            if(self.account_balance<total):
                self.error_text.setText("**The balance is not enough.**")
            else:
                return 1

        def change_balance():
            self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(self.account_balance,login_account_number[0]))
            self.connection.commit()

        def buy_currency():
            self.remove_right_widgets()
            self.selection_button = QtWidgets.QPushButton("Buy Currency")
            self.selection_button.setStyleSheet("background-color:green;color:white;")
            self.selection_button.setFont(QtGui.QFont("arial",10))
            self.selection_button.setMinimumSize(300,35)
            self.selection.setText("\nEnter the number of the currency you\nwant to buy:")
            self.selection_text.setText("\nHow much do you want to get:")
            self.error_text.setText("")
            table = QtWidgets.QTableWidget()
            table.setRowCount(len(list_of_currency_values))
            table.setColumnCount(2)
            for i in range(len(list_of_currency_values)):
                table.setItem(i,0,QTableWidgetItem(list_of_currency_values[i][0]))
                table.setItem(i,1,QTableWidgetItem(str(list_of_currency_values[i][1])))
            columns = ['Currency', 'Unit Price']
            table.setHorizontalHeaderLabels(columns)
            self.infobox.addStretch()
            self.infobox.addWidget(table)
            self.infobox.addWidget(self.selection)
            self.infobox.addWidget(self.selection_number)
            self.infobox.addWidget(self.selection_text)
            self.infobox.addWidget(self.selection_money)
            self.infobox.addWidget(self.selection_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()
            self.selection_button.clicked.connect(buy_currency_control)
        
        def sell_currency():
            if(int(self.total_currency_balance)<0):
                self.error_text.setText("**You do not have foreign currency to sell.**")
            else:
                self.remove_right_widgets()
                self.selection_button = QtWidgets.QPushButton("Sell Currency")
                self.selection_button.setStyleSheet("background-color:green;color:white;")
                self.selection_button.setFont(QtGui.QFont("arial",10))
                self.selection_button.setMinimumSize(300,35)
                self.selection.setText("\nEnter the number of the currency you want\nto sell:")
                self.selection_text.setText("\nHow much do you want to sell:")
                table = QtWidgets.QTableWidget()
                table.setRowCount(len(list_of_currency_values))
                table.setColumnCount(3)
                for i in range(len(list_of_currency_values)):
                    table.setItem(i,0,QTableWidgetItem(list_of_currency_values[i][0]))
                    table.setItem(i,1,QTableWidgetItem(str(list_of_currency_values[i][1])))
                self.get_info()
                table.setItem(0,2,QTableWidgetItem(str(round(self.account_turkishlira,2))))
                table.setItem(1,2,QTableWidgetItem(str(round(self.account_euro,2))))
                table.setItem(2,2,QTableWidgetItem(str(round(self.account_pound,2))))
                table.setItem(3,2,QTableWidgetItem(str(round(self.account_swissfranc,2))))
                table.setItem(4,2,QTableWidgetItem(str(round(self.account_canadiandollar,2))))
                table.setItem(5,2,QTableWidgetItem(str(round(self.account_russianrouble,2))))
                table.setItem(6,2,QTableWidgetItem(str(round(self.account_swedishkrona,2))))
                table.setItem(7,2,QTableWidgetItem(str(round(self.account_japaneseyen,2))))
                table.setItem(8,2,QTableWidgetItem(str(round(self.account_kuwaitidinar,2))))
                table.setItem(9,2,QTableWidgetItem(str(round(self.account_chinayuan,2))))
                columns = ['Currency', 'Unit Price','Current Balance']
                table.setHorizontalHeaderLabels(columns)
                self.infobox.addStretch()
                self.infobox.addWidget(table)
                self.infobox.addWidget(self.selection)
                self.infobox.addWidget(self.selection_number)
                self.infobox.addWidget(self.selection_text)
                self.infobox.addWidget(self.selection_money)
                self.infobox.addWidget(self.selection_button)
                self.infobox.addWidget(self.error_text)
                self.infobox.addStretch()
                self.selection_button.clicked.connect(sell_currency_control)

        self.remove_right_widgets()  
        self.selection = QtWidgets.QLabel()
        self.selection.setText("\nEnter the number of the currency you\nwant to buy:")
        self.selection.setFont(QtGui.QFont("arial",13))
        self.selection.setStyleSheet("color:green;")
        self.selection_number = QtWidgets.QLineEdit()
        self.selection_number.setMinimumSize(280,35)
        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")
        self.selection_text = QtWidgets.QLabel()
        self.selection_text.setFont(QtGui.QFont("arial",13))
        self.selection_text.setStyleSheet("color:green;")
        self.selection_money = QtWidgets.QLineEdit()
        self.selection_money.setMinimumSize(280,35)

        self.buy_currency_button = QtWidgets.QPushButton("Buy Currency")
        self.buy_currency_button.setStyleSheet("background-color:green;color:white;")
        self.buy_currency_button.setFont(QtGui.QFont("arial",10))
        self.buy_currency_button.setMinimumSize(300,35)
        self.sell_currency_button = QtWidgets.QPushButton("Sell Currency")
        self.sell_currency_button.setStyleSheet("background-color:green;color:white;")
        self.sell_currency_button.setFont(QtGui.QFont("arial",10))
        self.sell_currency_button.setMinimumSize(300,35)
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(300,35)

        self.infobox.addStretch()
        self.infobox.addWidget(self.buy_currency_button)
        self.infobox.addWidget(self.sell_currency_button)
        self.infobox.addWidget(self.back_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addStretch()

        self.buy_currency_button.clicked.connect(buy_currency)
        self.sell_currency_button.clicked.connect(sell_currency)
        self.back_button.clicked.connect(self.add_right_account_widgets)

    def investment_(self):
        def buy_shares_control():
            x = self.number(self.selection_number)
            y = self.number(self.selection_money)
            if(x==0 or y==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2 or y==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1 and y==1): 
                if(len(self.selection_number.text())==0 or len(self.selection_money.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.selection_number.text()=="0" or self.selection_money.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.selection_number.text())>0 and int(self.selection_number.text())<11):
                        self.error_text.setText("")
                        buy_shares_compare()
                    else:
                        self.error_text.setText("**Please enter a number between the specified\nvalues**")

        def sell_shares_control():
            x = self.number(self.selection_number)
            y = self.number(self.selection_money)
            if(x==0 and y==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2 and y==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1 and y==1): 
                if(len(self.selection_number.text())==0 or len(self.selection_money.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                else:
                    if(self.selection_number.text()=="0" or self.selection_money.text()=="0"):
                        self.error_text.setText("**Please enter any value other than '0'.**")
                    elif(int(self.selection_number.text())>0 and int(self.selection_number.text())<11):
                        self.error_text.setText("")
                        sell_shares_compare()
                    else:
                        self.error_text.setText("**Please enter a number between the specified\nvalues**")

        def buy_shares_compare():
            if(self.selection_number.text()=="1"):
                total = msft_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_msft+=total
                    self.cursor.execute("update INVESTMENT set MSFT = ? where Account_No = ?",(self.account_msft,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="2"):
                total = aapl_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_aapl+=total
                    self.cursor.execute("update INVESTMENT set AAPL = ? where Account_No = ?",(self.account_aapl,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="3"):
                total = jnj_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_jnj+=total
                    self.cursor.execute("update INVESTMENT set JNJ = ? where Account_No = ?",(self.account_jnj,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="4"):
                total = v_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_v+=total
                    self.cursor.execute("update INVESTMENT set V = ? where Account_No = ?",(self.account_v,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="5"):
                total = wmt_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_wmt+=total
                    self.cursor.execute("update INVESTMENT set WMT = ? where Account_No = ?",(self.account_wmt,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="6"):
                total = pg_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_pg+=total
                    self.cursor.execute("update INVESTMENT set PG = ? where Account_No = ?",(self.account_pg,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="7"):
                total = jpm_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_jpm+=total
                    self.cursor.execute("update INVESTMENT set JPM = ? where Account_No = ?",(self.account_jpm,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="8"):
                total = unh_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_unh+=total
                    self.cursor.execute("update INVESTMENT set UNH = ? where Account_No = ?",(self.account_unh,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="9"):
                total = intc_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_intc+=total
                    self.cursor.execute("update INVESTMENT set INTC = ? where Account_No = ?",(self.account_intc,login_account_number[0]))
                    self.connection.commit()
            elif(self.selection_number.text()=="10"):
                total = hd_information*int(self.selection_money.text())
                x = balance_control(total)
                if(x==1):
                    self.account_balance-=total
                    self.account_hd+=total
                    self.cursor.execute("update INVESTMENT set HD = ? where Account_No = ?",(self.account_hd,login_account_number[0]))
                    self.connection.commit()
            else:
                pass
            if(x==1):
                change_balance()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        def sell_shares_compare():
            x=0
            if(self.selection_number.text()=="1"):
                if(float(self.selection_money.text())>float(self.account_msft)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_msft-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set MSFT = ? where Account_No = ?",(self.account_msft,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="2"):
                if(float(self.selection_money.text())>float(self.account_aapl)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_aapl-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set AAPL = ? where Account_No = ?",(self.account_aapl,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="3"):
                if(float(self.selection_money.text())>float(self.account_jnj)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_jnj-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set JNJ = ? where Account_No = ?",(self.account_jnj,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="4"):
                if(float(self.selection_money.text())>float(self.account_v)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_v-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set V = ? where Account_No = ?",(self.account_v,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="5"):
                if(float(self.selection_money.text())>float(self.account_wmt)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_wmt-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set WMT = ? where Account_No = ?",(self.account_wmt,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="6"):
                if(float(self.selection_money.text())>float(self.account_pg)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_pg-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set PG = ? where Account_No = ?",(self.account_pg,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="7"):
                if(float(self.selection_money.text())>float(self.account_jpm)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_jpm-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set JPM = ? where Account_No = ?",(self.account_jpm,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="8"):
                if(float(self.selection_money.text())>float(self.account_unh)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_unh-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set UNH = ? where Account_No = ?",(self.account_unh,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="9"):
                if(float(self.selection_money.text())>float(self.account_intc)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_intc-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set INTC = ? where Account_No = ?",(self.account_intc,login_account_number[0]))
                    self.connection.commit()
                    x=1
            elif(self.selection_number.text()=="10"):
                if(float(self.selection_money.text())>float(self.account_hd)):
                    self.error_text.setText("**You do not have sufficient stock\nbalance to make this transaction.**")
                else:
                    self.account_balance+=float(self.selection_money.text())
                    self.account_hd-=float(self.selection_money.text())
                    self.cursor.execute("update INVESTMENT set HD = ? where Account_No = ?",(self.account_hd,login_account_number[0]))
                    self.connection.commit()
                    x=1
            else:
                pass
            if(x==1):
                change_balance()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        def balance_control(total):
            if(self.account_balance<total):
                self.error_text.setText("**The balance is not enough.**")
            else:
                return 1

        def change_balance():
            self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(self.account_balance,login_account_number[0]))
            self.connection.commit()

        def buy_share():
            self.remove_right_widgets()
            self.selection_button = QtWidgets.QPushButton("Buy Share")
            self.selection_button.setStyleSheet("background-color:green;color:white;")
            self.selection_button.setFont(QtGui.QFont("arial",10))
            self.selection_button.setMinimumSize(300,35)
            self.selection.setText("\nEnter the number of the stock you want\nto buy:")
            self.selection_text.setText("\nHow many lots do you want to buy:")
            self.error_text.setText("")
            table = QtWidgets.QTableWidget()
            table.setRowCount(len(stock_list))
            table.setColumnCount(2)
            for i in range(len(stock_list)):
                table.setItem(i,0,QTableWidgetItem(stock_list[i][0]))
                table.setItem(i,1,QTableWidgetItem(str(stock_list[i][1])))
            columns = ['Share Name', 'Lot Price']
            table.setHorizontalHeaderLabels(columns)
            self.infobox.addStretch()
            self.infobox.addWidget(table)
            self.infobox.addWidget(self.selection)
            self.infobox.addWidget(self.selection_number)
            self.infobox.addWidget(self.selection_text)
            self.infobox.addWidget(self.selection_money)
            self.infobox.addWidget(self.selection_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()
            self.selection_button.clicked.connect(buy_shares_control)
        
        def sell_share():
            if(int(self.total_currency_balance)<0):
                self.error_text.setText("**You do not have any shares to sell.**")
            else:
                self.remove_right_widgets()
                self.selection_button = QtWidgets.QPushButton("Sell Share")
                self.selection_button.setStyleSheet("background-color:green;color:white;")
                self.selection_button.setFont(QtGui.QFont("arial",10))
                self.selection_button.setMinimumSize(300,35)
                self.selection.setText("\nEnter the number of the stock you want\nto sell:")
                self.selection_text.setText("\nHow much do you want to sell:")
                table = QtWidgets.QTableWidget()
                table.setRowCount(len(stock_list))
                table.setColumnCount(3)
                for i in range(len(stock_list)):
                    table.setItem(i,0,QTableWidgetItem(stock_list[i][0]))
                    table.setItem(i,1,QTableWidgetItem(str(stock_list[i][1])))
                self.get_info()
                table.setItem(0,2,QTableWidgetItem(str(round(self.account_msft,2))))
                table.setItem(1,2,QTableWidgetItem(str(round(self.account_aapl,2))))
                table.setItem(2,2,QTableWidgetItem(str(round(self.account_jnj,2))))
                table.setItem(3,2,QTableWidgetItem(str(round(self.account_v,2))))
                table.setItem(4,2,QTableWidgetItem(str(round(self.account_wmt,2))))
                table.setItem(5,2,QTableWidgetItem(str(round(self.account_pg,2))))
                table.setItem(6,2,QTableWidgetItem(str(round(self.account_jpm,2))))
                table.setItem(7,2,QTableWidgetItem(str(round(self.account_unh,2))))
                table.setItem(8,2,QTableWidgetItem(str(round(self.account_intc,2))))
                table.setItem(9,2,QTableWidgetItem(str(round(self.account_hd,2))))
                columns = ['Share Name', 'Lot Price','Current Balance']
                table.setHorizontalHeaderLabels(columns)
                self.infobox.addStretch()
                self.infobox.addWidget(table)
                self.infobox.addWidget(self.selection)
                self.infobox.addWidget(self.selection_number)
                self.infobox.addWidget(self.selection_text)
                self.infobox.addWidget(self.selection_money)
                self.infobox.addWidget(self.selection_button)
                self.infobox.addWidget(self.error_text)
                self.infobox.addStretch()
                self.selection_button.clicked.connect(sell_shares_control)

        self.remove_right_widgets()  
        self.selection = QtWidgets.QLabel()
        self.selection.setFont(QtGui.QFont("arial",13))
        self.selection.setStyleSheet("color:green;")
        self.selection_number = QtWidgets.QLineEdit()
        self.selection_number.setMinimumSize(280,35)
        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")
        self.selection_text = QtWidgets.QLabel()
        self.selection_text.setFont(QtGui.QFont("arial",13))
        self.selection_text.setStyleSheet("color:green;")
        self.selection_money = QtWidgets.QLineEdit()
        self.selection_money.setMinimumSize(280,35)

        self.buy_shares_button = QtWidgets.QPushButton("Buy Share")
        self.buy_shares_button.setStyleSheet("background-color:green;color:white;")
        self.buy_shares_button.setFont(QtGui.QFont("arial",10))
        self.buy_shares_button.setMinimumSize(300,35)
        self.sell_shares_button = QtWidgets.QPushButton("Sell Share")
        self.sell_shares_button.setStyleSheet("background-color:green;color:white;")
        self.sell_shares_button.setFont(QtGui.QFont("arial",10))
        self.sell_shares_button.setMinimumSize(300,35)
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(300,35)

        self.infobox.addStretch()
        self.infobox.addWidget(self.buy_shares_button)
        self.infobox.addWidget(self.sell_shares_button)
        self.infobox.addWidget(self.back_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addStretch()

        self.buy_shares_button.clicked.connect(buy_share)
        self.sell_shares_button.clicked.connect(sell_share)
        self.back_button.clicked.connect(self.add_right_account_widgets)

    def pay_bill(self):
        def phone_compare_screen():
            self.remove_right_widgets()
            billno_text = QtWidgets.QLabel()
            billno_text.setFont(QtGui.QFont("arial",13))
            billno_text.setStyleSheet("color:green;")
            billno_text.setText("Enter the phone number:")
            self.bill_no = QtWidgets.QLineEdit()
            self.bill_no.setMinimumSize(280,35)
            pay_bill_button = QtWidgets.QPushButton("Pay")
            pay_bill_button.setStyleSheet("background-color:green;color:white;")
            pay_bill_button.setFont(QtGui.QFont("arial",10))
            pay_bill_button.setMinimumSize(300,35)
            self.billamount = random.randint(50,150)

            self.infobox.addStretch()
            self.infobox.addWidget(billno_text)
            self.infobox.addWidget(self.bill_no)
            self.infobox.addWidget(pay_bill_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            pay_bill_button.clicked.connect(phone_compare)

        def social_security_compare_screen():
            self.remove_right_widgets()
            billno_text = QtWidgets.QLabel()
            billno_text.setFont(QtGui.QFont("arial",13))
            billno_text.setStyleSheet("color:green;")
            billno_text.setText("Enter social security number:")
            self.bill_no = QtWidgets.QLineEdit()
            self.bill_no.setMinimumSize(280,35)
            pay_bill_button = QtWidgets.QPushButton("Pay")
            pay_bill_button.setStyleSheet("background-color:green;color:white;")
            pay_bill_button.setFont(QtGui.QFont("arial",10))
            pay_bill_button.setMinimumSize(300,35)
            self.billamount = random.randint(80,200)

            self.infobox.addStretch()
            self.infobox.addWidget(billno_text)
            self.infobox.addWidget(self.bill_no)
            self.infobox.addWidget(pay_bill_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            pay_bill_button.clicked.connect(social_security_compare)

        def bill_compare_screen():
            self.remove_right_widgets()
            billno_text = QtWidgets.QLabel()
            billno_text.setFont(QtGui.QFont("arial",13))
            billno_text.setStyleSheet("color:green;")
            billno_text.setText("Enter the bill number:\n(Examp;A23212,G21232)\n")
            self.bill_no = QtWidgets.QLineEdit()
            self.bill_no.setMinimumSize(280,35)
            pay_bill_button = QtWidgets.QPushButton("Pay")
            pay_bill_button.setStyleSheet("background-color:green;color:white;")
            pay_bill_button.setFont(QtGui.QFont("arial",10))
            pay_bill_button.setMinimumSize(300,35)
            self.billamount = random.randint(50,150)

            self.infobox.addStretch()
            self.infobox.addWidget(billno_text)
            self.infobox.addWidget(self.bill_no)
            self.infobox.addWidget(pay_bill_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            pay_bill_button.clicked.connect(bill_compare)
    
        def phone_compare():
            x = self.number(self.bill_no)
            if(x==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1): 
                if(len(self.bill_no.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                elif(len(self.bill_no.text())!=10):
                    self.error_text.setText("**The phone number must be 10 digits.**")
                else:
                    is_it_paid()

        def social_security_compare():
            x = self.number(self.bill_no)
            if(x==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1): 
                if(len(self.bill_no.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                elif(len(self.bill_no.text())!=9):
                    self.error_text.setText("**SSN must consist of 9 digits.**")
                else:
                    is_it_paid()

        def bill_compare():
            bill = self.bill_no.text()
            a=0
            if(len(self.bill_no.text())==0):
                    self.error_text.setText("**Please enter a value.**")
            elif(len(self.bill_no.text())!=6):
                self.error_text.setText("**Bill number must consist of 6 characters.**")
            for i in range(1,len(bill)):
                if(bill[i]>="0" and bill[i]<="9"):
                    a+=1
                else:
                    self.error_text.setText("**Please enter the bill number correctly.**")
            if(a==(len(bill)-1)):
                if((bill[0]>="a" and bill[0]<="z") or (bill[0]>="A" and bill[0]<="Z")):
                    is_it_paid()

        def pay_screen():
            self.remove_right_widgets()
            self.error_text.setText("")
            bill_no = QtWidgets.QLabel()
            bill_no.setFont(QtGui.QFont("arial",13))
            bill_no.setStyleSheet("color:green;")
            bill_no.setText("Bill Number = {}\n".format(self.bill_no.text().upper())) 
            account_balance = QtWidgets.QLabel()
            account_balance.setFont(QtGui.QFont("arial",13))
            account_balance.setStyleSheet("color:green;")
            account_balance.setText("Account Balance = {} TL\n".format(self.account_balance)) 
            billamount = QtWidgets.QLabel()
            billamount.setFont(QtGui.QFont("arial",13))
            billamount.setStyleSheet("color:green;")
            billamount.setText("Bill Amount = {} TL\n".format(self.billamount))
            pay_bill_button = QtWidgets.QPushButton("Pay")
            pay_bill_button.setStyleSheet("background-color:green;color:white;")
            pay_bill_button.setFont(QtGui.QFont("arial",10))
            pay_bill_button.setMinimumSize(300,35)
            back_button = QtWidgets.QPushButton("Exit")
            back_button.setStyleSheet("background-color:green;color:white;")
            back_button.setFont(QtGui.QFont("arial",10))
            back_button.setMinimumSize(300,35)

            self.infobox.addStretch()
            self.infobox.addWidget(bill_no)
            self.infobox.addWidget(account_balance)
            self.infobox.addWidget(billamount)
            self.infobox.addWidget(pay_bill_button)
            self.infobox.addWidget(back_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            pay_bill_button.clicked.connect(pay)
            back_button.clicked.connect(self.add_right_account_widgets)

        def is_it_paid():
            bill = self.bill_no.text().upper()
            self.cursor.execute("select * from BILLS where Bill_No = ?",(bill,))
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                pay_screen()
            else:
                self.error_text.setText("This number has been paid before.")

        def pay():
            if(self.account_balance<self.billamount):
                self.error_text.setText("**There is not enough balance.**")
            else:
                bill = self.bill_no.text().upper()
                new_balance = self.account_balance - self.billamount
                self.cursor.execute("insert into BILLS VALUES(?)",(bill,))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        self.remove_right_widgets()
        self.phone = QtWidgets.QPushButton("Phone Bill")
        self.phone.setStyleSheet("background-color:green;color:white;")
        self.phone.setFont(QtGui.QFont("arial",10))
        self.phone.setMinimumSize(300,35)
        self.ethernet = QtWidgets.QPushButton("Ethernet Bill")
        self.ethernet.setStyleSheet("background-color:green;color:white;")
        self.ethernet.setFont(QtGui.QFont("arial",10))
        self.ethernet.setMinimumSize(300,35)
        self.gas = QtWidgets.QPushButton("Gas Bill")
        self.gas.setStyleSheet("background-color:green;color:white;")
        self.gas.setFont(QtGui.QFont("arial",10))
        self.gas.setMinimumSize(300,35)
        self.water = QtWidgets.QPushButton("Water Bill")
        self.water.setStyleSheet("background-color:green;color:white;")
        self.water.setFont(QtGui.QFont("arial",10))
        self.water.setMinimumSize(300,35)
        self.electric = QtWidgets.QPushButton("Electric Bill")
        self.electric.setStyleSheet("background-color:green;color:white;")
        self.electric.setFont(QtGui.QFont("arial",10))
        self.electric.setMinimumSize(300,35)
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(300,35)
        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")

        self.infobox.addStretch()
        self.infobox.addWidget(self.phone)
        self.infobox.addWidget(self.ethernet)
        self.infobox.addWidget(self.electric)
        self.infobox.addWidget(self.gas)
        self.infobox.addWidget(self.water)
        self.infobox.addWidget(self.back_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addStretch()

        self.phone.clicked.connect(phone_compare_screen)
        self.ethernet.clicked.connect(social_security_compare_screen)
        self.water.clicked.connect(bill_compare_screen)
        self.electric.clicked.connect(bill_compare_screen)
        self.gas.clicked.connect(bill_compare_screen)
        self.back_button.clicked.connect(self.add_right_account_widgets)

    def insurance(self):
        def social_security_compare_screen():
            self.remove_right_widgets()
            insurance_text = QtWidgets.QLabel()
            insurance_text.setFont(QtGui.QFont("arial",13))
            insurance_text.setStyleSheet("color:green;")
            insurance_text.setText("Enter social security number:")
            self.insuranceno = QtWidgets.QLineEdit()
            self.insuranceno.setMinimumSize(280,35)
            insurance_pay_button = QtWidgets.QPushButton("Pay")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            self.insurance_amount = random.randint(500,1000)

            self.infobox.addStretch()
            self.infobox.addWidget(insurance_text)
            self.infobox.addWidget(self.insuranceno)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(social_security_compare)

        def plate_compare_screen():
            self.remove_right_widgets()
            insurance_text = QtWidgets.QLabel()
            insurance_text.setFont(QtGui.QFont("arial",13))
            insurance_text.setStyleSheet("color:green;")
            insurance_text.setText("Enter the plate:")
            self.plate = QtWidgets.QLineEdit()
            self.plate.setMinimumSize(0,35)
            
            insurance_pay_button = QtWidgets.QPushButton("Compare Plate")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            self.insurance_amount = random.randint(800,2000)

            self.infobox.addStretch()
            self.infobox.addWidget(insurance_text)
            self.infobox.addWidget(self.plate)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(plate_compare)
    
        def address_compare_screen():
            self.remove_right_widgets()
            state_text = QtWidgets.QLabel()
            state_text.setFont(QtGui.QFont("arial",13))
            state_text.setStyleSheet("color:green;")
            state_text.setText("Enter State Full:")
            city_text = QtWidgets.QLabel()
            city_text.setFont(QtGui.QFont("arial",13))
            city_text.setStyleSheet("color:green;")
            city_text.setText("\nEnter City:")
            street_text = QtWidgets.QLabel()
            street_text.setFont(QtGui.QFont("arial",13))
            street_text.setStyleSheet("color:green;")
            street_text.setText("\nEnter Street:")

            self.state = QtWidgets.QLineEdit()
            self.state.setMinimumSize(280,35)
            self.city = QtWidgets.QLineEdit()
            self.city.setMinimumSize(280,35)
            self.street = QtWidgets.QLineEdit()
            self.street.setMinimumSize(280,35)
            insurance_pay_button = QtWidgets.QPushButton("Pay")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            self.insurance_amount = random.randint(1000,2000)

            self.infobox.addStretch()
            self.infobox.addWidget(state_text)
            self.infobox.addWidget(self.state)
            self.infobox.addWidget(city_text)
            self.infobox.addWidget(self.city)
            self.infobox.addWidget(street_text)
            self.infobox.addWidget(self.street)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(address_compare)

        def social_security_compare():
            x = self.number(self.insuranceno)
            if(x==0):
                self.error_text.setText("**Please enter numbers only.**")
            elif(x==2):
                self.error_text.setText("**Please enter a positive number.**")
            elif(x==1): 
                if(len(self.insuranceno.text())==0):
                    self.error_text.setText("**Please enter a value.**")
                elif(len(self.insuranceno.text())!=9):
                    self.error_text.setText("**SSN must consist of 9 digits.**")
                else:
                    is_it_paid()

        def address_compare():
            a=0
            b=0
            c=0
            if(len(self.state.text())==0 or len(self.city.text())==0 or len(self.street.text())==0):
                self.error_text.setText("**Please fill in all the blanks.**")
            else:
                for i in self.state.text():
                    if(i>="0" and i<="9"):
                        a=0
                        self.error_text.setText("**The state section should not contain\nnumbers..**")
                    elif(i==" "):
                        self.error_text.setText("**There should be no spaces in the state\nsection.**")
                    else:
                        a+=1

                for j in self.city.text():
                    if(j>="0" and j<="9"):
                        b=0
                        self.error_text.setText("**The city section should not contain\nnumbers.**")
                    else:
                        b+=1

                for z in self.street.text():
                    if(z>="0" and z<="9"):
                        c=0
                        self.error_text.setText("**The street section should not contain\nnumbers.**")
                    else:
                        c+=1

                if(a == len(self.state.text()) and b == len(self.city.text()) and c == len(self.street.text())):
                    self.address = str(str(self.state.text())[:3]+"." + str(self.city.text())[:3]+"." + str(self.street.text())[:3]+".").upper()    
                    is_address_paid()
                
        def plate_compare():
            if(len(self.plate.text())==0):
                self.error_text.setText("**Please fill in all the blanks.**")
            else:
                is_plate_paid()

        def pay_screen():
            self.remove_right_widgets()
            self.error_text.setText("")
            insuranceno = QtWidgets.QLabel()
            insuranceno.setFont(QtGui.QFont("arial",13))
            insuranceno.setStyleSheet("color:green;")
            insuranceno.setText("Insurance Number = {}\n".format(self.insuranceno.text())) 
            account_balance = QtWidgets.QLabel()
            account_balance.setFont(QtGui.QFont("arial",13))
            account_balance.setStyleSheet("color:green;")
            account_balance.setText("Account Balance = {} TL\n".format(self.account_balance)) 
            insurance_amount = QtWidgets.QLabel()
            insurance_amount.setFont(QtGui.QFont("arial",13))
            insurance_amount.setStyleSheet("color:green;")
            insurance_amount.setText("Insurance Amount = {} TL\n".format(self.insurance_amount))
            insurance_pay_button = QtWidgets.QPushButton("Pay")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            back_button = QtWidgets.QPushButton("Exit")
            back_button.setStyleSheet("background-color:green;color:white;")
            back_button.setFont(QtGui.QFont("arial",10))
            back_button.setMinimumSize(300,35)

            self.infobox.addStretch()
            self.infobox.addWidget(insuranceno)
            self.infobox.addWidget(account_balance)
            self.infobox.addWidget(insurance_amount)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(back_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(pay)
            back_button.clicked.connect(self.add_right_account_widgets)

        def plate_pay_screen():
            self.remove_right_widgets()
            self.error_text.setText("")
            insuranceno = QtWidgets.QLabel()
            insuranceno.setFont(QtGui.QFont("arial",13))
            insuranceno.setStyleSheet("color:green;")
            insuranceno.setText("Plate = {}\n".format(self.plate.text())) 
            account_balance = QtWidgets.QLabel()
            account_balance.setFont(QtGui.QFont("arial",13))
            account_balance.setStyleSheet("color:green;")
            account_balance.setText("Account Balance = {} TL\n".format(self.account_balance)) 
            insurance_amount = QtWidgets.QLabel()
            insurance_amount.setFont(QtGui.QFont("arial",13))
            insurance_amount.setStyleSheet("color:green;")
            insurance_amount.setText("Insurance Amount = {} TL\n".format(self.insurance_amount))
            insurance_pay_button = QtWidgets.QPushButton("Pay")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            back_button = QtWidgets.QPushButton("Exit")
            back_button.setStyleSheet("background-color:green;color:white;")
            back_button.setFont(QtGui.QFont("arial",10))
            back_button.setMinimumSize(300,35)
            self.infobox.addStretch()
            self.infobox.addWidget(insuranceno)
            self.infobox.addWidget(account_balance)
            self.infobox.addWidget(insurance_amount)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(back_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(plate_pay)
            back_button.clicked.connect(self.add_right_account_widgets)

        def address_pay_screen():
            self.remove_right_widgets()
            self.error_text.setText("")
            insuranceno = QtWidgets.QLabel()
            insuranceno.setFont(QtGui.QFont("arial",13))
            insuranceno.setStyleSheet("color:green;")
            insuranceno.setText("Address = {}\n".format(self.address)) 
            account_balance = QtWidgets.QLabel()
            account_balance.setFont(QtGui.QFont("arial",13))
            account_balance.setStyleSheet("color:green;")
            account_balance.setText("Account Balance = {} TL\n".format(self.account_balance)) 
            insurance_amount = QtWidgets.QLabel()
            insurance_amount.setFont(QtGui.QFont("arial",13))
            insurance_amount.setStyleSheet("color:green;")
            insurance_amount.setText("Insurance Amount = {} TL\n".format(self.insurance_amount))
            insurance_pay_button = QtWidgets.QPushButton("Pay")
            insurance_pay_button.setStyleSheet("background-color:green;color:white;")
            insurance_pay_button.setFont(QtGui.QFont("arial",10))
            insurance_pay_button.setMinimumSize(300,35)
            back_button = QtWidgets.QPushButton("exit")
            back_button.setStyleSheet("background-color:green;color:white;")
            back_button.setFont(QtGui.QFont("arial",10))
            back_button.setMinimumSize(300,35)
            self.infobox.addStretch()
            self.infobox.addWidget(insuranceno)
            self.infobox.addWidget(account_balance)
            self.infobox.addWidget(insurance_amount)
            self.infobox.addWidget(insurance_pay_button)
            self.infobox.addWidget(back_button)
            self.infobox.addWidget(self.error_text)
            self.infobox.addStretch()

            insurance_pay_button.clicked.connect(address_pay)
            back_button.clicked.connect(self.add_right_account_widgets)

        def is_it_paid():
            insurance = self.insuranceno.text().upper()
            self.cursor.execute("select * from INSURANCES where Insurance_No = ?",(insurance,))
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                pay_screen()
            else:
                self.error_text.setText("This number has been paid before.")
        
        def is_plate_paid():
            self.cursor.execute("select * from INSURANCES where Insurance_No = ?",(self.plate.text(),))
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                plate_pay_screen()
            else:
                self.error_text.setText("This plate has already been paid.")

        def is_address_paid():
            self.cursor.execute("select * from INSURANCES where Insurance_No = ?",(self.address,))
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                address_pay_screen()
            else:
                self.error_text.setText("This address has already been paid.")

        def pay():
            if(self.account_balance<self.insurance_amount):
                self.error_text.setText("**There is not enough balance.**")
            else:
                amount = self.insuranceno.text().upper()
                new_balance = self.account_balance - self.insurance_amount
                self.cursor.execute("insert into INSURANCES VALUES(?)",(amount,))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()
        
        def plate_pay():
            if(self.account_balance<self.insurance_amount):
                self.error_text.setText("**There is not enough balance.**")
            else:
                new_balance = self.account_balance - self.insurance_amount
                self.cursor.execute("insert into INSURANCES VALUES(?)",(self.plate.text(),))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        def address_pay():
            if(self.account_balance<self.insurance_amount):
                self.error_text.setText("**There is not enough balance.**")
            else:
                new_balance = self.account_balance - self.insurance_amount
                self.cursor.execute("insert into INSURANCES VALUES(?)",(self.address,))
                self.connection.commit()
                self.cursor.execute("update BANK_CUSTOMERS set Balance = ? where Account_No = ?",(new_balance,login_account_number[0]))
                self.connection.commit()
                self.remove_right_widgets()
                self.add_right_account_widgets()

        self.remove_right_widgets()
        self.vehicle = QtWidgets.QPushButton("Vehicle Insurance")
        self.vehicle.setStyleSheet("background-color:green;color:white;")
        self.vehicle.setFont(QtGui.QFont("arial",10))
        self.vehicle.setMinimumSize(300,35)
        self.house = QtWidgets.QPushButton("House Insurance")
        self.house.setStyleSheet("background-color:green;color:white;")
        self.house.setFont(QtGui.QFont("arial",10))
        self.house.setMinimumSize(300,35)
        self.health = QtWidgets.QPushButton("Health Insurance")
        self.health.setStyleSheet("background-color:green;color:white;")
        self.health.setFont(QtGui.QFont("arial",10))
        self.health.setMinimumSize(300,35)
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(300,35)
        self.error_text = QtWidgets.QLabel()
        self.error_text.setFont(QtGui.QFont("arial",11))
        self.error_text.setStyleSheet("color:red;")

        self.infobox.addStretch()
        self.infobox.addWidget(self.vehicle)
        self.infobox.addWidget(self.house)
        self.infobox.addWidget(self.health)
        self.infobox.addWidget(self.back_button)
        self.infobox.addWidget(self.error_text)
        self.infobox.addStretch()

        self.vehicle.clicked.connect(plate_compare_screen)
        self.health.clicked.connect(social_security_compare_screen)
        self.house.clicked.connect(address_compare_screen)
        self.back_button.clicked.connect(self.add_right_account_widgets)

    def exit(self):
        login_account_number.clear()
        self.bank = First_Page()
        self.close()
        self.bank.show()

    def init_login_page(self):
        self.get_info()
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if(len(str(minute))==1):
            minute = "0" + str(minute)
        if(len(str(hour))==1):
            hour = "0"+str(hour)
        day = datetime.strftime(datetime.now(),"%D\n%A\n")
        day = day+str(hour)+":"+str(minute)
        self.date = QtWidgets.QLabel()
        self.date.setText(day)
        self.date.setFont(QtGui.QFont("arial",13))
        self.date.setStyleSheet("color:green")

        self.account_info_button = QtWidgets.QPushButton("Account Info")
        self.account_info_button.setStyleSheet("background-color:green;color:white;")
        self.account_info_button.setFont(QtGui.QFont("arial",10))
        self.account_info_button.setMinimumSize(300,35)

        self.deposit_money_button = QtWidgets.QPushButton("Deposit Money")
        self.deposit_money_button.setStyleSheet("background-color:green;color:white;")
        self.deposit_money_button.setFont(QtGui.QFont("arial",10))
        self.deposit_money_button.setMinimumSize(300,35)

        self.withdraw_money_button = QtWidgets.QPushButton("Withdraw Money")
        self.withdraw_money_button.setStyleSheet("background-color:green;color:white;")
        self.withdraw_money_button.setFont(QtGui.QFont("arial",10))
        self.withdraw_money_button.setMinimumSize(300,35)

        self.loans_button = QtWidgets.QPushButton("Loans")
        self.loans_button.setStyleSheet("background-color:green;color:white;")
        self.loans_button.setFont(QtGui.QFont("arial",10))
        self.loans_button.setMinimumSize(300,35)

        self.debt_payment_button = QtWidgets.QPushButton("Debt Payment")
        self.debt_payment_button.setStyleSheet("background-color:green;color:white;")
        self.debt_payment_button.setFont(QtGui.QFont("arial",10))
        self.debt_payment_button.setMinimumSize(300,35)

        self.money_transfer_button = QtWidgets.QPushButton("Money Transfer")
        self.money_transfer_button.setStyleSheet("background-color:green;color:white;")
        self.money_transfer_button.setFont(QtGui.QFont("arial",10))
        self.money_transfer_button.setMinimumSize(300,35)

        self.foreign_currency_button = QtWidgets.QPushButton("Foreign Currency")
        self.foreign_currency_button.setStyleSheet("background-color:green;color:white;")
        self.foreign_currency_button.setFont(QtGui.QFont("arial",10))
        self.foreign_currency_button.setMinimumSize(300,35)

        self.investment_button = QtWidgets.QPushButton("Investment")
        self.investment_button.setStyleSheet("background-color:green;color:white;")
        self.investment_button.setFont(QtGui.QFont("arial",10))
        self.investment_button.setMinimumSize(300,35)

        self.bill_button = QtWidgets.QPushButton("Pay Bill")
        self.bill_button.setStyleSheet("background-color:green;color:white;")
        self.bill_button.setFont(QtGui.QFont("arial",10))
        self.bill_button.setMinimumSize(300,35)

        self.insurance_button = QtWidgets.QPushButton("Insurances")
        self.insurance_button.setStyleSheet("background-color:green;color:white;")
        self.insurance_button.setFont(QtGui.QFont("arial",10))
        self.insurance_button.setMinimumSize(300,35)

        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.setStyleSheet("background-color:green;color:white;")
        self.exit_button.setFont(QtGui.QFont("arial",10))
        self.exit_button.setMinimumSize(300,35)

        self.uplayoutSpacer = QtWidgets.QSpacerItem(0,5)

        self.balance = QtWidgets.QLabel()
        self.balance.setText("Balance: $"+str(self.account_balance))
        self.balance.setFont(QtGui.QFont("arial",20))
        self.debt = QtWidgets.QLabel()
        self.debt.setText("Debt: $"+str(self.account_debt))
        self.debt.setFont(QtGui.QFont("arial",20))
        self.currency = QtWidgets.QLabel()
        self.currency.setText("Currency Balance: $"+str(self.total_currency_balance))
        self.currency.setFont(QtGui.QFont("arial",20))
        self.investment = QtWidgets.QLabel()
        self.investment.setText("Investment Balance: $"+str(self.total_investment_balance))
        self.investment.setFont(QtGui.QFont("arial",20))
        self.error= QtWidgets.QLabel()
        self.error.setFont(QtGui.QFont("arial",11))
        self.error.setStyleSheet("color:red;")

        vboxislemler = QtWidgets.QVBoxLayout()
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.account_info_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.deposit_money_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.withdraw_money_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.loans_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.debt_payment_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.money_transfer_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.foreign_currency_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.investment_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.bill_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.insurance_button)
        vboxislemler.addItem(self.uplayoutSpacer)
        vboxislemler.addWidget(self.exit_button)
        vboxislemler.addStretch()

        datebox =QtWidgets.QVBoxLayout()
        datebox.addWidget(self.date)
        datebox.addStretch()

        self.infobox = QtWidgets.QVBoxLayout()
        self.infobox.addStretch()
        self.infobox.addWidget(self.balance)
        self.infobox.addWidget(self.debt)
        self.infobox.addWidget(self.currency)
        self.infobox.addWidget(self.investment)
        self.infobox.addWidget(self.error)
        self.infobox.addStretch()

        rightvbox = QtWidgets.QHBoxLayout()
        rightvbox.addStretch()
        rightvbox.addLayout(self.infobox)
        rightvbox.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(vboxislemler)
        h_box.addStretch()
        h_box.addLayout(rightvbox)
        h_box.addStretch()
        h_box.addLayout(datebox)

        self.setFixedSize(900,500)
        self.setLayout(h_box)
        
        self.account_info_button.clicked.connect(self.account_info)
        self.deposit_money_button.clicked.connect(self.deposit_money)
        self.withdraw_money_button.clicked.connect(self.withdraw_money)
        self.loans_button.clicked.connect(self.loans)
        self.debt_payment_button.clicked.connect(self.debt_payment)
        self.money_transfer_button.clicked.connect(self.money_transfer)
        self.foreign_currency_button.clicked.connect(self.foreign_currency)
        self.investment_button.clicked.connect(self.investment_)
        self.bill_button.clicked.connect(self.pay_bill)
        self.insurance_button.clicked.connect(self.insurance)
        self.exit_button.clicked.connect(self.exit)
        
class Login_Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_giris()
        self.setWindowTitle("Alize Bank")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        
    def compare(self,name,password):
        try:
            self.connection = sqlite3.connect("bankdatabase.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from BANK_CUSTOMERS")
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                return 0
        except:
            return 0
        try:
            self.connection = sqlite3.connect("bankdatabase.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from BANK_CUSTOMERS where Name_Surname = ?",(str(name).upper(),))
            list1 = self.cursor.fetchall()
            if(len(list1)==0):
                return 3
        except:
            return 0
    
        login_account_number.append(list1[0][5])
        if(len(list1)==0):
            return 3
        elif(list1[0][1]!=password):
            return 2
        else:
            return 1
        
    def login_successful(self,):
        self.login1 = Main_Menu()
        self.close()
        self.login1.show()

    def name_query(self,isim):
        a=0
        b=0
        for i in list(self.login_name.text()):
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**İsim-Soyisim'de rakam veya özel karakter \nbulunamaz.**"
        for i in list(self.login_name.text()):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Lütfen isim ve soyisminizin arasında boşluk\n olacak şekilde yazınız.**"
        if(len(self.login_name.text())<6):
            return"**Lütfen isminizi doğru şekilde giriniz.**"
        return 1

    def password_query(self,password):
        a=0
        if(len(password)<4 or len(password)>6):
            return "**Şifre 4-6 adet rakamdan oluşmalıdır.**"
        for i in list(password):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(password)):
            return "**Şifre sadece rakamlardan oluşmalıdır.**"
        return 1  

    def login(self):
        b = self.password_query(self.password.text())
        if(b==1):
            pass
        else:
            self.error.setText(b)  

        a = self.name_query(self.login_name.text())
        if(a==1):
            pass
        else:
            self.error.setText(a)  

        if(len(self.login_name.text())==0 or len(self.password.text())==0):
                self.error.setText("**Please fill in the fields indicated with '*'.**")

        if(a==1 and b==1):
            x = self.compare(self.login_name.text(),self.password.text())
            if(x==0):
                self.error.setText("**No registration has been made yet.**")
            elif(x==1):
                self.error.setText("**Successful.**")
                self.login_successful()
            elif(x==2):
                self.error.setText("**This name does not match the password.**")
            else:
                self.error.setText("**There is no bank customer with this name.**")

    def exit(self):
        self.bank = First_Page()
        self.close()
        self.bank.show()

    def go_register(self):
        self.register = Sign_Up_Page()
        self.close()
        self.register.show()

    def init_giris(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if(len(str(minute))==1):
            minute = "0" + str(minute)
        if(len(str(hour))==1):
            hour = "0"+str(hour)
        day = datetime.strftime(datetime.now(),"%D\n%A\n")
        day = day+str(hour)+":"+str(minute)
        self.date = QtWidgets.QLabel()
        self.date.setText(day)
        self.date.setFont(QtGui.QFont("arial",15))
        self.date.setStyleSheet("color:green")

        self.warning = QtWidgets.QLabel()
        self.warning.setText("Please fill in the fields indicated with '*'\n**Please do not use special characters.")
        self.warning.setStyleSheet("color:red;")

        self.error = QtWidgets.QLabel()
        self.error.setStyleSheet("color:red;")
        self.error.setFont(QtGui.QFont("arial",10))

        self.login_name = QtWidgets.QLineEdit()
        self.login_name.setMinimumSize(300,30)
        self.login_name_text = QtWidgets.QLabel()
        self.login_name_text.setText("Name*")
        self.login_name_text.setStyleSheet("color:green")
        self.login_name_text.setFont(QtGui.QFont("arial",14))
        self.password = QtWidgets.QLineEdit()
        self.password.setMinimumSize(300,30)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text = QtWidgets.QLabel()
        self.password_text.setText("Password*")
        self.password_text.setStyleSheet("color:green")
        self.password_text.setFont(QtGui.QFont("arial",14))

        self.giris_buton = QtWidgets.QPushButton("Login")
        self.giris_buton.setStyleSheet("background-color:green;color:white;")
        self.giris_buton.setFont(QtGui.QFont("arial",10))
        self.giris_buton.setMinimumSize(80,35)
        
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(80,35)

        self.register_button = QtWidgets.QPushButton("New Register")
        self.register_button.setStyleSheet("background-color:green;color:white;")
        self.register_button.setFont(QtGui.QFont("arial",10))
        self.register_button.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(70,0)
        self.space = QtWidgets.QLabel()
        self.space.setText(" ")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.login_name_text)
        v_box.addWidget(self.login_name)
        v_box.addWidget(self.password_text)
        v_box.addWidget(self.password)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.register_button)
        hh_box.addWidget(self.back_button)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.date)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.warning)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.space)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.giris_buton)
        vvv_box.addWidget(self.error)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.giris_buton.clicked.connect(self.login)
        self.back_button.clicked.connect(self.exit)
        self.register_button.clicked.connect(self.go_register)

        self.setFixedSize(900,500)
        self.setLayout(h_box)

class Sign_Up_Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_register()
        self.setWindowTitle("Alize Bank")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        self.make_connection()

    def make_connection(self):
        self.connection = sqlite3.connect("bankdatabase.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BANK_CUSTOMERS(Name_Surname TEXT,Password TEXT,Phone TEXT,Balance FLOAT,Debt FLOAT,Account_No INT)")
        self.connection.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS CURRENCY(Account_No INT,TL FLOAT,Euro FLOAT,Pound FLOAT,Swiss_Franc FLOAT,Canadian_Dollar FLOAT,Russian_Rouble FLOAT,Swedish_Krona FLOAT,Japan_Yen FLOAT,Kuwaiti_Dinar FLOAT,China_Yuan FLOAT)")
        self.connection.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS INVESTMENT(Account_No INT,MSFT FLOAT,AAPL FLOAT,JNJ FLOAT,V FLOAT,WMT FLOAT,PG FLOAT,JPM FLOAT,UNH FLOAT,INTC FLOAT,HD FLOAT)")
        self.connection.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS BILLS(Bill_No TEXT)")
        self.connection.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS INSURANCES(Insurance_No TEXT)")
        self.connection.commit()

    def save_database(self,name,password,phone):
        account_no = random.randint(10000,100000)
        self.cursor.execute("insert into BANK_CUSTOMERS VALUES(?,?,?,?,?,?)",(name,password,phone,0.0,0.0,account_no))
        self.connection.commit()
        self.cursor.execute("insert into CURRENCY VALUES(?,?,?,?,?,?,?,?,?,?,?)",(account_no,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))
        self.connection.commit()
        self.cursor.execute("insert into INVESTMENT VALUES(?,?,?,?,?,?,?,?,?,?,?)",(account_no,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0))
        self.connection.commit()

    def compare(self,phone):
        a=0
        self.cursor.execute("select Phone from BANK_CUSTOMERS")
        list1 = self.cursor.fetchall()
        for i in list1:
            for y in i:
                if(y == phone):
                    a+=1
        if(a==0):
            return 1
        else:
            return 0

    def name_query(self,register_name):
        a=0
        b=0
        for i in list(self.register_name.text()):
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**No digits or special characters can be found\nin the name.**"
        for i in list(self.register_name.text()):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Please write without a space between your\nname and surname.**"
        if(len(self.register_name.text())<5):
            return"**Please enter your name correctly.**"
        return 1

    def password_query(self,password,re_password):
        a=0
        b=0
        if(password != re_password):
            return "**Passwords do not match.**"
        elif(len(password)<4 or len(password)>6 or len(re_password)<4 or len(re_password)>6):
            return "**The password should consist of 4-6 numbers.**"
        for i in list(password):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(password)):
            return "**The password should only contain numbers.**"
        for i in list(re_password):
            if(i>="0" and i<="9"):
                b+=1
            else:
                b=0
        if(b != len(password)):
            return "**The password should only contain numbers.**"
        return 1    
    
    def phone_query(self,phone):
        a=0
        b=0
        if(len(phone)!=0):
            pass
        for i in list(phone):
            if (i ==" "):
                b+=1
            else:
                pass
        if(b!=0):
            return "**Please write in the phone number without any\nspaces.**"
        for i in list(phone):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(phone)):
            return "**The phone number should only contain\ndigits.**"  
        return 1
        
    def register(self):     
        c=self.phone_query(self.phone.text())
        if(c==1):
            pass
        else:
            self.error.setText(c)

        b=self.password_query(self.password.text(),self.re_password.text())
        if(b==1):
            pass
        else:
            self.error.setText(b)

        a = self.name_query(self.register_name.text())
        if(a==1):
            pass
        else:
            self.error.setText(a)

        if(len(self.register_name.text())==0 or len(self.password.text())==0 or len(self.re_password.text())==0 or len(self.phone.text())==0):
            self.error.setText("**Please fill in the fields indicated with '*'.**")
             
        if(a==1 and b==1 and c==1):
            islem =self.compare(self.phone.text())
            if islem ==1:
                self.error.setText("**Your registration has been completed\nsuccessfully.**")
                self.save_database(self.register_name.text().upper(),self.password.text(),self.phone.text())
            else:
                self.error.setText("**This phone number has already been registered.**\nPlease try again.")   
       
    def exit(self):
        self.banka = First_Page()
        self.close()
        self.banka.show()

    def init_register(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if(len(str(minute))==1):
            minute = "0" + str(minute)
        if(len(str(hour))==1):
            hour = "0"+str(hour)
        day = datetime.strftime(datetime.now(),"%D\n%A\n")
        day = day+str(hour)+":"+str(minute)
        self.date = QtWidgets.QLabel()
        self.date.setText(day)
        self.date.setFont(QtGui.QFont("arial",15))
        self.date.setStyleSheet("color:green")

        self.warning = QtWidgets.QLabel()
        self.warning.setText("Please fill in the fields indicated with '*'\n**Please do not use special characters.\n**The password should consist of 4-6 numbers.")
        self.warning.setStyleSheet("color:red;")

        self.error= QtWidgets.QLabel()
        self.error.setStyleSheet("color:red;")
        self.error.setFont(QtGui.QFont("arial",10))

        self.register_name = QtWidgets.QLineEdit()
        self.register_name.setMinimumSize(300,30)
        self.register_name_text = QtWidgets.QLabel()
        self.register_name_text.setText("Name*")
        self.register_name_text.setStyleSheet("color:green")
        self.register_name_text.setFont(QtGui.QFont("arial",14))
        self.password = QtWidgets.QLineEdit()
        self.password.setMinimumSize(300,30)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text = QtWidgets.QLabel()
        self.password_text.setText("Password*")
        self.password_text.setStyleSheet("color:green")
        self.password_text.setFont(QtGui.QFont("arial",14))
        self.re_password = QtWidgets.QLineEdit()
        self.re_password.setMinimumSize(300,30)
        self.re_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.re_password_text = QtWidgets.QLabel()
        self.re_password_text.setText("Re-Password*")
        self.re_password_text.setStyleSheet("color:green")
        self.re_password_text.setFont(QtGui.QFont("arial",14))
        self.phone = QtWidgets.QLineEdit()
        self.phone.setMinimumSize(300,30)
        self.phone_text = QtWidgets.QLabel()
        self.phone_text.setText("Phone Number*")
        self.phone_text.setStyleSheet("color:green")
        self.phone_text.setFont(QtGui.QFont("arial",14))

        self.register_button = QtWidgets.QPushButton("Register")
        self.register_button.setStyleSheet("background-color:green;color:white;")
        self.register_button.setFont(QtGui.QFont("arial",10))
        self.register_button.setMinimumSize(80,35)
        
        self.back_button = QtWidgets.QPushButton("Back")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(45,0)
        self.space = QtWidgets.QLabel()
        self.space.setText(" ")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.register_name_text)
        v_box.addWidget(self.register_name)
        v_box.addWidget(self.password_text)
        v_box.addWidget(self.password)
        v_box.addWidget(self.re_password_text)
        v_box.addWidget(self.re_password)
        v_box.addWidget(self.phone_text)
        v_box.addWidget(self.phone)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.register_button)
        hh_box.addWidget(self.back_button)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.date)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.warning)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.space)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.error)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.register_button.clicked.connect(self.register)
        self.back_button.clicked.connect(self.exit)

        self.setFixedSize(900,500)
        self.setLayout(h_box)

class Unregister_Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_unregister()
        self.setWindowTitle("Alize Bank")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
          
    def exit(self):
        self.bank = First_Page()
        self.close()
        self.bank.show()

    def unregister_success(self):
        self.cursor.execute("delete from BANK_CUSTOMERS where Account_No = ?",(unregister_account_number[0],))
        self.connection.commit()
        self.cursor.execute("delete from CURRENCY where Account_No = ?",(unregister_account_number[0],))
        self.connection.commit()
        self.cursor.execute("delete from INVESTMENT where Account_No = ?",(unregister_account_number[0],))
        self.connection.commit()
        unregister_account_number.clear()
        return 1

    def compare_information(self,name,password):
        try:
            self.connection = sqlite3.connect("bankdatabase.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from BANK_CUSTOMERS")
            list2 = self.cursor.fetchall()
            if(len(list2)==0):
                return 0
        except:
            return 0
        try:
            self.connection = sqlite3.connect("bankdatabase.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("select * from BANK_CUSTOMERS where Name_Surname = ?",(str(name).upper(),))
        except:
            return 0
        list1 = self.cursor.fetchall()
        try:
            unregister_account_number.append(list1[0][5])
        except:
            pass
        if(len(list1)==0):
            return 3
        elif(list1[0][1]!=password):
            return 2
        else:
            return self.unregister_success()
        
    def name_query(self,name):
        a=0
        b=0
        for i in name:
            if ((i >="a" and i<="z") or (i >="A" and i<="Z") or (i == " ")):
                a+=1
            else:
                return "**No digits or special characters can be found\nin the name-surname.**"
        for i in name:
            if (i ==" "):
                b+=1
            else:
                pass
        if(b==0):
            return "**Please write without a space between your\nname and surname.**"
        if(len(name)<5):
            return"**Please enter your name correctly.**"
        return 1

    def password_query(self,password,re_password):
        a=0
        b=0
        if(password != re_password):
            return "**Passwords do not match.**"
        elif(len(password)<4 or len(password)>6 or len(re_password)<4 or len(re_password)>6):
            return "**The password should consist of 4-6 numbers.**"
        for i in list(password):
            if(i>="0" and i<="9"):
                a+=1
            else:
                a=0
        if(a != len(password)):
            return "**The password should only contain numbers.**"
        for i in list(re_password):
            if(i>="0" and i<="9"):
                b+=1
            else:
                b=0
        if(b != len(password)):
            return "**The password should only contain numbers.**"
        return 1      

    def unregister(self):
        b = self.password_query(self.password.text(),self.re_password.text())
        if(b==1):
            pass
        else:
            self.error.setText(b)  

        a = self.name_query(self.login_name.text())
        if(a==1):
            pass
        else:
            self.error.setText(a)

        if(len(self.login_name.text())==0 or len(self.password.text())==0 or len(self.re_password.text())==0):
                self.error.setText("**Please fill in the fields indicated with '*'.**")

        if(a==1 and b==1):
            x = self.compare_information(self.login_name.text(),self.password.text())
            if(x==0):
                self.error.setText("**No registration has yet been made.**")
            elif(x==1):
                self.error.setText("**Deregistration has been successfully completed.**")
            elif(x==2):
                self.error.setText("**This name does not match the password.**")
            else:
                self.error.setText("**There is no bank customer with this name.**")

    def init_unregister(self):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if(len(str(minute))==1):
            minute = "0" + str(minute)
        if(len(str(hour))==1):
            hour = "0"+str(hour)
        day = datetime.strftime(datetime.now(),"%D\n%A\n")
        day = day+str(hour)+":"+str(minute)
        self.date = QtWidgets.QLabel()
        self.date.setText(day)
        self.date.setFont(QtGui.QFont("arial",15))
        self.date.setStyleSheet("color:green")

        self.warning = QtWidgets.QLabel()
        self.warning.setText("Lütfen '*' ile gösterilen alanları doldurunuz.\n**Lütfen özel karakter kullanmayınız.")
        self.warning.setStyleSheet("color:red;")

        self.error= QtWidgets.QLabel()
        self.error.setStyleSheet("color:red;")
        self.error.setFont(QtGui.QFont("arial",10))

        self.login_name = QtWidgets.QLineEdit()
        self.login_name.setMinimumSize(300,30)
        self.login_name_text = QtWidgets.QLabel()
        self.login_name_text.setText("Name Surname*")
        self.login_name_text.setStyleSheet("color:green")
        self.login_name_text.setFont(QtGui.QFont("arial",14))
        self.password = QtWidgets.QLineEdit()
        self.password.setMinimumSize(300,30)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_text = QtWidgets.QLabel()
        self.password_text.setText("Password*")
        self.password_text.setStyleSheet("color:green")
        self.password_text.setFont(QtGui.QFont("arial",14))
        self.re_password = QtWidgets.QLineEdit()
        self.re_password.setMinimumSize(300,30)
        self.re_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.re_password_text = QtWidgets.QLabel()
        self.re_password_text.setText("Re-Password*")
        self.re_password_text.setStyleSheet("color:green")
        self.re_password_text.setFont(QtGui.QFont("arial",14))
        
        self.back_button = QtWidgets.QPushButton("Exit")
        self.back_button.setStyleSheet("background-color:green;color:white;")
        self.back_button.setFont(QtGui.QFont("arial",10))
        self.back_button.setMinimumSize(80,35)

        self.unregister_buton = QtWidgets.QPushButton("Unregister")
        self.unregister_buton.setStyleSheet("background-color:green;color:white;")
        self.unregister_buton.setFont(QtGui.QFont("arial",10))
        self.unregister_buton.setMinimumSize(80,35)

        layoutSpacer = QtWidgets.QSpacerItem(70,0)
        self.space = QtWidgets.QLabel()
        self.space.setText(" ")

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.login_name_text)
        v_box.addWidget(self.login_name)
        v_box.addWidget(self.password_text)
        v_box.addWidget(self.password)
        v_box.addWidget(self.re_password_text)
        v_box.addWidget(self.re_password)
        v_box.addStretch()

        hh_box = QtWidgets.QHBoxLayout()
        hh_box.addWidget(self.unregister_buton)
        hh_box.addWidget(self.back_button)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addWidget(self.date)
        v2_box.addStretch()
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.warning)
        v3_box.addStretch()

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addLayout(v_box)
        vvv_box.addWidget(self.space)
        vvv_box.addLayout(hh_box)
        vvv_box.addWidget(self.error)
        vvv_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v3_box)
        h_box.addItem(layoutSpacer)
        h_box.addLayout(vvv_box)
        h_box.addStretch()
        h_box.addLayout(v2_box)

        self.setFixedSize(900,500)
        self.setLayout(h_box)

        self.unregister_buton.clicked.connect(self.unregister)
        self.back_button.clicked.connect(self.exit)

class First_Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setWindowTitle("Welcome to Alize Bank...")
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("logo.png"))
        
    def Exit(self):
        self.close()

    def signup_page(self):
        self.signup_page1 = Sign_Up_Page()
        self.close()
        self.signup_page1.show()

    def login_page(self):
        self.login_page1 = Login_Page()
        self.close()
        self.login_page1.show()

    def unregister_page(self):
        self.unregister_page1 = Unregister_Page()
        self.close()
        self.unregister_page1.show()

    def init_ui(self):
        self.register = QtWidgets.QPushButton("Register")
        self.register.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.register.setMinimumSize(300,35)
        self.login = QtWidgets.QPushButton("Login")
        self.login.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.login.setMinimumSize(300,35)
        self.unregister = QtWidgets.QPushButton("Unregister")
        self.unregister.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.unregister.setMinimumSize(300,35)
        self.exit = QtWidgets.QPushButton("Exit")
        self.exit.setStyleSheet("background-color:green;color:white;font:10pt;width:20px")
        self.exit.setMinimumSize(300,35)

        self.bank_name=QtWidgets.QLabel()
        self.bank_name.setText("Alize Bank")
        self.bank_name.setStyleSheet("color:green;")
        self.bank_name.setFont(QtGui.QFont("arial",45))

        self.name = QtWidgets.QLabel()
        self.name.setText("            Ömer Şenol")
        self.name.setStyleSheet("color:gray")
        self.name.setFont(QtGui.QFont("arial",7))

        self.turkish_liras_currency = QtWidgets.QLabel()
        self.turkish_liras_currency.setText("Turkish Lira: "+main_page_turkish_lira_information[:4])
        self.turkish_liras_currency.setFont(QtGui.QFont("arial",15))
        self.turkish_liras_currency.setStyleSheet("color:green")
        self.euro_currency = QtWidgets.QLabel()
        self.euro_currency.setText("Euro: "+main_page_euro_information[:4])
        self.euro_currency.setFont(QtGui.QFont("arial",15))
        self.euro_currency.setStyleSheet("color:green")
        self.pound_currency = QtWidgets.QLabel()
        self.pound_currency.setText("Pound: "+main_page_pound_information[:4])
        self.pound_currency.setFont(QtGui.QFont("arial",15))
        self.pound_currency.setStyleSheet("color:green")    
        
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        if(len(str(minute))==1):
            minute = "0" + str(minute)
        if(len(str(hour))==1):
            hour = "0"+str(hour)
        day = datetime.strftime(datetime.now(),"%D\n%A\n")
        day = day+str(hour)+":"+str(minute)
               
        self.date = QtWidgets.QLabel()
        self.date.setText(day)
        self.date.setFont(QtGui.QFont("arial",15))
        self.date.setStyleSheet("color:green")

        vv_box = QtWidgets.QVBoxLayout()
        vv_box.addWidget(self.bank_name)

        vvv_box = QtWidgets.QVBoxLayout()
        vvv_box.addStretch()
        vvv_box.addWidget(self.login)
        vvv_box.addWidget(self.register)
        vvv_box.addWidget(self.unregister)
        vvv_box.addWidget(self.exit)
        vvv_box.addStretch()

        hhh_box =QtWidgets.QHBoxLayout()
        hhh_box.addStretch()
        hhh_box.addLayout(vvv_box)
        hhh_box.addStretch()

        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addLayout(vv_box)
        v_box.addStretch()
        v_box.addLayout(hhh_box)
        v_box.addStretch()

        v_currency = QtWidgets.QVBoxLayout()
        v_currency.addWidget(self.turkish_liras_currency)
        v_currency.addWidget(self.euro_currency)
        v_currency.addWidget(self.pound_currency)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.addStretch()
        v2_box.addLayout(v_currency)
        
        v3_box = QtWidgets.QVBoxLayout()
        v3_box.addWidget(self.date)
        v3_box.addStretch()
        v3_box.addWidget(self.name)

        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v2_box)
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()
        h_box.addLayout(v3_box)

        self.register.clicked.connect(self.signup_page)
        self.exit.clicked.connect(self.Exit)
        self.login.clicked.connect(self.login_page)
        self.unregister.clicked.connect(self.unregister_page)
        
        self.setLayout(h_box)
        self.setFixedSize(900,500)
        self.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
bank = First_Page()
sys.exit(app.exec_())