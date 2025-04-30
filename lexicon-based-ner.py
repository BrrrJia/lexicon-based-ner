import string
import regex as re
import nltk
import csv

def create_name_dict(name_first_file, name_last_file):
    with open(name_first_file,'r') as first_name, open (name_last_file,'r') as last_name:
        first_name_list = first_name.read().split('\n')
        last_name_list = last_name.read().split('\n')
        name_list = []
        for elem in first_name_list:
            name_list.append(elem)
        for elem in last_name_list:
            name_list.append(elem)
        abbr_name = ['A.','B.','C.','D.','E.','F.','G.','H.','I.','J.','K.','M.','N.','O.','P.','Q.','R.','S.','T.','U.','V.','W.','X.','Y.','Z.']
        for elem in abbr_name:
            name_list.append(elem)
        return name_list

def create_location_dict(location_file):
    with open(location_file,'r') as location:
        location = location.read().split('\n')
        location_list = []
        for elem in location:
            location_list.append(elem.strip(";").upper())
        return location_list
    
def create_time_dict():
    time = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','January','Feburary','March','April','May','June','July','August',
                'September','Octorber','November','December','First','Second']
    time_list = []
    for elem in time:
        time_list.append(elem.upper())
    return time_list

def read_text(text_file):
    with open(text_file,'r') as text:
        text = text.read().split('\n')
        sentence_list = []
        for sentence in text:
            sentence_new = sentence.strip()
            sentence_list.append(sentence_new)
    return sentence_list

def ner(name_first_file, name_last_file, text_file,location_file):
    name_list = create_name_dict(name_first_file, name_last_file)
    sentence_list = read_text(text_file)
    location_list = create_location_dict(location_file)
    time_list = create_time_dict()
    ner_dict = {}
    for sentence in sentence_list:
        token_list = nltk.word_tokenize(sentence)
        pos_tag = nltk.pos_tag(token_list)
        for token in token_list:
            if token.upper() not in location_list and token.upper() not in time_list:
                if re.match(r'NNPS?',pos_tag[token_list.index(token)][1]): #pos tag must be NNP or NNPS
                    if not token.islower():  
                        if not token.isupper() and token.upper() in name_list: 
                            if token_list.index(token) == 1 and len(token_list) >= 3 and not re.match(r'\d+(-\d+)?',token_list[2]) and not token_list[2] in string.punctuation: # case 1
                                next_token = token_list[2]
                                if re.match(r'NNPS?',pos_tag[2][1]):
                                    if next_token not in name_list and not next_token.islower():
                                        if next_token.upper() in name_list :
                                            token_fenster = [token, next_token]
                                        else:
                                            token_fenster = [token]
                                    else:
                                        token_fenster = [token]
                                else:
                                    token_fenster = [token]
                            elif token_list.index(token) == len(token_list)-1: #case 2: token at the end
                                previous_token =  token_list[-2]
                                if re.match(r'NNPS?',pos_tag[-2][1]):
                                    if previous_token not in name_list and not previous_token.islower():
                                        if previous_token.upper() in name_list :
                                            token_fenster = [previous_token, token]
                                        else:
                                            token_fenster = [token]
                                    else:
                                        token_fenster = [token]
                                else:
                                    token_fenster = [token]
                            else: #case 3: token in the middle
                                previous_token = token_list[token_list.index(token)-1]
                                next_token = token_list[token_list.index(token)+1]
                                token_fenster = [previous_token, token, next_token]
                                if re.match(r'NNPS?',pos_tag[token_list.index(token)-1][1]):
                                    if previous_token not in name_list and not previous_token.islower():
                                        if previous_token.upper() in name_list :
                                            token_fenster = [previous_token, token]
                                        elif re.match(r'NNPS?',pos_tag[token_list.index(token)+1][1]):
                                            if next_token not in name_list and not next_token.islower():
                                                if next_token.upper() in name_list :
                                                    token_fenster = [token, next_token]
                                                else:
                                                    token_fenster = [token]
                                            else:
                                                token_fenster = [token]
                                        else:
                                            token_fenster = [token]
                                    elif re.match(r'NNPS?',pos_tag[token_list.index(token)+1][1]):
                                        if next_token not in name_list and not next_token.islower():
                                            if next_token.upper() in name_list :
                                                token_fenster = [token, next_token]
                                            else:
                                                token_fenster = [token]
                                        else:
                                            token_fenster = [token]
                                    else:
                                        token_fenster = [token]    
                                elif re.match(r'NNPS?',pos_tag[token_list.index(token)+1][1]):
                                    if next_token not in name_list and not next_token.islower():
                                        if next_token.upper() in name_list :
                                            token_fenster = [token, next_token]
                                        else:
                                            token_fenster = [token]
                                    else:
                                        token_fenster = [token]
                                else:
                                    token_fenster = [token]
                                if token_list[0] in ner_dict:
                                    if token_fenster not in ner_dict[token_list[0]]:
                                        ner_dict[token_list[0]].append(token_fenster)
                                else: 
                                    ner_dict[token_list[0]] = [token_fenster]
    with open('ner_result.csv','w',newline='') as ner_result:
        csv_writer = csv.writer(ner_result,delimiter=';')
        for key,value in ner_dict.items():
            if len(value) == 1:
                csv_writer.writerow((key, value[0]))
            else:
                for elem in value:
                    csv_writer.writerow((key, elem))

if __name__ == '__main__':
    ner("first.txt", "last.txt", "sentences.txt",'location.txt')
