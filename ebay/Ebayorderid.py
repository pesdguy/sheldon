import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from zeep import Client
import json



processOrderUrl = ''
isProductionUrl = False
with open('setting.json') as setting_file:
	settingsdata = json.load(setting_file)
	processOrderUrl = settingsdata["ProcessOrderurl"]
	isProductionUrl = settingsdata["isproduction"]
	cardno=settingsdata["cardno"]
	Expd=settingsdata["Expd"]
	cvv=settingsdata["cvv"]
	Uname=settingsdata["Uname"]
	Pass=settingsdata["Pass"]
	paypal_Un=settingsdata["paypal_Un"]
	paypal_pass=settingsdata["paypal_pass"]


def updateOrder(order_id,itemid,transactionid,trackingid,trackingurl):
	 client = Client('http://staging.esupplybox.com/api/soap/?wsdl')
	 clientSession = client.service.login("test", "tester")
	 params = {}
	 params['item_id'] = itemid.encode('utf-8')  #required
	 params['order_id'] = order_id.encode('utf-8') # required
	 params['ebay_transaction_id'] = transactionid.encode('utf-8') # required
	 params['trackig_id'] = trackingid.encode('utf-8')   # required
	 params['tracking_url'] = trackingurl.encode('utf-8')  # opcional
	 print params
	 result = client.service.call(clientSession, 'neworders.update', str(params))
	 print result


def GetOrderInfo():
    client = Client('http://staging.esupplybox.com/api/soap/?wsdl')

    clientSession = client.service.login("test", "tester")
    fromto = {}
    fromto['from'] = '2017-11-07 00:00:00'
    fromto['to'] = '2017-11-09 00:00:00'
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
        Country=order["country"]
        Zipcode=order["zipcode"]
        Ebay_Item_id=order["selectedebayitemid"]
        
        if isProductionUrl == "True":
            SubmitOrderProduction(order_id,Ebay_Item_id,First_Name,Last_Name,Ship_address1,Ship_address2,City,State,Telephone,Country,Zipcode,Itemid)
        else:
            SubmitOrderSandbox(order_id,Ebay_Item_id,Shipname,Ship_address1,Ship_address2,City,State,Telephone,Country,Zipcode,Itemid)
      
      
def SubmitOrderProduction(orderid,ebayitemid,First_Name,Last_Name,Ship_address1,Ship_address2,city,state,Telephone,country,Zipcode,Itemid):
    print "production ......."
    driver=webdriver.Firefox()
    url = processOrderUrl + str(ebayitemid)
    driver.get(url)
    default_wait= 20
    main_window = driver.window_handles[0]
    time.sleep(10)
    elementFound = False
    try:
        try:
            Buybutton=driver.find_element_by_id("binBtn_btn")
        except:
            Buybutton = driver.find_element_by_id("but_v4-31binLnk")
        Buybutton.click()
        elementFound = True;
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
            resultupdate = updateOrder(orderid, Itemid, '-', 'Issue in Item Page', url)
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
    City=driver.find_element_by_id("af-city")
    City.send_keys(city)
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
    Entercardnumb=driver.find_element_by_id("cc")
    Entercardnumb.send_keys(cardno)
    time.sleep(5)
    Expirydate=driver.find_element_by_id("expiry_value")
    Expirydate.send_keys(Expd)
    time.sleep(5)
    EnterCVV=driver.find_element_by_id("cvv")
    EnterCVV.send_keys(cvv)
    time.sleep(5)
    proceed=driver.find_element_by_id("proceedButton")
    proceed.click()
    time.sleep(5)
    driver.switch_to_window(main_window)
	#updateOrderStatus(ebayitemid)
	#except Exception:
	#driver.close()
	#pass  
    
    
    
def SubmitOrderSandbox(orderid,ebayitemid,Shipname,Ship_address1,Ship_address2,city,state,Telephone,Country,Zipcode,Itemid):
	print "staging ......."
	driver=webdriver.Firefox()
	url = processOrderUrl + str(ebayitemid)
	driver.get(url)
	time.sleep(15)
	elementFound = False
	try:
		try:
			Buybutton=driver.find_element_by_id("binBtn_btn")
		except:
			Buybutton = driver.find_element_by_id("but_v4-31binLnk")
		Buybutton.click()
		elementFound = True;
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
			resultupdate = updateOrder(orderid, Itemid, '-', 'Issue in Item Page', url)
			print resultupdate
		except:
			pass
		return
	Username=driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/form/div[1]/div[2]/div/div[4]/span[2]/input")
	Username.send_keys(Uname)
	Password=driver.find_element_by_xpath("html/body/div[4]/div/div/div/div[5]/div[1]/div[1]/div/div/div[1]/div[2]/div/span/form/div[1]/div[2]/div/div[5]/span[2]/input")
	Password.send_keys(Pass)
	Signin=driver.find_element_by_id("sgnBt")
	Signin.click()
	time.sleep(20)
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
	City=driver.find_element_by_id("city")            
	City.send_keys(city)
	time.sleep(1)
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
	time.sleep(1)
	ShipaddressButton=driver.find_element_by_id("but_shiptobtn")
	ShipaddressButton.click()
	time.sleep(10)
	driver.switch_to_default_content()
	time.sleep(30)
	Paypal=driver.find_element_by_id("PAYPAL")
	Paypal.click()
	time.sleep(5)
	ButtonToContinue=driver.find_element_by_id("but_ryp_continue")
	ButtonToContinue.click()
	time.sleep(30)
	driver.switch_to_frame(driver.find_element_by_name("injectedUl"))
	time.sleep(30)
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
    
  
GetOrderInfo()  
