import tkinter as tk
import numpy as np
import requests
import socket
import os

def get_ip_current_device():
    return socket.gethostbyname(socket.gethostname())

ch = input("IS Client and server on same Machine : y/n  -> ")

if ch == 'n' :
	IP = input("IP address of the Server : example = 192.168.43.111}")
else :
	# IP = "linuxserver78559530.ddns.net"
	# IP = "192.168.43.111"
	IP = get_ip_current_device()

PORT = "5000"

online_link = "http://" + IP + ":" + PORT + "/post_data/online"
s_c_link = "http://" + IP + ":" + PORT + "/check_status/"
g_c_d_link = "http://" + IP + ":" + PORT + "/get_command_data/"

get_path_data_status_link = "http://" + IP + ":" + PORT + "/get_path_update_status/"  
get_path_data_link = "http://" + IP + ":" + PORT + "/get_path_data/"  

default_state_get_link = 'http://' + IP + ':' + PORT + "/get_default_state/"
default_state_post_link = 'http://' + IP + ':' + PORT + "/set_default_state/"

code_data_link = 'http://' + IP + ':' + PORT + "/get_code/"
code_update_check_link = 'http://' + IP + ':' + PORT + "/get_code_status/"

print(online_link)
print(s_c_link)
print(g_c_d_link)
print(get_path_data_status_link)
print(get_path_data_link)
print(default_state_get_link)
print(default_state_post_link)

state_list = ['Binary', 'File', 'Coding']

folder_list = ['folder'] * 20
file_list = ['file'] * 15
current_path = requests.get(get_path_data_link).json()['path'] + "/"

folder_img_path = os.getcwd() + "/assets/folder.png"
file_img_path = os.getcwd() + "/assets/file.png"

requests.post(default_state_post_link+"0")
default_state = 0
view_state = 1

window = tk.Tk()

width = 1440
height = 900

window.attributes("-fullscreen", True)

file_row_limit = 9

file_name = "Supported"

# PARENT CANVAS
canvas_parent = tk.Canvas(window, height=height, width=width, bg="#000000", highlightthickness=0)

# BINARY SCREEN CANVAS
canvas_binary = tk.Canvas(canvas_parent, height=0, width=0, bg="#000000", highlightthickness=0)
canvas_parent.create_window(0, 0, anchor=tk.NW, window=canvas_binary)
bin_t = canvas_binary.create_text( 2, 2, text=''.join(str(e) for e in np.random.randint(0, 2, 15500)), font='Time 10 bold', fill="#00ffff", anchor=tk.NW, width = 1438)

# FILE SCREEN CANVAS
canvas_file = tk.Canvas(canvas_parent, height=0, width=0, bg="#222222", highlightthickness=0)
canvas_parent.create_window(0, 0, anchor=tk.NW, window=canvas_file)


# CODING SCREEN CANVAS
canvas_code = tk.Canvas(canvas_parent, height=0, width=0, bg="#262831", highlightthickness=0)
canvas_parent.create_window(0, 0, anchor=tk.NW, window=canvas_code)
canvas_code_area = tk.Canvas(canvas_code, height=830, width=1400, bg="#313440", highlightthickness=0)
canvas_code.create_window(60, 50, anchor=tk.NW, window=canvas_code_area)
canvas_code.create_line(20, 30, 200, 30, width=40, fill="#313440")
canvas_code.create_text(110, 35, text=file_name, fill="#888888", anchor=tk.CENTER, font="courier 18")
canvas_code.create_line(20, 445, 60, 445, width=870, fill="#313440")
for val in range(29):
            canvas_code.create_text( 50, 77 + (val * 28), text=str(val + 1), fill="#4e5265",anchor=tk.E, font="courier 18")

canvas_data = [canvas_binary, canvas_file, canvas_code]
folder_img = tk.PhotoImage(file=folder_img_path)
file_img = tk.PhotoImage(file=file_img_path)

