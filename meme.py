import json
import requests
import os
import shutil


#Creating necessary directories and files if they doesn't exist (eg. First run, Change location)
# if os.path.exists('AllMemes/') == False:
#     try:
#         os.mkdir('AllMemes')
#     except:
#         print("Can't create AllMemes directory, try running the program again")
if os.path.exists('MemesByPage/') == False:
    try:
        os.mkdir('MemesByPage')
    except:
        print("Can't create MemesByPage directory, try running the program again")
if os.path.exists('NewMemes') == False:
    try:
        os.mkdir('NewMemes')
    except:
        print("Can't create NewMemes directory. Try running the program again")

if os.path.exists('pages.json') == False:
    json_str = '''
    {
        "pages" : []
    }'''
    try:
        with open('pages.json', 'w') as f:
            f.write(json_str)
            f.close()
    except:
        print("Can't create pagelist file. Try running the program again.")


#returns content of a photo in binary from that photo post's url 
def get_photo_content(url):
    try:
        r = requests.get(url)
        evrr = r.text
        ind = evrr.find('data-ploi')
        evrr = evrr[ind+11:]
        ind = evrr.find('class')
        evrr = evrr[:ind-2]
        url = evrr.replace('&amp;','&')
        try:
            r = requests.get(url)
            return r.content
        except:
            print('Internal error occured while loading a image')
    except:
        print('Internal error occured while loading image url')


def show_pages():
    with open('pages.json') as f:
        data = json.load(f)
        pages = data['pages']
        for i, page in enumerate(pages):
            print(str(i), page['name'])

    print('')


def add_page():
    print("Please enter page link: ")
    link = input()
    link += '/'
    link = link[:link[link.find('.com/')+5:].find('/')+link.find('.com/')+5]
    if link[:-1] != '/':
        link += '/'
    try:
        r = requests.get(link+'photos/')
        evr = r.text
        ind = evr.find("pageTitle")
        evr = evr[ind+11:]
        ind = evr.find("Photos")
        evr = evr[:ind-3]
        page_name = evr
        try:
            f = open('pages.json')
            data = json.load(f)
            f.close()
            dic = {'name':page_name, 'link':link}
            if dic in data['pages']:
                print("Page already Exists")
            else:
                data['pages'].append(dic)
                f = open('pages.json', 'w')
                json.dump(data, f)
                f.close()
                if os.path.exists(f'{page_name}/') == False:
                    os.mkdir(f'MemesByPage/{page_name}')
                print("page added: ", page_name)
                

        except:
            print("Page not added!")
    except:
        print("Invalid Page")
    

def get_page_names():
    ans = []
    with open('pages.json') as f:
        data = json.load(f)
        pages = data['pages']
        for page in pages:
            ans.append(page['name'])
    return ans


def get_page_links():
    ans = []
    with open('pages.json') as f:
        data = json.load(f)
        pages = data['pages']
        for page in pages:
            ans.append(page['link'])
    return ans


def download_memes():
    print("Enter Number of memes to download (0 for all memes): ")
    x = input()
    try:
        if x == '':
            x = 1000
        elif int(x) == 0:
            x = 1000
        else:
            x = int(x)
    except:
        x = 1000
    counter = 0
    page_links = get_page_links()
    page_names = get_page_names()
    for i,page_link in enumerate(page_links):
        print("Downloading from ", page_names[i])
        try:
            #get the page response 

            photos_link = page_link + 'photos/'
            r = requests.get(photos_link)
            evr = r.text

            # get the needed json part of the response text
            ind = evr.find('posted_photos')
            evr = evr[ind-1:]
            ind = evr.find('sequence_number')
            evr = evr[:ind-4]
            evr = '{' + evr
            #load the data as json
            data = json.loads(evr)

            #get the list of the photos
            photos = data['posted_photos']['edges']
           
            #loop over every photo in that list
            for photo in photos:
                #get the photo url
                url = photo['node']['url']
                idd = str(photo['node']['id'])
                url.replace('&amp;', '&')
                if os.path.exists(f'MemesByPage/{page_names[i]}/') == False:
                    os.mkdir(f'MemesByPage/{page_names[i]}/')
                if os.path.exists(f'MemesByPage/{page_names[i]}/{idd}.jpg'):
                    continue
                photo_content = get_photo_content(url)
                if len(photo_content) > 20000:
                    with open(f'MemesByPage/{page_names[i]}/{idd}.jpg', 'wb') as img:
                        img.write(photo_content)
                        img.close()
                    with open(f'NewMemes/{idd}.jpg', 'wb') as img:
                        img.write(photo_content)
                        img.close()
                    print(f'image {idd} saved')
                    counter += 1
                if counter >= x:
                    return

        except:
            print('Invalid page link or no Network. Sorry')




#                Program starts here               

def remove_page():
    print('')
    show_pages()
    print("Enter page id/ids to remove (seperated by space): ")
    lst = input().split(' ')
    f = open('pages.json')
    data = json.load(f)
    f.close()
    for it in lst:
        try:
            data['pages'].pop(int(it))
            f = open('pages.json', 'w')
            json.dump(data, f)
            f.close()
        except:
            continue
    print("\n\n")
    print("Current pages: ")
    show_pages()
    print("Pages removed")


def clear_newmemes():
    shutil.rmtree('NewMemes')
    os.mkdir('NewMemes')
    print("\n   NewMemes folder cleared")


def delete_all_memes():
    shutil.rmtree('MemesByPage')
    os.mkdir('MemesByPage')
    print("\n   MemesByPage folder cleard")

while(1):

    print("   Welcome to automatic meme downloader   ")
    print("   ------------------------------------   ")
    print()
    print("Please select an option: ")
    print('''
        1) Download Memes
        2) Show listed pages
        3) Add new page
        4) Remove page/pages
        5) Clear NewMemes folder
        6) Clear MemesByPage Folder
        0) Exit
    ''')

    x = input()
    try:
        x = int(x)
    except:
        continue
    if x==1:
        download_memes()
    elif x==2:
        show_pages()
    elif x==3:
        add_page()
    elif x==4:
        remove_page()
    elif x==5:
        clear_newmemes()
    elif x==6:
        delete_all_memes()
    elif x==0:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("To report any bug or suggestion: send a mail")
        print("shafinohin04@gmail.com")
        print("\n Press enter to exit")
        x = input()
        break

    else:
        print("enter a valid number")

    print('')
    print('Press Enter to return ')
    x = input()

