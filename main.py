from tkinter import *
import time
import datetime
from csv import *
import os
from reportlab.pdfgen import canvas
import qrcode
from PIL import Image
from reportlab.lib.pagesizes import letter

global number, address, city
address = "Indus University Ahmedabad"
city = "Ahmedabad"
number = 1

class appWindow:
    def __init__(self, root):
        # root = Tk()
        self.root = root
        self.root.geometry("1200x700+0+0")
        self.root.resizable(1, 1)
        self.root.title("Restaurant Management System")

        Tops = Frame(self.root, bg="white", width=1000,
                     height=50, relief=SUNKEN)
        Tops.pack(side=TOP)

        f1 = Frame(self.root, width=900, height=700, relief=SUNKEN)
        f1.pack(side=LEFT)

        f2 = Frame(self.root, width=400, height=700, relief=SUNKEN)
        f2.pack(side=RIGHT)
        # ------------------TIME---------------


        # Get the current local time
        current_local_time = datetime.datetime.now()

        # Format the local time as a string in the desired format
        localtime = current_local_time.strftime("%d-%m-%Y %A %I:%M %p")
# ***************************************************************************************
        # -----------------INFO TOP------------
        lblinfo = Label(Tops, font=('aria', 30, 'bold'),
                        text="Restaurant Management System", fg="steel blue", bd=10, anchor='w')
        lblinfo.grid(row=0, column=0)
        lblinfo = Label(Tops, font=('aria', 20, ),
                        text=localtime, fg="steel blue", anchor=W)
        lblinfo.grid(row=1, column=0)

        # ---------------Calculator------------------
        text_Input = StringVar()
        operator = ""

        txtdisplay = Entry(f2, font=('ariel', 20, 'bold'), textvariable=text_Input,
                           bd=5, insertwidth=7, bg="white", justify='right')
        txtdisplay.grid(columnspan=4)

        def btnclick(numbers):
            global operator
            operator = operator + str(numbers)
            text_Input.set(operator)

        def clrdisplay():
            global operator
            operator = ""
            text_Input.set("")

        def eqals():
            global operator
            sumup = str(eval(operator))

            text_Input.set(sumup)
            operator = ""

        def Ref():
            contFJ = float(FJ.get())
            contGT = float(GT.get())
            contPT = float(PT.get())
            contST = float(ST.get())
            contLassi = float(Lassi.get())
            contDrink = float(Drink.get())

            costofFJ = contFJ*100
            costofGT = contGT*110
            costofPT = contPT*130
            costofST = contST*150
            costofLassi = contLassi*70
            costofdrinks = contDrink*20

            global costofmeal,PaidTax,Service,OverAllCost,FTax,ovrcst
            # ********* TYPE OF COSTS ***************************************************
            cstmeal = (costofFJ + costofGT + costofPT +
                       costofST + costofLassi + costofdrinks)
            costofmeal = "Rs. "+ str('%.2f' % cstmeal)

            PayTax = ((cstmeal)*0.05)  # 33% GST
            PaidTax = "Rs. "+ str('%.2f' % PayTax)

            Ser_Charge = ((cstmeal)/99)
            Service = "Rs. "+ str('%.2f' % Ser_Charge)
            FTax = 'Rs. '+('%.2f' %(PayTax + Ser_Charge))

            ovrcst = PayTax + cstmeal + Ser_Charge
            OverAllCost = "Rs. "+ str('%.2f' % ovrcst)

           

            Service_Charge.set(Service)
            cost.set(costofmeal)
            Tax.set(PaidTax)
            Subtotal.set(FTax)
            Total.set(OverAllCost)

            global Header, dict,pdf

            Header = ['Order No', 'Fafda-Jalebi (500gm)', 'Gujarati Thali', 'Punjabi Thali', 'SouthIndian Tadka', 'Lassi (400ml)', 'Drink (200ml)',
                      'Cost Of Meal', 'Tax(GST)','Total Tax', 'Service charge', 'Final Cost']
            dict = {'Order No': number,
                    'Fafda-Jalebi (500gm)': contFJ,
                    'Gujarati Thali': contGT,
                    'Punjabi Thali': contPT,
                    'SouthIndian Tadka': contST,
                    'Lassi (400ml)': contLassi,
                    'Drink (200ml)': contDrink,
                    'Cost Of Meal': cstmeal,
                    'Tax(GST)': PayTax,
                    'Total Tax': FTax,
                    'Service charge': Ser_Charge,
                    'Final Cost': ovrcst}

                    
            pdf = {
                # 'Order No': number,
                                'Fafda-Jalebi (500gm)': [contFJ,"100",costofFJ],
                                'Gujarati Thali': [contGT,"110",costofGT],
                                'Punjabi Thali': [contPT,"130",costofPT],
                                'SouthIndian Tadka': [contST,"150",costofST],
                                'Lassi (400ml)': [contLassi,"70",costofLassi],
                                'Drink (200ml)': [contDrink,"20",costofdrinks],
                                # 'Cost Of Meal': cstmeal,
                                # 'Tax(GST)': PayTax,
                                # 'Total cost': Totalcost,
                                # 'Service charge': Ser_Charge,
                                # 'Final Cost': ovrcst
                                }




        def qexit():
            self.root.destroy()

        def reset():
            FJ.set("")
            GT.set("")
            PT.set("")
            ST.set("")
            Lassi.set("")
            Drink.set("")
            Subtotal.set("")
            Total.set("")
            Service_Charge.set("")
            Tax.set("")
            cost.set("")

        def generate_invoice():

            #********** UPI Section ********************************************************************
            upi_address = "param.bankid@oksbi"
            QRamount = str(ovrcst)  # Specific amount

            upi_url = f"upi://pay?pa={upi_address}&pn=Recipient Name&tn=Payment Description&am={QRamount}"

            # Generate the QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(upi_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save("upi_qr.png")

            #******************PDF INVOICE STRUCTURE*******************
            c = canvas.Canvas("Invoice.pdf", pagesize=(200, 250), bottomup=0)
            c.setFillColorRGB(1.35, 0.45, 0.255)
            c.setFillColorRGB(0, 0, 0)
          
            c.line(5, 50, 195, 50)
            c.line(15, 102, 185, 102)
            c.line(35, 90, 35, 168)
            c.line(135, 90, 135, 168)
            c.line(115, 90, 115, 168)
            c.line(160, 90, 160, 168)
            c.line(15, 168, 185, 168)

            c.translate(10, 40)
            c.scale(1, -1)
            c.drawImage('Logo.png', 0, 10, width=50, height=15)

            c.scale(1, -1)
            c.translate(-10, -40)

            c.setFont("Times-Bold", 10)
            c.drawCentredString(125, 20, "INDUS INDIAN CUISINE")

            c.setFont("Times-Bold", 5)
            c.drawCentredString(125, 28, "Nr.Rancharda Village,Shilaj")
            c.drawCentredString(125, 34, "Ahmedabad, India")

            #*******Contact Info.************
            c.setFont("Times-Bold", 4)
            c.drawRightString(115, 40, "Phone No. :")
            c.drawRightString(146, 40, "+91 7874265233")
            c.drawString(101, 45, "E-mail : ")
            c.drawString(119, 45, "param.corpid@gmail.com")



            c.setFont("Times-Bold", 8)
            c.drawCentredString(100, 60, "BILL INVOICE DETAILS")

            c.setFont("Times-Bold", 5)

            c.drawRightString(80, 72, "Invoice No. :")
            c.drawRightString(100, 72, str('%06d' % number))

            c.drawRightString(80, 80, "Date :")
            c.drawRightString(155, 80, localtime)




            #Table & Column-Headings
            c.roundRect(15, 90, 170, 130, 2, stroke=1, fill=0)

            c.drawCentredString(25, 99, "S.No.")
            c.drawCentredString(75, 99, "Orders")
            c.drawCentredString(125, 99, "Price")
            c.drawCentredString(148, 99, "Qty.")
            c.drawCentredString(173, 99, "Total")

            c.setFillColorRGB(0.35, 0.45, 2.255)

            #******GETTING VALUES FROM DICTIONARY & Print in Invoice PDF********* 
            y_pos = 110
            srNo = 1
            for key,value in pdf.items():
                if value[0] > 0:
                    # print(key,value)
                    
                    c.drawCentredString(25, y_pos, str(srNo))
                    c.drawCentredString(75, y_pos, key)
                    c.drawCentredString(125, y_pos, str(value[1]))
                    c.drawCentredString(148, y_pos, str(value[0]))
                    c.drawCentredString(173, y_pos, str(value[2]))
                    y_pos+=10
                    srNo+=1

            #**********Bottom Section************************
            c.setFillColorRGB(0, 0, 0)
            c.drawRightString(152, 175, "Meal Cost(Total) : ")
            c.drawRightString(152, 181, "Service Cost : ")
            c.drawRightString(152, 187, "Tax(5% GST) : ")
            c.drawRightString(152, 193, "Total Tax : ")
            c.drawRightString(152, 205, "Grand Total : ")

            c.setFillColorRGB(0.35, 0.45, 2.255)
            c.drawRightString(180, 175, str(costofmeal))
            c.drawRightString(180, 181, str(Service))
            c.drawRightString(180, 187, str(PaidTax))
            c.drawRightString(180, 193, str(FTax))
            c.setFillColorRGB(1.35, 0.45, 0.255)
            c.drawRightString(180, 205, str(OverAllCost))

            
            c.setFillColorRGB(0, 0, 0)
            c.drawString(60, 230, "This is Computer generated invoice!!")

            #******Print QR code******
            c.drawString(30, 175, "Scan to Pay")
            c.drawImage("upi_qr.png", 25, 177, width=34, height=34)
            c.drawString(22, 215, f"Amount: {OverAllCost}")

            c.showPage()
            c.save()



        def csv_inc():
            Header = ['Order No', 'Fafda-Jalebi (500gm)', 'Gujarati Thali', 'Punjabi Thali', 'SouthIndian Tadka', 'Lassi (400ml)', 'Drink (200ml)',
                      'Cost Of Meal', 'Tax(GST)','Total Tax', 'Service charge', 'Final Cost']
            fname = 'Sample.csv'
            IsExist = os.path.exists(fname)
            print(IsExist)

            #***Logic : If the file exists then the value will be appended Otherwise New file will be created.
            if IsExist:
                with open('Sample.csv', 'a', newline='') as csvfile:
                    my_writer = DictWriter(csvfile, fieldnames=Header)
                    my_writer.writerow(dict)
                    global number
                    number += 1
                    lblreference.config(text=number)
                    reset()
            else:
                with open('Sample.csv', 'a', newline='') as csvfile:
                    my_writer = writer(csvfile)
                    my_writer.writerow(Header)
                    writer1 = DictWriter(csvfile, fieldnames=Header)
                    writer1.writerow(dict)
                    number += 1
                    lblreference.config(text=number)
                    reset()
            generate_invoice()

        #***********************Buttons Of calculator*****************************************************************************************
        btn7 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="7", bg="powder blue", command=lambda: btnclick(7))
        btn7.grid(row=2, column=0)

        btn8 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="8", bg="powder blue", command=lambda: btnclick(8))
        btn8.grid(row=2, column=1)

        btn9 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="9", bg="powder blue", command=lambda: btnclick(9))
        btn9.grid(row=2, column=2)

        Addition = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="+", bg="powder blue", command=lambda: btnclick("+"))
        Addition.grid(row=2, column=3)
        # ---------------------------------------------------------------------------------------------
        btn4 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="4", bg="powder blue", command=lambda: btnclick(4))
        btn4.grid(row=3, column=0)

        btn5 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="5", bg="powder blue", command=lambda: btnclick(5))
        btn5.grid(row=3, column=1)

        btn6 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="6", bg="powder blue", command=lambda: btnclick(6))
        btn6.grid(row=3, column=2)

        Substraction = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="-", bg="powder blue", command=lambda: btnclick("-"))
        Substraction.grid(row=3, column=3)
        # -----------------------------------------------------------------------------------------------
        btn1 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="1", bg="powder blue", command=lambda: btnclick(1))
        btn1.grid(row=4, column=0)

        btn2 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="2", bg="powder blue", command=lambda: btnclick(2))
        btn2.grid(row=4, column=1)

        btn3 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="3", bg="powder blue", command=lambda: btnclick(3))
        btn3.grid(row=4, column=2)

        multiply = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="*", bg="powder blue", command=lambda: btnclick("*"))
        multiply.grid(row=4, column=3)
        # ------------------------------------------------------------------------------------------------
        btn0 = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="0", bg="powder blue", command=lambda: btnclick(0))
        btn0.grid(row=5, column=0)

        btnc = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="c", bg="powder blue", command=clrdisplay)
        btnc.grid(row=5, column=1)

        btnequal = Button(f2, padx=16, pady=16, bd=4, width=16, fg="black", font=(
            'ariel', 20, 'bold'), text="=", bg="powder blue", command=eqals)
        btnequal.grid(columnspan=4)

        Decimal = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text=".", bg="powder blue", command=lambda: btnclick("."))
        Decimal.grid(row=5, column=2)

        Division = Button(f2, padx=16, pady=16, bd=4, fg="black", font=(
            'ariel', 20, 'bold'), text="/", bg="powder blue", command=lambda: btnclick("/"))
        Division.grid(row=5, column=3)

        # ---------------------------------------------------------------------------------------
        FJ = StringVar()
        GT = StringVar()
        PT = StringVar()
        ST = StringVar()
        Lassi = StringVar()
        Drink = StringVar()
        Subtotal = StringVar()
        Total = StringVar()
        Service_Charge = StringVar()
        Tax = StringVar()
        cost = StringVar()

        lblreference = Label(f1, font=('aria', 16, 'bold'),
                             text="Order No.", fg="steel blue", bd=10, anchor='w')
        lblreference.grid(row=0, column=0)
        lblreference = Label(f1, font=('aria', 16, 'bold'), text=str(
            number), fg="steel blue", bd=10, anchor='w')
        lblreference.grid(row=0, column=1)

        lblFJ = Label(f1, font=('aria', 16, 'bold'),
                      text="Fafda-Jalebi (500gm)", fg="steel blue", bd=10, anchor='w')
        lblFJ.grid(row=1, column=0)
        qFJ = Entry(f1, font=('ariel', 16, 'bold'), textvariable=FJ,
                    bd=6, insertwidth=4, bg="powder blue", justify='right')
        qFJ.grid(row=1, column=1)

        lblGT = Label(f1, font=('aria', 16, 'bold'),
                      text="Gujarati Thali", fg="steel blue", bd=10, anchor='w')
        lblGT.grid(row=2, column=0)
        qGT = Entry(f1, font=('ariel', 16, 'bold'), textvariable=GT,
                    bd=6, insertwidth=4, bg="powder blue", justify='right')
        qGT.grid(row=2, column=1)

        lblPT = Label(f1, font=('aria', 16, 'bold'),
                      text="Punjabi Thali", fg="steel blue", bd=10, anchor='w')
        lblPT.grid(row=3, column=0)
        qPT = Entry(f1, font=('ariel', 16, 'bold'), textvariable=PT,
                    bd=6, insertwidth=4, bg="powder blue", justify='right')
        qPT.grid(row=3, column=1)

        lblST = Label(f1, font=('aria', 16, 'bold'),
                      text="SouthIndian Tadka", fg="steel blue", bd=10, anchor='w')
        lblST.grid(row=4, column=0)
        qST = Entry(f1, font=('ariel', 16, 'bold'), textvariable=ST,
                    bd=6, insertwidth=4, bg="powder blue", justify='right')
        qST.grid(row=4, column=1)

        lblLassi = Label(f1, font=('aria', 16, 'bold'),
                         text="Lassi (400ml)", fg="steel blue", bd=10, anchor='w')
        lblLassi.grid(row=5, column=0)
        qLassi = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Lassi,
                       bd=6, insertwidth=4, bg="powder blue", justify='right')
        qLassi.grid(row=5, column=1)

        # --------------------------------------------------------------------------------------
        lblDrink = Label(f1, font=('aria', 16, 'bold'),
                         text="Drink (200ml)", fg="steel blue", bd=10, anchor='w')
        lblDrink.grid(row=0, column=2)
        qDrink = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Drink,
                       bd=6, insertwidth=4, bg="powder blue", justify='right')
        qDrink.grid(row=0, column=3)

        lblcost = Label(f1, font=('aria', 16, 'bold'),
                        text="Meal Cost", fg="steel blue", bd=10, anchor='w')
        lblcost.grid(row=1, column=2)
        txtcost = Entry(f1, font=('ariel', 16, 'bold'), textvariable=cost,
                        bd=6, insertwidth=4, bg="powder blue", justify='right')
        txtcost.grid(row=1, column=3)

        lblService_Charge = Label(f1, font=(
            'aria', 16, 'bold'), text="Service Charge", fg="steel blue", bd=10, anchor='w')
        lblService_Charge.grid(row=2, column=2)
        txtService_Charge = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Service_Charge,
                                  bd=6, insertwidth=4, bg="powder blue", justify='right')
        txtService_Charge.grid(row=2, column=3)

        lblTax = Label(f1, font=('aria', 16, 'bold'), text="Tax(5% GST)",
                       fg="steel blue", bd=10, anchor='w')
        lblTax.grid(row=3, column=2)
        txtTax = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Tax,
                       bd=6, insertwidth=4, bg="powder blue", justify='right')
        txtTax.grid(row=3, column=3)

        lblSubtotal = Label(f1, font=('aria', 16, 'bold'),
                            text="Total Tax", fg="steel blue", bd=10, anchor='w')
        lblSubtotal.grid(row=4, column=2)
        txtSubtotal = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Subtotal,
                            bd=6, insertwidth=4, bg="powder blue", justify='right')
        txtSubtotal.grid(row=4, column=3)

        lblTotal = Label(f1, font=('aria', 16, 'bold'),
                         text="Grand Total", fg="steel blue", bd=10, anchor='w')
        lblTotal.grid(row=5, column=2)
        txtTotal = Entry(f1, font=('ariel', 16, 'bold'), textvariable=Total,
                         bd=6, insertwidth=4, bg="powder blue", justify='right')
        txtTotal.grid(row=5, column=3)

        btnprint = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
            'ariel', 16, 'bold'), width=10, text="Print", bg="powder blue", command=csv_inc)
        # btnprint = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
        #     'ariel', 16, 'bold'), width=10, text="Print", bg="powder blue", command=csv_inc)
        btnprint.grid(row=8, column=0)

        # -----------------------------------------Buttons------------------------------------------
        lblTotal = Label(f1, text="---------------------", fg="white")
        lblTotal.grid(row=6, columnspan=3)

        btnTotal = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
            'ariel', 16, 'bold'), width=10, text="TOTAL", bg="powder blue", command=Ref)
        btnTotal.grid(row=7, column=1)

        btnreset = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
            'ariel', 16, 'bold'), width=10, text="RESET", bg="powder blue", command=reset)
        btnreset.grid(row=7, column=2)

        btnexit = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
            'ariel', 16, 'bold'), width=10, text="EXIT", bg="powder blue", command=qexit)
        btnexit.grid(row=7, column=3)

        def price():
            roo = Tk()
            roo.geometry("600x220+0+0")
            roo.title("Price List")
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="ITEM", fg="black", bd=5)
            lblinfo.grid(row=0, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="_____________", fg="white", anchor=W)
            lblinfo.grid(row=0, column=2)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="PRICE", fg="black", anchor=W)
            lblinfo.grid(row=0, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="Fafda-Jalebi (500gm)", fg="steel blue", anchor=W)
            lblinfo.grid(row=1, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="100", fg="steel blue", anchor=W)
            lblinfo.grid(row=1, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="Gujarati Thali", fg="steel blue", anchor=W)
            lblinfo.grid(row=2, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="110", fg="steel blue", anchor=W)
            lblinfo.grid(row=2, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="Punjabi Thali", fg="steel blue", anchor=W)
            lblinfo.grid(row=3, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="130", fg="steel blue", anchor=W)
            lblinfo.grid(row=3, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="SouthIndian Tadka", fg="steel blue", anchor=W)
            lblinfo.grid(row=4, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="150", fg="steel blue", anchor=W)
            lblinfo.grid(row=4, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="Lassi (400ml)", fg="steel blue", anchor=W)
            lblinfo.grid(row=5, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="70", fg="steel blue", anchor=W)
            lblinfo.grid(row=5, column=3)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="Drink (200ml)", fg="steel blue", anchor=W)
            lblinfo.grid(row=6, column=0)
            lblinfo = Label(roo, font=('aria', 15, 'bold'),
                            text="20", fg="steel blue", anchor=W)
            lblinfo.grid(row=6, column=3)

        btnprice = Button(f1, padx=16, pady=8, bd=10, fg="black", font=(
            'ariel', 16, 'bold'), width=10, text="Menu", bg="powder blue", command=price)
        btnprice.grid(row=7, column=0)


def main():
    # ==== create tkinter window
    root = Tk()

    # === creating object for class InvoiceGenerator
    obj = appWindow(root)

    # ==== start the gui
    root.mainloop()


if __name__ == "__main__":
    main()

'''
Fafda-Jalebi(500gm) -> 100
Gujarati Thali      -> 110
Punjabi Thali       -> 130
South-indian Thali  -> 150
Lassi(400ml)        -> 70
drink(200ml)        -> 20
'''