def draw_file_canvas_screen() :
    created = 0
    x_i = 0
    y_i = 100
    canvas_file.delete("all")
    canvas_file.create_line(420, 50, 1020, 50, width=50, fill="#666666")
    canvas_file.create_oval(395, 25, 445, 75, fill="#666666", outline="")
    canvas_file.create_oval(995, 25, 1045, 75, fill="#666666", outline="")
    canvas_file.create_text(720, 50, text=current_path, fill="#ffffff", anchor=tk.CENTER, font="courier 20")
    for folder in folder_list:
        i = created % file_row_limit
        j = created // file_row_limit
        canvas_file_f = tk.Canvas(canvas_file, height=120, width=150, bg="#222222", highlightthickness=0)
        canvas_file.create_window( (45 + i * 150) + x_i, (j * 120) + y_i, anchor=tk.NW, window=canvas_file_f)
        canvas_file_f.create_image(45,20, image=folder_img, anchor = tk.NW)
        canvas_file_f.create_text( 75, 95, text=folder, fill="#ffffff", anchor=tk.CENTER)
        created += 1
    for file in file_list:
        i = created % file_row_limit
        j = created // file_row_limit
        canvas_file_f = tk.Canvas(canvas_file, height=120, width=150, bg="#222222", highlightthickness=0)
        canvas_file.create_window( (45 + i * 150) + x_i, (j * 120) + y_i, anchor=tk.NW, window=canvas_file_f)
        canvas_file_f.create_image(45,20, image=file_img, anchor = tk.NW)
        canvas_file_f.create_text( 75, 95, text=file, fill="#ffffff", anchor=tk.CENTER)
        created += 1

def update_file_path_data(forced_start = False) :
    global current_path, folder_list, file_list
    """ Check if need to update folder or file meta data """
    if int(requests.get(get_path_data_status_link).text) or forced_start:
        path_dic = requests.get(get_path_data_link).json()
        current_path = path_dic['path']
        path_dic = path_dic['path_data']
        folder_list = []
        file_list = []
        for f_dir in path_dic :
            if f_dir['type'] == 'folder' :
                folder_list.append(f_dir['name'])
            else :
                file_list.append(f_dir['name'])
        print(current_path)
        print("FOLDER ", folder_list)
        print("FILE", file_list)
        draw_file_canvas_screen()
    if default_state != 1:
        return
    window.after(100, update_file_path_data)
    
def update_code_data(forced = False) :
    if int(requests.get(code_update_check_link).text) or forced :
        canvas_code_area.delete("all")
        code = requests.get(code_data_link).json()['code']
        code_list = code.split("\n")
        print(len(code_list))
        for val in range(29):
            if len(code_list) > val :
                print(code_list[val])
                canvas_code_area.create_text( 7, 17 + (val * 28), text=code_list[val], fill="#888888",anchor=tk.NW, font="courier 18")
    if default_state != 2:
        return
    window.after(500, update_code_data)
        
            
def update_binary_data() :
    """ Function to update the binary screen value with random values """
    canvas_binary.itemconfig(bin_t, text=''.join(str(e) for e in np.random.randint(0, 2, 15500)))
    if default_state >  0:
        return
    window.after(150, update_binary_data)

def switch_canvas_view() :
    """ Function to Change View State as per user requirement. """
    global view_state, default_state
    default_state = int(requests.get(default_state_get_link).text)
    if default_state != view_state :
        print("CHANGING VIEW ",view_state, " ==> ", default_state)
        canvas_data[view_state].config(width=0, height=0)
        canvas_data[default_state].config(width=width, height=height)
        view_state = default_state
        # SELECT APPROPRIATE DATA TO UPDATE
        if default_state == 0 :
            update_binary_data()
        elif default_state == 1 :
            update_file_path_data(True)
        elif default_state == 2 :
            update_code_data(True)
        else :
            update_binary_data()
    window.after(10, switch_canvas_view)

def server_data_fetch() :
    """ This Function is used to fetch Data from the Server """
    status_check = int(requests.get(s_c_link).text)
    if status_check :
        command = requests.get(g_c_d_link).text.strip()
        command = command[1:-1]
        print("Command Recived", command)
    window.after(250, server_data_fetch)
    
# CONTROL THE DISPLAY
switch_canvas_view()

# FETCH
server_data_fetch()
canvas_parent.pack()
tk.mainloop()