import tkinter

window = tkinter.Tk()
window.title("New title")
window.minsize(200, 100)
window.config(padx=20, pady=20)

def button_clicked():
    label_num["text"] = round(float(input.get())*1.609, 3)

input = tkinter.Entry(width=10)
input.grid(column=1, row=0)

#Label
label_miles = tkinter.Label(text="Miles", font=("Arial", 10, "italic"))
label_miles.grid(column=2, row=0)

label_equal = tkinter.Label(text="is equal to", font=("Arial", 10, "italic"))
label_equal.grid(column=0, row=1)

label_num = tkinter.Label(text="", font=("Arial", 10, "italic"))
label_num.grid(column=1, row=1)

label_km = tkinter.Label(text="Km", font=("Arial", 10, "italic"))
label_km.grid(column=2, row=1)

#Button
button = tkinter.Button(text="Calculate", command=button_clicked)
button.grid(column=1, row=2)

window.mainloop()