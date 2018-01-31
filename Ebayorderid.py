import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from zeep import Client
import json,os



isProductionUrl = False
cardno=""
Expd=""
cvv=""
Uname=""
Pass=""
paypal_Un=""
paypal_pass=""


def updateOrder(order_id,itemid,transactionid,trackingid,trackingurl):
    shelcomm = 'php5 updateorder.php ' + itemid + ' ' + order_id + ' ' + transactionid + ' ' + trackingid + ' '  + trackingurl
    os.system("")
    print result


def GetOrderInfo():
    client = Client('http://www.esupplybox.com/index.php/api/soap/?wsdl')

    clientSession = client.service.login("ebay_connection", "prabhjit123")
    fromto = {}
    fromto['from'] = '2015-1-1 00:00:00'
    fromto['to'] = '2018-1-13 00:00:00'
    createdate = {}
    createdate['created_at'] = fromto
    datefilter = {}
    datefilter['complex_filter'] = createdate
    resultFilter =  datefilter
    result = client.service.call(clientSession, 'neworders.list', str(resultFilter))
    print result
    jsonData = json.loads(result)
    for order in jsonData:
        order_id=order["entity_id"]
        Itemid=order["itemid"]
        orderdate=order["orderdate"]
        Shipname=order["buyer_name"]
        Split_Name=Shipname.split()
        First_Name=Split_Name[0]
        Last_Name=Split_Name[1]
        Ship_address1=order["address_line_1"]
        Ship_address2=order["address_line_2"]
        State=order["state"]
        City=order["city"]
        Country=order["country"]
        Telephone=order["telephone"]
        quantity = order["qty"]
        Zipcode=order["zipcode"]
        Purchasetype =order["purchase_type"]
        Purchaseurl =order["purchase_url"]
        Ebay_Item_id=order["selectedebayitemid"]
        Environment = order["environment"]

        with open('setting.json') as setting_file:
            settingsdata = json.load(setting_file)
            settingsdata = settingsdata[Environment]
            global cardno
            cardno=settingsdata["cardno"]
            global Expd
            Expd=settingsdata["Expd"]
            global cvv
            cvv=settingsdata["cvv"]
            global Uname
            Uname=settingsdata["Uname"]
            global Pass
            Pass=settingsdata["Pass"]
            global paypal_Un
            paypal_Un=settingsdata["paypal_Un"]
            global paypal_pass
            paypal_pass=settingsdata["paypal_pass"]


        if Environment == "production":
            if Purchasetype == "offer":
                Placebid(Purchaseurl,First_Name,Last_Name,Ship_address1,Ship_address2,City,State,Telephone,Country,Zipcode,Uname,Pass,paypal_Un,paypal_pass)
            elif Purchasetype == "straight":
                SubmitOrderProduction(order_id,Purchaseurl,First_Name,Last_Name,Ship_address1,Ship_address2,City,State,Telephone,Country,Zipcode,Itemid,Uname,Pass,paypal_Un,paypal_pass)
        else:
            SubmitOrderSandbox(order_id,Purchaseurl,First_Name,Last_Name,Ship_address1,Ship_address2,City,State,Telephone,Country,Zipcode,Itemid,Uname,Pass,paypal_Un,paypal_pass) 
                
            
      
