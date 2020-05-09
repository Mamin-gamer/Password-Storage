from tkinter import *
from tkinter import messagebox
import hashlib
import os
import base64





objects = []
window = Tk()
window.withdraw()
window.title('Password Storage')

class StartWindow:

    def __init__(self):

        self.ts = Toplevel(window)
        self.ts.title('Option')
        self.ts.resizable(False, False)
        b1 = Button(self.ts, text = 'Login', command = self.login,font=('Courier', 20), width = 10).grid(column = 0, row = 0, pady = 20, padx = 20)
        b2 = Button(self.ts, text = 'Register', command = self.register,font=('Courier', 20), width = 10).grid(column = 1, row = 0, pady = 20, padx = 20)

    def login(self):
        self.attempts = 2
        self.ts.withdraw()
        self.tl = Toplevel(self.ts)
        self.tl.title('Login')

        l = Label(self.tl, text = 'Password:', font=('Courier', 14)).grid(row = 0, column = 0, pady = 20, padx = 20, sticky = 'e')
        self.entry_login = Entry(self.tl, show = '*',font=('Courier', 14), width = 20, bd = 3)
        self.entry_login.grid(row = 0, column = 1, padx = 20)
        b = Button(self.tl, text = 'Submit', font=('Courier', 18), command = self.login_submit).grid(row = 1, columnspan = 3, pady = 20)

    def login_submit(self):
        val = self.entry_login.get()
        if self.attempts!=0:
            if check_passwords(val):
                self.ts.destroy()
                window.deiconify()

            else:
                messagebox.showerror(title = 'Error', message = f'Incorrent password. You have got {self.attempts} attempts left')
                self.attempts-=1
                self.entry_login.delete(0, 'end')
        else:
            window.destroy()



    def register(self):
        self.ts.withdraw()
        self.tr = Toplevel(self.ts)
        self.tr.title('Register')

        l = Label(self.tr, text = 'Password:', font=('Courier', 14)).grid(column = 0, row = 0, pady = 20, padx = 20, sticky = 'e')
        l = Label(self.tr, text = 'Confirm Password:', font=('Courier', 14)).grid(column = 0, row = 1, pady = 20, padx = 20, sticky = 'e')

        self.p1 = Entry(self.tr, font=('Courier', 14), show = '*', bd = 3)
        self.p2 = Entry(self.tr, font=('Courier', 14), show = '*', bd = 3)

        self.p1.grid(column = 1, row = 0, padx = 20, pady = 20)
        self.p2.grid(column = 1, row = 1, padx = 20, pady = 20)

        b = Button(self.tr, text = 'Submit', font=('Courier', 14), command = self.register_submit).grid(columnspan = 3, row = 2, pady = 20, padx = 20)


    def register_submit(self):
        user = messagebox.askquestion(title = 'Confitmation', message = 'If you press "yes", details of previous owner would be deleted.\nDo you want to create an account?')
        if user == 'yes':
            reason, can_pass = password_verification(self.p1.get(), self.p2.get())
            if can_pass:
                store_password(p1.get())
                self.ts.destroy()
                window.deiconify()
            else:
                messagebox.showerror(title = 'Error', message = reason)
                self.p1.delete(0,'end')
                self.p2.delete(0,'end')
        else:
            self.tr.destroy()
            self.ts.deiconify()



class Display:
    def __init__(self, n, e, p, a, count):
        self.name = n
        self.email = e
        self.password = p
        self.ad = a
        self.c = count

        self.label_name = Label(window, text=self.name, font=('Courier', 14))
        self.label_email = Label(window, text=self.email, font=('Courier', 14))
        self.label_pass = Label(window, text=decrypt(self.password), font=('Courier', 14))
        self.label_add = Label(window, text=decrypt(self.ad), font=('Courier', 14))
        self.button = Button(window, text='X', fg='red', command=lambda: self.delete(self.c))

    def showup(self):
        self.label_name.grid(column = 0, row = 9 + self.c, pady = 5)
        self.label_email.grid(column = 1, row = 9 + self.c)
        self.label_pass.grid(column = 2, row = 9 + self.c)
        self.label_add.grid(column = 3, row = 9 + self.c)
        self.button.grid(column = 4, row = 9 + self.c, padx = 10)

    def delete(self, pos):

        user = messagebox.askquestion(title = 'Delete', message = 'Are you sure you want to delete this data?')
        if user == 'yes':
            for i in objects:
                i.destroy()
            with open('saves.txt', 'r') as file:
                all_lines = file.readlines()
            all_lines.pop(pos+1)


            with open('saves.txt', 'w') as file2:
                for line in all_lines:
                    file2.write(line)

            readfile()

    def destroy(self):
        self.label_name.destroy()
        self.label_email.destroy()
        self.label_pass.destroy()
        self.label_add.destroy()
        self.button.destroy()


