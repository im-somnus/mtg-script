import json, requests, os, re, datetime
 
def get_valid_filename(s): #makes a "good" filename to save the file (removes spaces and slashes, etc).
    return re.sub(r"(?u)[^-\w.^' :_,]", '%', s)

def get_valid_dir(s): 
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def checkdir(dir_path): #checks if the directory for the set already exists. If not it creates it.
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
 
def writefile(url, file_path): #checks if the file already exists. If not it downloads the image and creates the file.
    if not os.path.isfile(file_path):
        r = requests.get(url)
        open(file_path, 'wb').write(r.content)
 
def getallcardsdata(): #downloads the current all-cards.json file from scryfall. Just reads to memory, doesn't save it to a file.
                       #this part takes a while. If you're running the script and don't see any files being written for a bit, wait longer.
    request_url = requests.get('https://api.scryfall.com/bulk-data')
    request_data = requests.get(request_url.json()['data'][3]['download_uri'])
    return request_data.json()
 
start=datetime.datetime.now()
print("Writing files to " + os.path.join(os.getcwd(), "art"))
 
print("Starting at: " + str(start))
 
 
for card in getallcardsdata(): #reads each card in the all-cards file
    if card['lang'] == 'en': 
            #checks if it's an english card. checks if it's a standard set (or un set).
            #see all set types: https://scryfall.com/docs/api/sets 
        dir_path="art\\" + get_valid_dir(card['set_name'])
        checkdir(dir_path) #creates the set directory if it doesn't already exist
        if 'image_uris' in card: #if it's a regular card, writes the file
            file_path=dir_path + "\\" + get_valid_filename(card['name']) + " " + "(" + card['set'] + ")" + " " + card['collector_number']
            print(file_path)
        else:
            if 'type_line' in card:
                if card['type_line'] != 'Card // Card':
                    file_path=dir_path + "\\" + get_valid_filename(card['card_faces'][0]['name']) + " " + "(" + card['set'] + ")" + " " + card['collector_number'] + ' front'
                    print(file_path)
                    file_path=dir_path + "\\" + get_valid_filename(card['card_faces'][0]['name']) + " " + "(" + card['set'] + ")" + " " + card['collector_number'] + ' rear'
                    print(file_path)
            elif card['layout'] == 'reversible_card':	
                file_path=dir_path + "\\" + get_valid_filename(card['card_faces'][0]['name']) + " " + "(" + card['set'] + ")" + " " + card['collector_number'] + ' front'
                print(file_path)
                file_path=dir_path + "\\" + get_valid_filename(card['card_faces'][0]['name']) + " " + "(" + card['set'] + ")" + " " + card['collector_number'] + ' rear'
                print(file_path)
end=datetime.datetime.now()
print("Finished at " + str(end) + ". Elapsed time: " + str(end-start))
