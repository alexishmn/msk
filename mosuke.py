import json
import requests
from datetime import date, datetime
# import pasteboard

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m' 

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Variables
datesStr = ['2023-10-', '2023-11-', '2023-12-']
nbPsn = 2
lastday = 30

for datestr in datesStr:
    if datestr == '2023-10-':
        print("\n*************** OCTOBRE ***************\n")
        lastday = 31
    if datestr == '2023-11-':
        print("\n*************** NOVEMBRE ***************\n")
        lastday = 30
    if datestr == '2023-12-':
        print("\n*************** DECEMBRE ***************\n")
        lastday = 31

    list_rjson = []

    for d in range(1, lastday + 1):

        dateparam = datestr + f"{d:02d}"  
        dateformated = datetime.strptime(dateparam, "%Y-%m-%d")        

        if (dateformated < datetime.now()):            
            # print("la date est passée")
            continue 
        # print(dateparam)

        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://bookings.zenchef.com',
        'Referer': 'https://bookings.zenchef.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'restaurantId': '356054',
            'date_begin': dateparam,
            'date_end': dateparam,
        }

        response = requests.get('https://bookings-middleware.zenchef.com/getAvailabilities', params=params, headers=headers, verify=False)    

        list_rjson.append(response.json())

    # with open(f'outputfile{datestr}.json', 'w') as outf:
    #     for r in list_rjson:
    #         json.dump(r, outf)
    #     # outf.write(str(response.json()))    
    
    # print(list_rjson)
    allresas = {}    
    restoPossible = {}
    waitList = {}
    for day in list_rjson:  
        #Check if not WE
        if (len(day[0]['shifts']) != 0):    
            slots = day[0]['shifts'][0]['shift_slots']

            day = datetime.strptime(day[0]['date'], "%Y-%m-%d")
            dayFormated = day.strftime("%A %d. %B %Y")

            dispofortwoInSlot = []
            alldispoInSlot = []
            waitListInSlot = []

            for s in slots:                
                if (len(s['available_rooms']) != 0):
                    # print(day[0]['date'])
                    dispos = list(s['available_rooms'].keys())
                    alldispoInSlot.append(f"{s['slot_name']} : {dispos}")  
                    # print(f"{s['slot_name']} : {dispos}")

                    if (str(nbPsn) in dispos):
                        dispofortwoInSlot.append(s['slot_name'])
                        # restoPossible.append(day[0]['date'] + ' : ' + s['slot_name'])
                
                if len(dispofortwoInSlot) != 0:
                    restoPossible[dayFormated] = dispofortwoInSlot

                if len(alldispoInSlot) != 0:
                    allresas[dayFormated] = alldispoInSlot

                if (len(s['waitlist_possible_guests']) != 0):
                    waitListInSlot.append(s['slot_name'] + ' : ' + str(s['waitlist_possible_guests']))
                    # waitList.append(day[0]['date'] + ' - ' + s['slot_name'] + ' : ' + str(s['waitlist_possible_guests']))

                if len(waitListInSlot) != 0:
                    waitList[dayFormated] = waitListInSlot
                



    if (len(restoPossible) != 0):
        print('****************** DISPONIBILITES POUR 2 *********************')
        for d, r in restoPossible.items():
                print(bcolors.FAIL + d)
                [print(x) for x in r]
                print(bcolors.ENDC)
        # print([r for r in restoPossible]) 
    else:
        if len(waitList) != 0 :
            print("**************** EN LISTE D'ATTENTE **************")
            for d, w in waitList.items():
                print(d)
                [print(x) for x in w]
            # print([w for w in waitList]) 
        else:
            print('*********** AUCUNE DISPONIBILITE POUR 2 *************')

    
    print("************** VISUEL DE TOUTES LES DISPOS *******************")
    for d, r in allresas.items():
        print(d)
        [print(x) for x in r]
    # print([ar for ar in allresas])


    # pasteboard.set_string(restoPossible)


                
                