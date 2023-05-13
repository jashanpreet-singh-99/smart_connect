import os
import time
import nltk
import socket
import requests
import pandas as pd

def get_ip_current_device():
    return socket.gethostbyname(socket.gethostname())

print(get_ip_current_device())
IP = get_ip_current_device()
# IP = 'linuxserver78559530.ddns.net'
# IP = '192.168.43.111'
PORT = '5000'

online_link = "http://" + IP + ":" + PORT + "/post_data/online"
s_c_link = "http://" + IP + ":" + PORT + "/check_status/"
g_c_d_link = "http://" + IP + ":" + PORT + "/get_command_data/"

post_reply_data = "http://" + IP + ":" + PORT + "/post_reply_data/"

path_data_link = 'http://' + IP + ':' + PORT + '/get_path_data/'
path_data_post_link = 'http://' + IP + ':' + PORT + '/path_data/'

default_state_post_link = 'http://' + IP + ':' + PORT + "/set_default_state/"
default_state_get_link = 'http://' + IP + ':' + PORT + "/get_default_state/"

upload_code_link = 'http://' + IP + ':' + PORT + "/post_code/"

print(online_link)
print(s_c_link)
print(g_c_d_link)
print(path_data_link)
print(path_data_post_link)
print(default_state_post_link)
print(default_state_get_link)

command_word_file = pd.read_csv(os.getcwd() + '/corpus/command_words.csv', index_col=0)
req_exp_file = list(command_word_file.Exp)

c_type = ['system', 'file', 'coding']   

folder_list = []
file_list = []

def convert_file_to_category(path) :
    global file_list, folder_list
    folder_list = []
    file_list = []
    json_data = {'path':path,'path_data':[]}
    path_data = os.listdir(path)
    for f_dir in path_data:
        if '.' in f_dir:
            f_type = 'file'
            file_list.append(f_dir)
        else:
            f_type = 'folder'
            folder_list.append(f_dir)
        json_data['path_data'].append({'type':f_type,'name':f_dir})
    print(json_data)
    return json_data

# SET UP PATH OF THE SERVER
requests.post(path_data_post_link, json=convert_file_to_category(os.getcwd()))
path = requests.get(path_data_link).json()['path'] + "/"

def reply(val) :
    requests.post(post_reply_data + val)

def create_multiplier_table() :
    
    # READ DATA FROM CSV
    corpus_data = pd.read_csv(os.getcwd() + '/corpus/command_expression.csv', index_col=0)
    category = set()
    
    def get_length_each_exp(value) :
        value = value.split("__")[1:-1]
        for t in value :
            category.add(t)
        return len(value)

    # ADD LENGTH COLUMN
    corpus_data['length'] = corpus_data.command_exp.apply(get_length_each_exp)
    corpus_data_features = corpus_data.iloc[:,[0, 2]].copy()
    
    # CREATE DIC WITH EACH CAT
    binary_data = dict((cat,[]) for cat in category)

    def get_feature_binary_data(value) :
        for cat in category :
            binary_data[cat].append(int(cat in value))

    # FILL THE BLANK DIC WITH BINARY DATA
    corpus_data.command_exp.apply(get_feature_binary_data)

    # CREATE COLUMN FOR EACH CAT
    for cat in category:
        corpus_data_features[cat] = binary_data[cat]

    corpus_data_features

    dic_multiplier = {}

    c_type = list(corpus_data_features.c_type.unique())

    dic_len = {}
    # FILL LENGTH DIC
    for c in c_type:
        dic_len[c] = corpus_data_features.length[corpus_data_features['c_type'] ==  c].sum()
    dic_multiplier['length'] = dic_len

    for col in category:
        total = corpus_data_features[col].value_counts()[1]
        dic_count = {}
        for c in c_type:
            try :
                dic_count[c] = corpus_data_features[col][corpus_data_features['c_type'] == c].value_counts()[1]/(total)
            except:
                dic_count[c] = 0
        dic_multiplier[col] = dic_count
    return dic_multiplier

"""
COMMAND FUNCTIONS
"""

supported_file_format = ['go','py','txt','java']
def open_folder(tag) :
    global path
    print(tag)
    if '.' in tag[0] :
        file_ext = tag[0].split('.')
        if file_ext[-1] in supported_file_format :
            if tag[0] not in file_list :
                reply("No Such File")
                return
            code = open(path+tag[0],'r').read()
            requests.post(upload_code_link, json={'code':code})
            switch_to_coding_mode()
            return
        else :
            reply("File Not SUpported Yet")
    if tag[1] == 'CD':
        if int(tag[0]) > len(folder_list) :
            print("NO SUCH DIR NUMBER")
            reply("no such directory found.")
            return
        folder = folder_list[int(tag[0]) - 1]
    else :
        folder = tag[0]
    if folder not in folder_list:
        if folder.capitalize() in folder_list :
            folder = folder.capitalize()
        elif folder.lower() in folder_list :
            folder = folder.lower()
        else :
            print("NO SUCH FOLDER")
            reply("no such directory found.")
            return
    path += folder + "/"
    reply("Opening Folder " + folder)
    requests.post(path_data_post_link, json=convert_file_to_category(path))
    
def go_back_dir() :
    global path
    print(path)
    if '/' == path :
        return
    path_exp = path[1:-1].split("/")[:-1]
    print(path_exp)
    path = "/"
    for p in path_exp:
        path += p + "/"
    print(path)
    reply("Going Back.")
    requests.post(path_data_post_link, json=convert_file_to_category(path))
    
