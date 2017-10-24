###################
# Config section
###################
# folder:
folder=r'temp'

# file:
filename=r'datafile.json'

# output file:
output_csv=r'output.csv'

# I believe some servers detect when there are too many requests all at once,
# therefore, we're adding a random sleep in between using the following two
# variables; note that it is possible to set both values to 0 in order to
# avoid sleep altogether:
# sleep randomly from (in seconds):
random_sleep_from=0.1
# sleep randomly to (in seconds):
random_sleep_to=0.2
###################


####################
# Code:   
####################    
import os
import json
import time
import random
import urllib.request

print ('starting')

fullpath=os.path.join(folder, filename)
debugfile1=os.path.join(folder, 'debugfile1.txt')

# get the data and write it to file
if 1 == 1:
    print ('Fetching general data')
    with urllib.request.urlopen('https://fantasy.premierleague.com/drf/bootstrap-static') as request:
        request_data = request.read()
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    with open(fullpath, 'wb') as f:
        f.write(request_data)
    
    data = json.loads(request_data)
    with open(debugfile1, 'wt') as fDebug:
        fDebug.write(json.dumps(data, indent=4, sort_keys=True))
        
    print ('finished fetching general data which drives the rest of the process')


# retrieve files per player
if 1 == 1:
    print ('Retrieving all players data')
    
    with open(fullpath, 'rb') as f:
        request_data = f.read()
    
    data = json.loads(request_data)    
        
    elements_length = len(data['elements'])
    for i in range(elements_length):
        if i > 0:
            time.sleep(random.uniform(random_sleep_from, random_sleep_to))
            
        #print (data['elements'][i]['id'])
        with urllib.request.urlopen('https://fantasy.premierleague.com/drf/element-summary/' + str(data['elements'][i]['id'])) as request:
            request_data = request.read()

        player_file_no_extension = os.path.join(folder, str(data['elements'][i]['id']))
        with open(player_file_no_extension + '.json', 'wb') as f:
            f.write(request_data)
                
        onePlayerData = json.loads(request_data)
        with open(player_file_no_extension + '.txt', 'wt') as fDebug:
            fDebug.write(json.dumps(onePlayerData, indent=4, sort_keys=True))
    
#     elements_length = len(data['elements'])
#     for i in range(elements_length):
#         print (data['elements'][i]['web_name'])
    
#     #print (data)
#     print (data['phases'])
#     print ('finished printing parsed JSON')
#     
#     data_length = len(data['phases'])
#     for i in range(data_length):
#         print (data['phases'][i])

if 1 == 1:
    print ('Generating csv files')
    
    with open(os.path.join(folder, output_csv), "wt") as outputfile:
        
        headers = 'id,first_name,second_name,team,position'
        for j in range(38):
            headers += ',total_points ' + str(j+1) + ',value ' + str(j+1)
        #print (headers)
    
        outputfile.write(headers + '\n')
    
        with open(fullpath, 'rb') as f:
            request_data = f.read()
        
        data = json.loads(request_data)
            
        elements_length = len(data['elements'])
        for i in range(elements_length):
            playerId = data['elements'][i]['id']
            player_file_no_extension = os.path.join(folder, str(playerId))
            with open(player_file_no_extension + '.json', 'rb') as f:
                player_data = f.read()
                
            onePlayerData = json.loads(player_data)
            
            #print (str(data['elements'][i]['id']) + ',' + data['elements'][i]['first_name'] + ',' + data['elements'][i]['second_name']) # + ',' + onePlayerData['total_points'] + ',' + onePlayerData['value'])
            
            history_length = len(onePlayerData['history'])
            
            values=''
            
            for k in range(38):
                gotOne = False
                total_points = 0
                value = 0
                for j in range(history_length):
                    if (onePlayerData['history'][j]['round'] - 1) == k:
                        # incrementing total_points, but taking last value
                        total_points += onePlayerData['history'][j]['total_points']
                        value = onePlayerData['history'][j]['value']
                        #values += ',' + str(onePlayerData['history'][j]['total_points']) + ',' + str(onePlayerData['history'][j]['value'])
                        gotOne = True
                        #break
                    
                #if playerId == 12 and gotOne:
                #    print ('writing data for round ' + str(onePlayerData['history'][j]['round']))
                #    if k >= 38:
                #        print ('going past 38 to ' + str(k))
                #    if (onePlayerData['history'][j]['round'] - 1) >= 38:
                #        print ('round outside bounds: ' + str(onePlayerData['history'][j]['round']))
                       
                if gotOne: 
                    values += ',' + str(total_points) + ',' + str(value)
                else:
                    #if playerId == 12:
                    #    print('For 12, couldnt find id ' + str(k) + '\n')
                    values += ',,'
                
            #for j in range(history_length):
            #    values += ',' + str(onePlayerData['history'][j]['total_points']) + ',' + str(onePlayerData['history'][j]['value'])
                
            
            #print (str(data['elements'][i]['id']) + ',' + data['elements'][i]['first_name'] + ',' + data['elements'][i]['second_name'] + values)
            #print (playerId)
            teamId = data['elements'][i]['team']
            outputfile.write(str(data['elements'][i]['id']) + ',' + data['elements'][i]['first_name'] + ',' + data['elements'][i]['second_name'] + ',' + data['teams'][teamId-1]['name'] + ',' + values + '\n')
    
#data = json.load(request)
print ('done')