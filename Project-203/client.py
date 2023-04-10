import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected to the Server")

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.configure(bg="lightblue")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        
        self.pls = Label(self.login,text = "Please login to continue",justify = CENTER,font = "Helvetica 14 bold",bg="lightblue")
        self.pls.place( relheight = 0.15,relx = 0.2,rely = 0.07)
        self.labelName = Label(self.login,text = "Name: ",font = "Helvetica 12",bg="lightblue")
        self.labelName.place(relheight = 0.2,relx = 0.1,rely = 0.2)
        self.entryName = Entry(self.login,font = "Helvetica 14",bg="white")
        self.entryName.place(relwidth = 0.4,relheight = 0.12,relx = 0.35,rely = 0.2)
        self.entryName.focus()

        self.bttn=Button(self.login, text="Join Game", font = "Helvetica 14 bold",bg="lightgreen", command=lambda: self.goAhead(self.entryName.get()))
        self.bttn.place(relx=0.4,rely=0.5)

        self.count = 0
        
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.name=name
        self.layout()
    
    def layout(self):
        self.Window.deiconify()
        self.Window.title("!! QUIZ ROOM !!")
        self.Window.resizable(width = False,
							height = False)
        self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
        self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
        self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
        self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
        self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
        self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
        self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
        self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
        self.entryMsg.place(relwidth = 0.74,
							relheight = 0.04,
							rely = 0.008,
							relx = 0.011)
		
        self.entryMsg.focus()

        self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "lightgreen",
                                command = lambda: self.sendButton(self.entryMsg.get()))
		
        self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.04,
							relwidth = 0.22)
		
        self.textCons.config(cursor = "arrow")
		
        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight = 1,
						relx = 0.974)
		
        scrollbar.config(command = self.textCons.yview)
		
        self.textCons.config(state = DISABLED)
    
    def write(self, question):
        q=question
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, q+"\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        self.entryMsg.delete(0, END)

    def sendButton(self, msg):
        if self.count>0:
            message = msg
            client.send(message.encode('utf-8'))
            snd= Thread(target = self.write("You: "+message))
            snd.start()
        else:
            client.send(self.name.encode('utf-8'))
            self.count+=1

        self.entryMsg.focus()

        

g=GUI()

while True:
    data = client.recv(1024)
    if not data:
        break
    snd= Thread(target = g.write("Server: "+data))
    snd.start()
    
    # message = g.inp()    
    
    # client.send(message.encode('utf-8'))

client.close()