def SubmitOrderProduction(orderid,Purchaseurl,First_Name,Last_Name,Ship_address1,Ship_address2,city,state,Telephone,country,Zipcode,Itemid,Uname,Pass,paypal_Un,paypal_pass):
    print "production ......."
    driver=webdriver.Firefox()
    url = Purchaseurl
    driver.get(url)
    default_wait= 20
    main_window = driver.window_handles[0]
    time.sleep(10)
    elementFound = False
    try:
        try:
            Selectcolor=Select(driver.find_element_by_id("msku-sel-1"))
            Selectcolor.select_by_visible_text("Black")
        except Exception:
            pass
        try:
            Selectlength=Select(driver.find_element_by_id("msku-sel-2"))
            Selectlength.select_by_visible_text("6ft")
        except Exception:
            pass   
        try:
            Buybutton=driver.find_element_by_id("binBtn_btn")
        except:
            Buybutton = driver.find_element_by_id("but_v4-31binLnk")
        Buybutton.click()
        elementFound = True
    except Exception:
        pass
    try:
        Buybutton=driver.find_element_by_xpath("html/body/div[3]/div[3]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/a")
        Buybutton.click()
        elementFound = True
    except Exception:
        pass
    if elementFound == False:
        driver.close()
        print "Issue in Order"
        try:
            resultupdate = updateOrder(orderid, Itemid, '-', 'item is already sold', url)
            print resultupdate
        except:
            pass
        return
    #sys.exit()
    time.sleep(10)       
    Username=driver.find_element_by_id("userid")
    Username.send_keys(Uname)
    Password=driver.find_element_by_id("pass")
    Password.send_keys(Pass)
    Signin=driver.find_element_by_id("sgnBt")
    Signin.click()
    time.sleep(10)
    try:
        Commitbutton=driver.find_element_by_id("but_v4-2")
        Commitbutton.click()
    except Exception:
        pass
    time.sleep(20)
    try:
        Paynowbutton=driver.find_element_by_id("but_v4-1")
        Paynowbutton.click()
    except Exception:
        pass
    time.sleep(60)
    AddressChange=driver.find_element_by_xpath(".//*[@id='sa-change-link']/a")
    AddressChange.click()
    time.sleep(30)
    Add_address=driver.find_element_by_link_text("Add a new address")
    Add_address.click()
    time.sleep(10)
    CountryOrRegion=Select(driver.find_element_by_id("af-country"))
    CountryOrRegion.select_by_visible_text(country)
    time.sleep(2)
    ContactFName=driver.find_element_by_id("af-first-name")
    ContactFName.send_keys(First_Name)
    time.sleep(1)
    ContactLName=driver.find_element_by_id("af-last-name")
    ContactLName.send_keys(Last_Name)
    StreetAddress1=driver.find_element_by_id("af-address1")
    StreetAddress1.send_keys(Ship_address1)
    time.sleep(1)
    StreetAddress2=driver.find_element_by_id("af-address2")
    StreetAddress2.send_keys(Ship_address2)
    time.sleep(1)
    try:
        City=driver.find_element_by_id("af-city")
        City.send_keys(city)
    except Exception:
        pass
    time.sleep(1)
    try:
        City=Select(driver.find_element_by_id("af-city"))
        City.select_by_visible_text(city)
    except Exception:
        pass
    time.sleep(3)
    try:
        State=driver.find_element_by_id("af-state")
        State.send_keys(state)
    except Exception:
        pass
    try:
        State=Select(driver.find_element_by_id("af-state"))
        State.select_by_visible_text(state)
    except Exception:
        pass
    time.sleep(3)
    zipc=driver.find_element_by_id("af-zip")
    zipc.send_keys(Zipcode)
    time.sleep(1)
    Phoneno=driver.find_element_by_xpath(".//*[@id='address-fields']/div[6]/span/input")
    Phoneno.send_keys(Telephone)
    time.sleep(1)
    Add=driver.find_element_by_xpath(".//*[@id='address-fields-ctr']/div[2]/div[3]/button")
    Add.click()
    time.sleep(10)
    noteButton = driver.find_element_by_class_name("slr-msg-link")
    noteButton.click()
    time.sleep(2)
    Message = driver.find_element_by_id("seller-message")
    Message.send_keys("Seller Make Blind Shipping")
    time.sleep(5)
    AddNote = driver.find_element_by_xpath(".//*[@id='seller-message-ctr']/div/div/div[3]/button")
    AddNote.click()
    try:
        resultupdate = updateOrder(orderid, Itemid, '-', 'Issue in Item Page', url)
        print resultupdate
    except Exception:
        pass
    time.sleep(10)
    try:
        ConfirmAdd=driver.find_element_by_id("recommended-addr-btn")
        ConfirmAdd.click()
    except Exception:
        pass
    time.sleep(20)
    Paypal=driver.find_element_by_id("PAYPAL")
    Paypal.click()
    time.sleep(5)
    child_window = driver.window_handles[1]
    driver.switch_to_window(child_window)
    time.sleep(30)
    Paypal_Username=driver.find_element_by_id("email")
    Paypal_Username.send_keys(paypal_Un)
    time.sleep(1)
    Paypal_Password=driver.find_element_by_id("password")
    Paypal_Password.send_keys(paypal_pass)
    time.sleep(1)
    Paypal_Login=driver.find_element_by_id("btnLogin")
    Paypal_Login.click()
    time.sleep(30)
    rememberme=driver.find_element_by_id("declineRememberMe")
    rememberme.click()
    time.sleep(30)
    driver.switch_to_window(main_window)
    time.sleep(5)
    ConfirmAndPay = driver.find_element_by_id("cta-btn")
    ConfirmAndPay.click()
    time.sleep(10)
    SeeOrderdetails = driver.find_element_by_xpath(".//*[@id='success-order-summary']/div[1]/div[3]/a")
    SeeOrderdetails.click()

	
    
    
    