def switch_to_file_mode() :
    requests.post(default_state_post_link + "1")
    print("FILE MODE")
    reply("Switching to File Mode")
    
def switch_to_sleep_mode() :
    requests.post(default_state_post_link + "0")
    print("SLEEP MODE")
    reply("Going to Sleep. Wake me up if u need anything.")
    
def switch_to_coding_mode() :
    requests.post(default_state_post_link + "2")
    print("CODING MODE")
    reply("Switching to Coding Mode")
    
def switch_to_specific_mode(mode) :
    if mode[0] == c_type[1]:
        switch_to_file_mode()
    elif mode[0] == c_type[2]:
        switch_to_coding_mode()
    else :
        switch_to_sleep_mode()
    print("Switch to ",mode)
    
function_list = [open_folder, go_back_dir, switch_to_file_mode, switch_to_sleep_mode, switch_to_specific_mode]

run = True

train = False

exp_file = set()

stop_word_file = {'file':['file','folder','number'],'system':[]}

def save_trained_expressions(exp_set, c_type) :
    command_co = pd.read_csv(os.getcwd() + "/corpus/command_expression.csv", index_col=0)
    command_corpus = command_co[command_co.c_type == c_type]
    command_corpus_list = list(command_corpus.command_exp)
    print("Present Commands : ",command_corpus_list)
    command_to_add = []
    for com in list(exp_set):
        if com not in command_corpus_list:
            command_to_add.append(com)
    print("NEW COMMANDS TO BE ADDED :",command_to_add)
    df = pd.DataFrame({'command_exp':command_to_add, 'c_type' : ([c_type]*(len(command_to_add)))})
    command_co = command_co.append(df, sort=True).copy()
    command_co.reset_index(inplace = True, drop=True)
    print(command_co)
    command_co.to_csv(os.getcwd() + "/corpus/command_expression.csv")

def do_training_exp(command) :
    global exp_file
    c_text = nltk.word_tokenize(command)
    tagged = nltk.pos_tag(c_text)
    exp = "__"
    for t in tagged :
        exp += t[1] + "__"
    print(exp)
    exp_file.add(exp)

def expression_analyser(exp, command_pos) :
    automaton = exp.split('__')[1:-1]
    i = 0
    state = 0
    command = []
    print(command_pos)
    for t in command_pos:
        if t[1] == automaton[i]:
            print(t[0])
            command.append(t[0])
            state = i + 1
            if i < len(automaton)  :
                i += 1
        if state == len(automaton):
            print('## accepted ##')
            break

def work_on_command(command) :
    dic_multiplier = create_multiplier_table()
    c_text = nltk.word_tokenize(command)
    tagged = nltk.pos_tag(c_text)
    expression_analyser('__JJ__NN__', tagged)
    """ CHANGE LEN WHEN REQUIRED """
    #  multi = [0] * len(c_type)
    multi = [0] * 2
    c_type = ['file', 'system']
    for v in tagged:
        for c_i,c_c in enumerate(c_type):
            try:
                multi[c_i] += dic_multiplier[v[1]][c_c]/dic_multiplier['length'][c_c]
            except:
                print("TAG NOT FOUND SO SKIPING")
                continue
    result_type = c_type[int(multi[1] > multi[0])]
    print(result_type)
    command_word = command_word_file[command_word_file.F_type == result_type]
    req_exp_file = list(command_word.Exp)
    required_arg_list = []
    stop_word = stop_word_file[result_type]
    for tag in tagged:
        if len(required_arg_list) > 0 :
            print("ARG", tag)
            if tag[1] in required_arg_list :
                if tag[0] in stop_word:
                    continue
                print("STATE 4 : FUNC : ")
                function_list[required_arg_list[-1]](tag)
                break
            continue
        print("STATE 1 : TAG : ",tag[1], " ", req_exp_file)
        if tag[1] in req_exp_file:
            dataframe = command_word[command_word.Exp == tag[1]]
            req_word_file = list(dataframe.Word)
            print("STATE 2 : WORD : ",req_word_file)
            for word in req_word_file:
                if word == tag[0] :
                    print("STATE 3 : ARGs : ",)
                    d = dataframe[dataframe.Word == tag[0]]
                    args = d.Args.values[0]
                    if args == 0 :
                        print("STATE 4 : FUNC : ", d.Func.values[0])
                        function_list[d.Func.values[0]]()
                        return
                    else :
                        required_arg_list = (d.Args_exp.values[0]).split(',')
                        print(required_arg_list)
                        required_arg_list.append(d.Func.values[0])
                        break
        reply("I was Never Taught AnyThing Like This.")

def server_data_fetch() :
    global run, train, c_type
    """ This Function is used to fetch Data from the Server """
    status_check = int(requests.get(s_c_link).text)
    if status_check :
        command = requests.get(g_c_d_link).text.strip()
        command = command[1:-1]
        print("Command Recived", command)
        """ TO QUIT AND SAVE TRAINED """
        if command == "qqqq" :
            if train :
                print('\n\n',exp_file)
                save_trained_expressions(exp_file, c_type)
            run = False 
        elif "train" in command:
            train = not train
            command_l = command.split(' ')
            if len(command_l) > 1 :
                c_type = command_l[-1]
                print("TRAINING IN ", c_type, " MODE")
        else :
            if not train:
                work_on_command(command)
            else :
                do_training_exp(command)

while run:
    server_data_fetch()
    time.sleep(0.01)