from cs50 import get_string
import re

n=get_string("Number: ")

def check(n):
    a=[]
    c=[]
    #Iterate over the input
    for i in range(len(n)):
        if i%2==0:
            a.append(int(n[i])*2)
        else:
            c.append(int(n[i]))
    b=sum(c)
    x=0
    for i in a:
        if i<10:
            x+=i
        else:
            x+=(i%10)+1

    result= x+b
    if result%10==0:
        return True
    else:
        return False

def check_card_type(number):
    number_str = str(number)
    if re.match(r'^3[47]\d{13}$', number_str):
        results='AMEX'
    elif re.match(r'^5[1-5]\d{14}$', number_str):
        results='MASTERCARD'
    elif re.match(r'^4\d{12}$', number_str) or re.match(r'^4\d{15}$', number_str):
        results='VISA'
    else:
        results ='INVALID'
    return results

if check(n)==True:
    print(check_card_type(n))
elif check(n)==False:
    print("INVALID")

print(check_card_type(n))