def SubmitOrderSandbox(orderid,Purchaseurl,Shipname,Ship_address1,Ship_address2,city,state,Telephone,Country,Zipcode,Itemid,Uname,Pass,paypal_Un,paypal_pass):
	print "staging ......."
	driver=webdriver.Firefox()
	url = Purchaseurl
	driver.get(url)
	time.sleep(15)
	elementFound = False
	try:
		Selectcolor=Select(driver.find_element_by_id("msku-sel-1"))
		Selectcolor.select_by_visible_text("Black")
	except Exception:
		pass
	try:
		Selectlength=Select(driver.find_element_by_id("msku-sel-2"))
		Selectlength.select_by_visible_text("6ft")
	except Exception:
		pass
	try:
		try:
			Buybutton=driver.find_element_by_id("binBtn_btn")
		except:
			Buybutton = driver.find_element_by_id("but_v4-31binLnk")
		Buybutton.click()
		elementFound = True;
	except Exception:
		pass
	time.sleep(5)
	try:
		Buybutton=driver.find_element_by_xpath("html/body/div[3]/div[3]/div[3]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/div/a")
		Buybutton.click()
		elementFound = True
	except Exception:
		pass
	if elementFound == False:
		driver.close()
		print "Issue in Order"
		try:
			resultupdate = updateOrder(orderid, Itemid, '-', 'Issue in Item Page', url)
			print resultupdate
		except:
			pass
		return
	time.sleep(10)
	Username=driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/form/div[1]/div[2]/div/div[4]/span[2]/input")
	Username.send_keys(Uname)
	Password=driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/form/div[1]/div[2]/div/div[5]/span[2]/input")
	Password.send_keys(Pass)
	Signin=driver.find_element_by_id("sgnBt")
	Signin.click()
	time.sleep(20)
	#try:
		#Quantity=driver.find_element_by_id("quantity")
		#Quantity.send_keys(quantity)
	#except Exception:
		#pass
	#time.sleep(5)
	try:
		ContinueButton=driver.find_element_by_name("Continue")
		ContinueButton.click()
	except Exception:
		pass
	time.sleep(10)
	Commitbutton=driver.find_element_by_id("but_v4-2")
	Commitbutton.click()
	time.sleep(20)
	Paynowbutton=driver.find_element_by_id("but_v4-1")
	Paynowbutton.click()
	time.sleep(100)
	AddressChange=driver.find_element_by_id("chgShipping")
	AddressChange.click()
	time.sleep(20)
	driver.switch_to_frame(0)
	Add_address=driver.find_element_by_link_text("Add a new address")
	Add_address.click()
	time.sleep(10)
	CountryOrRegion=Select(driver.find_element_by_id("country"))
	CountryOrRegion.select_by_visible_text(Country)
	time.sleep(2)
	ContactName=driver.find_element_by_id("contactName" )
	ContactName.send_keys(Shipname)
	time.sleep(1)
	StreetAddress1=driver.find_element_by_id("address1")
	StreetAddress1.send_keys(Ship_address1)
	time.sleep(1)
	StreetAddress2=driver.find_element_by_id("address2" )
	StreetAddress2.send_keys(Ship_address2)
	time.sleep(1)
	try:
		City=driver.find_element_by_id("city")            
		City.send_keys(city)
	except Exception:
		pass
	time.sleep(1)
	try:
		City=Select(driver.find_element_by_id("city"))
		City.select_by_visible_text(city)
	except Exception:
		pass
	time.sleep(2)
	try:
		State=driver.find_element_by_id("state")
		State.send_keys(state)
	except Exception:
		pass
	try:
		State=Select(driver.find_element_by_id("state"))   
		State.select_by_visible_text(state)
	except Exception:
		pass
	time.sleep(1)
	print Zipcode
	zipc=driver.find_element_by_id("zip")
	zipc.send_keys(Zipcode)
	time.sleep(1)
	Phoneno=driver.find_element_by_id("dayphone1")     
	Phoneno.send_keys(Telephone)
	time.sleep(10)
	ShipaddressButton=driver.find_element_by_id("but_shiptobtn")
	ShipaddressButton.click()
	time.sleep(10)
	driver.switch_to_default_content()
	time.sleep(20)
	Paypal=driver.find_element_by_id("PAYPAL")
	Paypal.click()
	time.sleep(5)
	ButtonToContinue=driver.find_element_by_id("but_ryp_continue")
	ButtonToContinue.click()
	time.sleep(20)
	driver.switch_to_frame(driver.find_element_by_name("injectedUl"))
	time.sleep(20)
	Paypal_Username=driver.find_element_by_id("email")
	Paypal_Username.send_keys(paypal_Un)
	time.sleep(5)
	Paypal_Password=driver.find_element_by_id("password")
	Paypal_Password.send_keys(paypal_pass)
	time.sleep(5)
	Paypal_Login=driver.find_element_by_id("btnLogin")
	Paypal_Login.click()
	time.sleep(30)
	driver.switch_to_default_content()
	Pay_Order=driver.find_element_by_id("confirmButtonTop")
	Pay_Order.click()
	time.sleep(20)
	Completeorder=driver.find_element_by_id("but_succturbocontinue")
	Completeorder.click()
    