def password_verification(p1, p2):
    if p1 == p2:
        if len(p1) > 6:
            capital = 0
            digit = 0
            lower = 0
            special = 0
            for character in str(p1):
                if character.isdigit():
                    digit+=1
                elif character.isupper():
                    capital+=1
                elif character in ['!', '?', '#', '%', '*', '^', '$', '`', '£', '(', ')', '&', '/', '_', '@', ':', ';', "№"]:
                    special+=1
                elif character.islower():
                    lower+=1
            if capital == 0 or digit == 0 or special == 0:
                return ('Password must contain at least 1 Capical letter, 1 Lowercase letter, 1 digit, 1 special symbol', False)        #password verification in many ways
            else:
                return None, True
        else:
            return ('Password is too short', False)
    else:
        return ('Passwords don`t match up', False)

def encrypt(text):
    return base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8')

def decrypt(text):
    missing_padding = 4 - len (text)% 4
    if missing_padding:
        text += ' = ' * missing_padding
    return base64.urlsafe_b64decode(text.encode('utf-8')).decode('utf-8')

def generate_hash(password, salt):
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        bytes(salt, 'utf-8'),
        100000
    )
    new_key = new_key.hex()
    return new_key

def store_password(password):
    salt = os.urandom(32).hex()
    key = generate_hash(password, salt)
    with open('saves.txt','w') as file:
        file.write(str(key))
        file.write('      ')
        file.write(str(salt))
        file.write('\n')


def check_passwords(password):
    with open('saves.txt', 'r') as file:
        line = (file.readline()).split()
    try:
        key = generate_hash(password,line[1])
        if key == line[0]:
            return True
        else:
            return False
    except:

        return False

def readfile():
    with open ('saves.txt', 'r') as file:
        count = 0
        _ = file.readline()
        for line in file:
            line = line.split('    ')
            e = Display(line[0], line[1], line[2], line[3], count)
            objects.append(e)
            e.showup()
            count+=1


def clicked():
    name = namee.get()
    email = emaile.get()
    password = passe.get()
    add = adde.get()
    with open('saves.txt', 'a') as file:
        line = name + '    ' + email + '    ' + encrypt(password) + '    ' + encrypt(add) + '\n'
        file.write(line)
    messagebox.showinfo(title = 'Added Successfully', message = 'Data has been added Successfully')
    readfile()

    namee.delete(0,'end')
    emaile.delete(0,'end')
    passe.delete(0,'end')
    adde.delete(0,'end')

StartWindow()


label = Label(window, text = 'Add Password', font=('Courier', 20)).grid(columnspan = 5, row = 0, pady = 20)
namel = Label(window, text = 'Name:', font=('Courier', 14))
namel.grid(column = 1, row = 1, pady = 20, padx = 20, sticky = 'e')
emaill = Label(window, text = 'Email:', font=('Courier', 14))
emaill.grid(column = 1, row = 2, pady = 20, padx = 20, sticky = 'e')
passl = Label(window, text = 'Password:', font=('Courier', 14))
passl.grid(column = 1, row = 3, pady = 20, padx = 20, sticky = 'e')
addl = Label(window, text = 'Aditional Info:', font=('Courier', 14))
addl.grid(column = 1, row = 4, pady = 20, padx = 20, sticky = 'e')

b = Button(window, text = 'Submit', font=('Courier', 16) , command = clicked).grid(columnspan = 5, row = 5, pady = 10)

namee = Entry(window, font=('Courier', 14),bd = 3, width = 30)
emaile = Entry(window, font=('Courier', 14),bd = 3, width = 30)
passe = Entry(window, font=('Courier', 14), show = '*',bd = 3, width = 30)
adde = Entry(window, font=('Courier', 14),bd = 3, width = 30)

namee.grid(column = 2, row = 1, padx = 10)
emaile.grid(column = 2, row = 2, padx = 10)
passe.grid(column = 2, row = 3, padx = 10)
adde.grid(column = 2, row = 4, padx = 10)

namel2 = Label(window, text='Name:', font=('Courier', 14)).grid(column = 0, row = 6, pady = 10, padx = 10)
emaill2 = Label(window, text='Email:', font=('Courier', 14)).grid(column = 1, row = 6, pady = 10, padx = 10)
passl2 = Label(window, text='Password:', font=('Courier', 14)).grid(column = 2, row = 6, pady = 10, padx = 10)
addl2 = Label(window, text='Aditional Info:', font=('Courier', 14)).grid(column = 3, row = 6, pady = 10, padx = 20)




readfile()

window.mainloop()
