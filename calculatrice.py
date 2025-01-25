import tkinter as tk
def click_button(value) :
    if value =="C" :
        display.delete(0,tk.END)
    elif value =="=" :
        try :
            resultat =eval(display.get())
            display.delete(0,tk.END)
            display.insert(0,str(resultat))
        except Exception :
            display.delete(0,tk.END)
            display.insert(0,"ERROR")
    else :
        display.insert(tk.END , value)
root =tk.Tk()
root.title("Calculatrice")
root.geometry("300x400")
root.resizable(False,False)
display = tk.Entry(root , font=("Arial" ,18) , borderwidth=5 , relief="ridge" , justify ="right")
display.pack(pady =10 , fill="both")

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

frame = tk.Frame(root)
frame.pack(expand=True , fill="both")

ligne , column = 0 , 0
for bouton in buttons :
    tk.Button(
    frame ,text=bouton , font=("Arial" ,18) , borderwidth=1 ,
    command=lambda x =bouton : click_button(x) ,
    bg ="lightgray" , fg="black" ,
    activebackground="darkgray" ,activeforeground="white"
    ).grid(row=ligne , column=column , sticky ="nsew" , ipadx =10 , ipady=10)

    column +=1
    if column >3:
        column =0
        ligne+=1
for i in range (4):
    frame.grid_rowconfigure(i,weight=1)
    frame.grid_columnconfigure(i,weight=1)


root.mainloop()