def Placebid(Purchaseurl,First_Name,Last_Name,Ship_address1,Ship_address2,city,state,Telephone,country,Zipcode,Uname,Pass,paypal_Un,paypal_pass):
    driver=webdriver.Firefox()
    url = Purchaseurl
    driver.get(url)
    default_wait= 20
    main_window = driver.window_handles[0]
    try:
        SignInButton = driver.find_element_by_xpath(".//*[@id='gh-ug']/a")
        SignInButton.click()
    except Exception:
        pass
    time.sleep(5)
    Username=driver.find_element_by_id("userid")
    Username.send_keys(Uname)
    time.sleep(2)
    Password=driver.find_element_by_id("pass")
    Password.send_keys(Pass)
    time.sleep(2)
    Signin=driver.find_element_by_id("sgnBt")
    Signin.click()
    time.sleep(5)
    try:
        PayNow = driver.find_element_by_link_text("pay now")
        PayNow.click()
    except Exception:
        pass
    time.sleep(5)
    try:
        purchaseHistory = driver.find_element_by_xpath(" .//*[@id='msgPanel']/div/div/span/span[1]/a")
        purchaseHistory.click()
    except Exception:
        pass
    time.sleep(10)
    Paynowlink = driver.find_element_by_id("PayNow")
    Paynowlink.click()
    time.sleep(10)
    AddressChange=driver.find_element_by_xpath(".//*[@id='sa-change-link']/a")
    AddressChange.click()
    time.sleep(30)
    Add_address=driver.find_element_by_link_text("Add a new address")
    Add_address.click()
    time.sleep(10)
    CountryOrRegion=Select(driver.find_element_by_id("af-country"))
    CountryOrRegion.select_by_visible_text(country)
    time.sleep(2)
    ContactFName=driver.find_element_by_id("af-first-name")
    ContactFName.send_keys(First_Name)
    time.sleep(1)
    ContactLName=driver.find_element_by_id("af-last-name")
    ContactLName.send_keys(Last_Name)
    StreetAddress1=driver.find_element_by_id("af-address1")
    StreetAddress1.send_keys(Ship_address1)
    time.sleep(1)
    StreetAddress2=driver.find_element_by_id("af-address2")
    StreetAddress2.send_keys(Ship_address2)
    time.sleep(1)
    try:
        City=driver.find_element_by_id("af-city")
        City.send_keys(city)
    except Exception:
        pass
    time.sleep(1)
    try:
        City=Select(driver.find_element_by_id("af-city"))
        City.select_by_visible_text(city)
    except Exception:
        pass
    time.sleep(3)
    try:
        State=driver.find_element_by_id("af-state")
        State.send_keys(state)
    except Exception:
        pass
    try:
        State=Select(driver.find_element_by_id("af-state"))
        State.select_by_visible_text(state)
    except Exception:
        pass
    time.sleep(3)
    zipc=driver.find_element_by_id("af-zip")
    zipc.send_keys(Zipcode)
    time.sleep(1)
    Phoneno=driver.find_element_by_xpath(".//*[@id='address-fields']/div[6]/span/input")
    Phoneno.send_keys(Telephone)
    time.sleep(1)
    Add=driver.find_element_by_xpath(".//*[@id='address-fields-ctr']/div[2]/div[3]/button")
    Add.click()
    time.sleep(3)
    try:
        ConfirmAdd=driver.find_element_by_id("recommended-addr-btn")
        ConfirmAdd.click()
    except Exception:
        pass
    time.sleep(5)
    noteButton = driver.find_element_by_class_name("slr-msg-link")
    noteButton.click()
    time.sleep(2)
    Message = driver.find_element_by_id("seller-message")
    Message.send_keys("Seller Make Blind Shipping")
    time.sleep(5)
    AddNote = driver.find_element_by_xpath(".//*[@id='seller-message-ctr']/div/div/div[3]/button")
    AddNote.click() 
    time.sleep(3)
    try:
        resultupdate = updateOrder(orderid, Itemid, '-', 'Issue in Item Page', url)
        print resultupdate
    except Exception:
        pass
    time.sleep(20)
    Paypal=driver.find_element_by_id("PAYPAL")
    Paypal.click()
    time.sleep(5)
    child_window = driver.window_handles[1]
    driver.switch_to_window(child_window)
    time.sleep(30)
    Paypal_Username=driver.find_element_by_id("email")
    Paypal_Username.send_keys(paypal_Un)
    time.sleep(1)
    Paypal_Password=driver.find_element_by_id("password")
    Paypal_Password.send_keys(paypal_pass)
    time.sleep(1)
    Paypal_Login=driver.find_element_by_id("btnLogin")
    Paypal_Login.click()
    time.sleep(30)
    rememberme=driver.find_element_by_id("declineRememberMe")
    rememberme.click()
    time.sleep(20)
    driver.switch_to_window(main_window)
    time.sleep(5)
    ConfirmAndPay = driver.find_element_by_id("cta-btn")
    ConfirmAndPay.click()
    time.sleep(10)
    #SeeOrderdetails = driver.find_element_by_xpath(".//*[@id='success-order-summary']/div[1]/div[3]/a")
    #SeeOrderdetails.click()

    
    
    
  
GetOrderInfo()  







    
    
    

    
    
  
    
    
    
  
 
  
  
    
  
    
    
    
