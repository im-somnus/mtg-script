import json, requests, os, re, datetime
 
def get_valid_filename(s):
    print("S before p: " + s)
    p = s
    if " // " in s:
        p = s.replace(" // ", "_%%_")
    print("S after p: " + p)
    return p

def checkdir(dir_path):
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

def writefile(url, file_path):
    if not os.path.isfile(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        r = requests.get(url)
        open(file_path, 'wb').write(r.content)
 
def getallcardsdata():
    request_url = requests.get('https://api.scryfall.com/bulk-data')
    request_data = requests.get(request_url.json()['data'][3]['download_uri'])
    return request_data.json()
 
start=datetime.datetime.now()
print("Writing files to " + os.path.join(os.getcwd(), "art"))
 
print("Starting at: " + str(start))
 
for card in getallcardsdata():
    if card['lang'] == 'en' and card['set'] in ['ncc', 'arn', 'rna']:
        dir_path="art/" + card['set_name']
        checkdir(dir_path) 
        if 'image_uris' in card:
            print("Calling from the card")
            file_path=dir_path + "\\" + get_valid_filename(card['name']) + "_" + "(" + card['set'] + ")" + "_" + card['collector_number'] + '.jpg'
            print(file_path)
            writefile(card['image_uris']['large'],file_path)
        else:
            if 'type_line' in card:
                if card['type_line'] != 'Card // Card':
                    file_path = os.path.join(dir_path, get_valid_filename(card['card_faces'][0]['name']) + "_" + "(" + card['set'] + ")" + "_" + card['collector_number']+ '_front.jpg')
                    writefile(card['card_faces'][0]['image_uris']['large'], file_path)
                    file_path = os.path.join(dir_path, get_valid_filename(card['card_faces'][0]['name']) + "_" + "(" + card['set'] + ")" + "_" + card['collector_number']+ '_rear.jpg')
                    writefile(card['card_faces'][1]['image_uris']['large'], file_path)
            elif card['layout'] == 'reversible_card':   
                file_path = os.path.join(dir_path, get_valid_filename(card['card_faces'][0]['name']) + "_" + "(" + card['set'] + ")" + "_" + card['collector_number']+ '_front.jpg')
                writefile(card['card_faces'][0]['image_uris']['large'], file_path)
                file_path = os.path.join(dir_path, get_valid_filename(card['card_faces'][0]['name']) + "_" + "(" + card['set'] + ")" +"_" + card['collector_number'] + '_rear.jpg')
                writefile(card['card_faces'][1]['image_uris']['large'], file_path)    

end=datetime.datetime.now()
print("Finished at " + str(end) + ". Elapsed time: " + str(end-start))
