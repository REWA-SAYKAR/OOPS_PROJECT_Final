import customtkinter
import sqlite3
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import os
from twilio.rest import Client
from datetime import datetime

app = customtkinter.CTk()
app.title('112103126 Restaurant Management System')
app.geometry('724x640')
app.config(bg='#000')#diff bet config and configure
app.resizable(False,False)#width and height will not be resizacle if False

font1 = ('Arial',22,'bold')

def get_dishes(): 
    conn = sqlite3.connect('dish.db')
    c = conn.cursor()
    c.execute('SELECT dish_name,price FROM dish')
    results = c.fetchall()
    print(results)
    
    global dish1_details
    global dish2_details
    global dish3_details
    
    dish1_details = results[0]
    dish2_details = results[1]    
    dish3_details = results[2]
    
    p1_name_label.configure(text="{}\nPrice: Rs{}".format(dish1_details[0],dish1_details[1]))
    p2_name_label.configure(text="{}\nPrice: Rs{}".format(dish2_details[0],dish2_details[1]))    
    p3_name_label.configure(text="{}\nPrice: Rs{}".format(dish3_details[0],dish3_details[1]))

    conn.close()
    
def get_quantity():
    conn = sqlite3.connect('dish.db')
    c = conn.cursor()
    c.execute('SELECT quantity FROM dish')
    results = c.fetchall()
    
    global dish1_quantity
    global dish2_quantity
    global dish3_quantity
    
    dish1_quantity = results[0][0]
    dish2_quantity = results[1][0]
    dish3_quantity = results[2][0]

    if dish1_quantity == 0:
        variable1.set('0')
        p1_quatity.destroy()
        p1_state_label = customtkinter.CTkLabel(p1_frame,font=font1,text='Dish Sold ',text_color='#ff0',bg_color='#000',width=100)
        p1_state_label.place(x=20,y=270)
        
    else:
        list1 = [str(i) for i in range(dish1_quantity+1)]
        p1_quatity.configure(values = list1)
        p1_quatity.set('0')
        
    if dish2_quantity == 0:
        variable2.set('0')
        p2_quatity.destroy()
        p2_state_label = customtkinter.CTkLabel(p2_frame,font=font1,text='Dish Sold ',text_color='#ff0',bg_color='#000',width=100)
        p2_state_label.place(x=20,y=270)
        
    else:
        list2 = [str(i) for i in range(dish2_quantity+1)]
        p2_quatity.configure(values = list2)
        p2_quatity.set('0')
    
    if dish3_quantity == 0:
        variable3.set('0')
        p3_quatity.destroy()
        p3_state_label = customtkinter.CTkLabel(p3_frame,font=font1,text='Dish Sold ',text_color='#ff0',bg_color='#000',width=100)
        p3_state_label.place(x=20,y=270)
        
    else:
        list3 = [str(i) for i in range(dish3_quantity+1)]
        p3_quatity.configure(values = list3)
        p3_quatity.set('0')
        

def checkout():
    if dish1_quantity==0 and dish2_quantity==0 and dish3_quantity==0:
        messagebox.showerror('ERROR','Can not serve you now.')
    else:
        if customer_entry.get():
            conn = sqlite3.connect('dish.db')
            c = conn.cursor()
            global qty1
            global qty2 
            global qty3
            qty1 = int(variable1.get())    
            qty2 = int(variable2.get())            
            qty3 = int(variable3.get())
            
            c.execute("UPDATE dish SET quantity = ? WHERE id = ?",(dish1_quantity-qty1,1))
            c.execute("UPDATE dish SET quantity = ? WHERE id = ?",(dish2_quantity-qty2,2))
            c.execute("UPDATE dish SET quantity = ? WHERE id = ?",(dish3_quantity-qty3,3))
            conn.commit()
            conn.close()
            global total_price
            total_price = qty1*dish1_details[1] + qty2*dish2_details[1] + qty3*dish3_details[1]
            if total_price == 0:
                messagebox.showinfo('NOTE','Please choose a dish')
            else:
                price_label.configure(text=f'Price:Rs{total_price}')
                get_quantity()
                with open('Order_receipts.txt','a') as f:
                    f.write(f'\nName --> {customer_entry.get()}\n')
                    f.write(f'Misal Pav --> {qty1}\n')
                    f.write(f'Dhokla --> {qty2}\n')
                    f.write(f'Pongal --> {qty3}\n')
                    f.write(f'Total BILL --> Rs{total_price}\n')
                    f.write(f'------------------\nThankYou\n------------------')
        else:
            messagebox.showerror('ERROR','Please enter the customer name.')
import pywhatkit
#from import_mobile_no import MobileNo
from urllib.parse import quote            
def send_msg():
    if dish1_quantity!=0 or dish2_quantity!=0 or dish3_quantity!=0:
        if qty1 != 0 and qty2 == 0 and qty3 == 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Misal pav. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 != 0 and qty3 == 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty2)+' Dhokla. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 == 0 and qty3 != 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty3)+' Pongal. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 != 0 and qty3 == 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Misal pav and '+str(qty2)+' Dhokla. Thank you! We will love to see you again!'
        elif qty1 == 0 and qty2 != 0 and qty3 != 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty2)+' Dhokla and '+str(qty3)+' Pongal. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 == 0 and qty3 != 0:
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Misal pav and '+str(qty3)+' Pongal. Thank you! We will love to see you again!'
        elif qty1 != 0 and qty2 != 0 and qty3 != 0: 
            Msg = 'Thankyou for choosing our restaurant Mr./Mrs. '+ customer_entry.get() +'.  Your total bill is Rs. '+str(total_price)+'. You ordered '+str(qty1)+' Misal pav '+str(qty2)+' Dhokla and '+str(qty3)+' Pongal. Thank you! We will love to see you again!'
        now = datetime.now()
        hr = int(now.strftime("%H"))
        min = int(now.strftime("%M")) + 2
        MobileNo = "+91 "+number_entry.get()
        pywhatkit.sendwhatmsg(MobileNo,Msg,hr,min)
    
    
    
                

variable1 = StringVar()
variable2 = StringVar()
variable3 = StringVar()




frame1 = customtkinter.CTkFrame(app,bg_color='#000',fg_color='#000',width=724,height=195)
frame1.place(x=0,y=0)

frame2 = customtkinter.CTkFrame(app,bg_color='#000',fg_color='#0E0F0F',width=724,height=440)
frame2.place(x=0,y=195)


image1 = Image.open("/home/hp/Desktop/vscode/rp_proj_final/RP_top_banner.jpg").resize((724,195))#!!!two bracks not one
photo1 = ImageTk.PhotoImage(image1)

image1_label = Label(frame1,image=photo1,bg='#000')
image1_label.place(x=0,y=0)
#image1_label.pack()

p1_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p1_frame.place(x=10,y=20)
image2 = Image.open("/home/hp/Desktop/vscode/rp_proj_final/misal_pav_final.webp").resize((228,270))
photo2 = ImageTk.PhotoImage(image2)
image2_label = Label(p1_frame,image=photo2,bg='#333333')
image2_label.place(x=0,y=0)
#image2_label.pack()
p1_name_label = customtkinter.CTkLabel(p1_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p1_name_label.place(x=17,y=200)
p1_quatity = customtkinter.CTkComboBox(p1_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable1,width=120)
p1_quatity.set('0')
p1_quatity.place(x=40,y=270)

p2_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p2_frame.place(x=248,y=20)
image3 = Image.open("/home/hp/Desktop/vscode/rp_proj_final/RP_dhokla.jpg").resize((228,270))
photo3 = ImageTk.PhotoImage(image3)
image3_label = Label(p2_frame,image=photo3,bg='#333333')
image3_label.place(x=0,y=0)
#image3_label.pack()
p2_name_label = customtkinter.CTkLabel(p2_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p2_name_label.place(x=40,y=200)
p2_quatity = customtkinter.CTkComboBox(p2_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable2,width=120)
p2_quatity.set('0')
p2_quatity.place(x=40,y=270)

p3_frame = customtkinter.CTkFrame(frame2,bg_color='#0E0F0F',fg_color='#333333',corner_radius=0,width=228,height=320)
p3_frame.place(x=486,y=20)
image4 = Image.open("/home/hp/Desktop/vscode/rp_proj_final/RP_pongal.jpg").resize((228,270))
photo4 = ImageTk.PhotoImage(image4)
image4_label = Label(p3_frame,image=photo4,bg='#333333')
image4_label.place(x=0,y=0)
#image4_label.pack()
p3_name_label = customtkinter.CTkLabel(p3_frame,font=font1,text='',text_color='#fff',bg_color='#333333')
p3_name_label.place(x=23,y=200)
p3_quatity = customtkinter.CTkComboBox(p3_frame,font=font1,text_color='#000',fg_color='#fff',dropdown_hover_color='#06911f',button_color='#f67a0d',button_hover_color='#f67a0d',variable=variable3,width=120)
p3_quatity.set('0')
p3_quatity.place(x=40,y=270)
#-----------------------------------------------------------------------------------------------------------

customer_label = customtkinter.CTkLabel(frame2,font=font1,text='Customer: ',text_color='#fff',bg_color='#0E0F0F')
customer_label.place(x=40,y=370)

customer_entry = customtkinter.CTkEntry(frame2,font=font1,text_color='#000',fg_color='#fff',border_color='#fff',width=150)
customer_entry.place(x=150,y=370)

checkout_button = customtkinter.CTkButton(frame2,command=checkout,font=font1,text_color='#fff',text='ORDER',fg_color='#410ae3',hover_color='#3303c0',bg_color='#0e0f0f',cursor = 'hand2',corner_radius=30,width=160,height=50)
checkout_button.place(x=340,y=360)

price_label = customtkinter.CTkLabel(frame2,font=font1,text='',text_color='#0f0',bg_color='#0E0F0F')
price_label.place(x=540,y=370)

wp_image = Image.open("/home/hp/Desktop/vscode/rp_proj_final/wp_img.png").resize((30,30))
wp_img = ImageTk.PhotoImage(wp_image)

send_button = customtkinter.CTkButton(frame2,image= wp_img,text= " ",command=send_msg,font=font1,fg_color='#0E0F0F',hover_color='#0E0F0F',bg_color='#0E0F0F',cursor = 'hand2',corner_radius=30,width= 30,height= 30)
send_button.place(x=498,y=405)

number_entry = customtkinter.CTkEntry(frame2,font=font1,text_color='#000',fg_color='#fff',border_color='#fff',width=150, height= 29)
number_entry.place(x=568,y=406)

get_dishes()
get_quantity()

app.mainloop()
