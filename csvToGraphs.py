#!/usr/bin/python

# Author: Nick Aspiras
# Date: 6/21/2022
# Description: Converts CSV file to Necessary Graphs
import os
import csv
import re
import matplotlib.pyplot as plt
from numpy import NaN


def sliceNetworkValues(networkHold, mode):
    if networkHold != '' and networkHold.find("False") == -1 and networkHold.find("FALSE") == -1:
        networkHold = networkHold[0:len(networkHold) - 5].strip() #cuts off line number and any leading spaces
        if mode == 'RSRP':
            regex_str = re.compile("true", re.IGNORECASE)
            networkHold = regex_str.sub("", networkHold)
            regex_str = re.compile("[(]\d\d[)]", re.IGNORECASE)
            networkHold = regex_str.sub("", networkHold)
            regex_str = re.compile("dBm", re.IGNORECASE)
            networkHold = regex_str.sub("", networkHold)
            networkHold = networkHold.replace(",", "", 10)
            arr = networkHold.split(" ")
                
        else:
            arr = networkHold.split(" ")
            netStr = arr[0].replace("dB", "")
            arr = netStr.split(",")
        netArr = int(arr[0])
        return netArr
    return None

# NECESSARY TO CHANGE PATH TO CSV FILE ON SPECIFIC SYSTEM


# Command Line to run
# C:\Users\nicsl\Desktop\KCCTech\csvToGraphs\csvToGraphs.py

# terminal command to run for executable
# pyinstaller --onefile csvToGraphs.py

# C:\Users\nicsl\Desktop\KCCTech\csvToGraphs\data_one_hour.csv
# C:\Users\nicsl\Downloads\Interfreq 80.1 HO RSRP SINR RSRQ.csv



# intialize rows & columns
DLFrequency = []
timeStamp = []
RSRP = []
RSSI = []
RSRQ = []
SINR = []
PCI = []
headers = []
INFO = []
INFO_DISPLAY = []

Bytes =[]
TTL = []
ReturnTime = []

# open file
# Choose wireshark or cpe
input_source = input("\nPlease enter the source of the information (CPE, Wireshark, etc): ")
input_source = input_source.casefold()
while input_source != 'cpe' and input_source != 'wireshark':
    print("\nThe following Selection is incorrect")
    input_source = input("\nPlease enter the source of the information (CPE, Wireshark, etc): ")
    input_source = input_source.casefold()

file_name = input("\nPlease enter the file path of the csv file to graph: ")
works = False

# While the file is not valid, it will continue to ask for a file tor un
while works is False:
    try:
        with open(file_name, 'r') as file:
            file = file.read()
            works = True
    except IOError as e:
        print("\nThe following file cannot be found. Please try again\n")
        file_name = input("\nPlease enter the file path of the csv file to graph: ")
'''
ping_file_name = input("\nPlease enter the file path of the ping csv file you wish to use. Enter 'no' otherwise: ")
works = False

# While the file is not valid, it will continue to ask for a file tor un
while works is False:
    if(ping_file_name.lower() == 'no'):
        works = True
        ping_file_name = ''
    else:
        try:
            with open(ping_file_name, 'r') as file:
                file = file.read()
                works = True
        except IOError as e:
            print("\nThe following file cannot be found. Please try again\n")
            ping_file_name = input("\nPlease enter the file path of the csv file to graph: ")

iperf_file_name = input("\nPlease enter the file path of the iPerf csv file you wish to use. Enter 'no' otherwise: ")
works = False

# While the file is not valid, it will continue to ask for a file tor un
while works is False:
    if(iperf_file_name.lower() == 'no'):
        works = True
        iperf_file_name = ''
    else:
        try:
            with open(iperf_file_name, 'r') as file:
                file = file.read()
                works = True
        except IOError as e:
            print("\nThe following file cannot be found. Please try again\n")
            iperf_file_name = input("\nPlease enter the file path of the csv file to graph: ")

if iperf_file_name != '':
    protocolType = input("\nType TCP for a TCP Throughput Test or Type UDP for a UDP Througput Test: ")
    while(protocolType != 'TCP' and protocolType != 'UDP'):
        print("\nThe following response is incorrect. Please try again\n")
        protocolType = input("\nType TCP for a TCP Throughput Test or Type UDP for a UDP Througput Test: ")
    testType = input("\nType DL for a DL Throughput Test or Type UL for a UL Througput Test: ")
    while(protocolType != 'DL' and protocolType != 'UL'):
        print("\nThe following response is incorrect. Please try again\n")
        testType = input("\nType DL for a DL Throughput Test or Type UL for a UL Througput Test: ")


'''
# Clear Command Prompt
try:
    os.system('cls')
except:
    os.system('clear')


# Open .csv file for reading

with open(file_name,'r') as csvfile:

    lines = csv.reader(csvfile, delimiter=',')
    idx = 0
    totalSeconds = 0
    headersSet = False
    isPCIEmpty = False
    index = 0
    lastTimeStamp = ''
    for row in lines:
        # Append Data Values if it is not the first row
        if headersSet is True:
            try:
                # except will be hit if fullRow statement fails 
                if input_source == 'cpe':
                    fullRow = float(row[1])
                    timeStamp.append(row[0])
                    RSRP.append(int(row[5]))
                    RSSI.append(int(row[6]))
                    RSRQ.append(int(row[7]))
                    SINR.append(int(row[8]))
                    PCI.append(int(row[9]))
                    totalSeconds = totalSeconds + 3
                elif input_source == 'wireshark':
                    fullRow = int(row[0])
                    # if get past here, there still is another row
                    tstamp = row[1].replace(",", ":")
                    '''
                    timeStamp.append(tstamp)
                    if row[6] != '' and row[7] != '':
                        isPCIEmpty = False
                        if len(row[6]) > 3:
                            arr = row[6].split(',')
                            arr = [int(x) for x in arr]
                            PCI.append(arr[0])
                        else:
                            PCI.append(int(row[6]))
                    else:
                        isPCIEmpty = True    

                    if isPCIEmpty is False:
                        networkHold = sliceNetworkValues(row[7], 'RSRP')
                        if networkHold is None:
                            networkHold = NaN
                        RSRP.append(networkHold)
                        networkHold = sliceNetworkValues(row[8], 'SINR')
                        if networkHold is None:
                            networkHold = NaN
                        SINR.append(networkHold)
                        networkHold = sliceNetworkValues(row[9], 'RSRQ')
                        if networkHold is None:
                            networkHold = NaN
                        RSRQ.append(networkHold)
                        INFO.append(row[10])
                        if row[10] not in INFO_DISPLAY :
                            INFO_DISPLAY.append(row[10])
                    '''
                    timeStamp.append(tstamp)
                    if(row[6] == ''):
                        PCI.append(NaN)
                    else:
                        if len(row[6]) > 3:
                            arr = row[6].split(',')
                            arr = [int(x) for x in arr]
                            PCI.append(arr[0])
                        else:
                            PCI.append(int(row[6]))
                    networkHold = sliceNetworkValues(row[7], 'RSRP')
                    if networkHold is None:
                        networkHold = NaN
                    RSRP.append(networkHold)
                    networkHold = sliceNetworkValues(row[8], 'SINR')
                    if networkHold is None:
                        networkHold = NaN
                    SINR.append(networkHold)
                    networkHold = sliceNetworkValues(row[9], 'RSRQ')
                    if networkHold is None:
                        networkHold = NaN
                    RSRQ.append(networkHold)
                    INFO.append(row[10])
                    if row[10] not in INFO_DISPLAY :
                        INFO_DISPLAY.append(row[10])
                
                    totalSeconds = totalSeconds + 1
                else:
                    print('no')
            # If except is hit, all data has been read    
            except:
                break
            
        # Append Headers for Data Values
        else:
            # Set headersSet to true to set them
            headersSet = True
            if input_source == 'cpe':
                
                # Append Time Stamp header
                headers.append(row[0])

                # Append Necessary Headers
                for i in range(4):
                    headers.append(row[i + 5])
                headers.append('PCI')
            elif input_source == 'wireshark':
                # Append Time Stamp header
                headers.append(row[1])

                # Append Necessary Headers
                for i in range(3):
                    headers.append(row[i + 7].upper())
                headers.append('PCI')
        idx += 1
# protocolType , testType
# Ping Test Split
'''
with open(ping_file_name,'r') as csvfile:

    lines = csv.reader(csvfile, delimiter=',')
    first = 0
    for row in lines:
        if(first != 0):
            Bytes.append(row[1])
            TTL.append(row[3])
            ReturnTime.append(row[4])
        else:
            first = 1
# iPerf Test Split
# All
interval = []
transfer = []
bitrate = []
# TCP
retr = []
sendRecieve = []
# TCP UL
cwnd = []
# UDP
lostAndTotalDiagrams = []
# UDP DL
jitter = []
  
with open(iperf_file_name,'r') as csvfile:

    lines = csv.reader(csvfile, delimiter=',')
    first = 0
    for row in lines:
        if(first != 0):
            interval.append(row[1])
            transfer.append(row[2])
            bitrate.append(row[3])
            if(protocolType == "TCP"):
                retr.append(row[4])
                if(testType == "UL"):
                    cwnd.append(row[4])
                    sendRecieve.append(row[5])
                else:
                    sendRecieve.append(row[4])
            else:
                if(testType == "UL"):
                    lostAndTotalDiagrams.append(row[4])
                else:
                    jitter.append(row[4]);
                    lostAndTotalDiagrams.append(row[5])
        else:
            first = 1
'''
# These values hold the first and last possible time stamps
# as well as calculating the max amount of minutes you can check
firstTimeStamp = timeStamp[0]
lastTimeStamp = timeStamp[len(timeStamp) - 1]
maxMinutes = totalSeconds / 60

run = False
while run is False:
    try:
        os.system('cls')
    except:
        os.system('clear')
    
    
    # Choice Handler (Handles Incorrect)
    print("Hit 'Enter' to submit your selection\n")
    print("Type 1 to choose by Time Stamp\nType 2 to choose by Number of Minutes\nType 3 to select Ranges of Time Stamps")
    print("Type 4 to select using threshold or offset\nType 5 to select by Information (if using Wireshark method)\n")
    choice = input("Selection: ")
    while choice != '1' and choice != '2' and choice != '3' and choice != '4' and choice != '5':
        print("\n\n\nThe following selection is incorrect.")
        print("Hit 'Enter' to submit your selection\n")
        print("Type 1 to choose by Time Stamp\nType 2 to choose by Number of Minutes\nType 3 to select Ranges of Time Stamps")
        print("Type 4 to select using threshold or offset\nType 5 to select by Information (if using Wireshark method)\n")
        choice = input("Selection: ")

    # Clear Console after Selection
    
    try:
        os.system('cls')
    except:
        os.system('clear')


    # Intialize all the necessary variables we need
    isTimeStamp = False
    isMinutes = False
    chooseTimeStamp = False
    isThreshold = False
    isInfoTab = False
    tableIndex = 0
    startIndex = 0
    endIndex = 9 + 1

    if choice == '1':
        # Handling Time Stamp Here
        isTimeStamp = True
        print("\n")
        for i in timeStamp:
            print(i)
        print("Please type 'cancel' at any time to go back to the original menu.\n\n")
        startIndex = input("\nPlease Enter an Starting Time Stamp in the form HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")

        # Check if the input time stamp is valid
        while len(startIndex) == 0 or any(startIndex in string for string in timeStamp) is False:
            if startIndex == 'cancel':
                break
            print("\n\n\nThe following selection is incorrect.")
            startIndex = input("\nPlease Enter an Starting Time Stamp in the form HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
        if startIndex != 'cancel':
            run = True
            startIndexString = startIndex
            result = [string for string in timeStamp if startIndex in string]
            startIndex = timeStamp.index(result[0])

        if startIndex != 'cancel':
            # End Index
            endIndex = input("\nPlease Enter an Ending Time Stamp in the form HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
    
            # Check if the input time stamp is valid
            while len(endIndex) == 0 or startIndexString > endIndex or any(endIndex in string for string in timeStamp) is False:
                if endIndex == 'cancel':
                    run = False
                    break
                print("\n\n\nThe following selection is incorrect.")
                endIndex = input("\nPlease Enter an Ending Time Stamp in the form HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
            if endIndex != 'cancel':
                run = True
                result = [string for string in timeStamp if endIndex in string]
                endIndex = timeStamp.index(result[0]) + 1
       

    if choice == '2':
        # Handling Number of Minutes
        isMinutes = True
        print("Please type 'cancel' at any time to go back to the original menu.\n\n")
        numOfMinutes = input("Please enter the number of minutes that you would like to capture or type 'all' if you would like all values\nNumber of Minutes: ")

        # Check if the input minutes is valid
        if numOfMinutes.strip() != 'all' and numOfMinutes.strip() != 'cancel':
            while len(numOfMinutes.strip()) == 0 or float(numOfMinutes) > 0 and float(numOfMinutes) > maxMinutes:
                print("\n\n\nThe following selection is incorrect.")
                numOfMinutes = input("\nPlease enter the number of minutes that you would like to capture\nNumber of Minutes: ")
        if numOfMinutes.strip() != 'cancel':
            run = True
            

    if choice == '3':
        # Handling Select Time Stamp
        chooseTimeStamp = True
        print("Please type 'cancel' at any time to go back to the original menu.\n\n")
        print("\nThe First Time Stamp is: ")
        print(firstTimeStamp)
        print("\nThe Last Time Stamp is: ")
        print(lastTimeStamp)
        print("\nEnter 'done' at entering beginning range to print ranges")
        print(timeStamp)
        ranges = []
        beginningRange = ''
        endingRange = ''
        print("Please type 'cancel' at any time to go back to the original menu.\n\n")
        while beginningRange != 'done' and endingRange != 'cancel':
            beginningRange = input("\nPlease enter the beginning of this range in the form: HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
            # beginningRange != 'done': checks to see if user is done inputting values
            while len(beginningRange) > 0 and beginningRange != 'cancel' and beginningRange != 'done' and any(beginningRange in string for string in timeStamp) is False:
                print("\n\n\nThe following selection is incorrect.")
                beginningRange = input("\nPlease enter the beginning of this range in the form: HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
            if beginningRange == 'done' or beginningRange == 'cancel':
                break
            result = [string for string in timeStamp if beginningRange in string]
            begin = timeStamp.index(result[0])

            endingRange = input("\nPlease enter the ending of this range in the form: HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")

            # beginningRange > endingRange: checks to ensure your range is valid for beginning to end
            while len(endingRange) > 0 and endingRange != 'cancel' and beginningRange > endingRange and any(endingRange in string for string in timeStamp) is False:
                print("\n\n\nThe following selection is incorrect.")
                endingRange = input("\nPlease enter the ending of this range in the form: HH:MM:SS AM|PM\nExamples: 5:11:22 AM, 11:32:12 PM\nTime Stamp: ")
            if endingRange != 'cancel':
                result = [string for string in timeStamp if endingRange in string]
                end = timeStamp.index(result[0]) + 1
                ranges.append([begin, end])
                run = True
            

    if choice == '4':
        # Handles Thresholds
        isThreshold = True
        firstThreshold = ''
        secondThreshold = ''
        print("Please type 'cancel' at any time to go back to the original menu.\n\n")
        print("Which Threshold KPI do you want to use?")
        print("\nPlease type '0' for RSRP, type '2' for RSRQ, or type '3' for SINR\n")
        thresholdKPI = input("Selection: ")
        while thresholdKPI != '0' and thresholdKPI != '2' and thresholdKPI != '3' and thresholdKPI != 'cancel':
            print("\nThe following selection does not exist.\n")
            print("Which Threshold KPI do you want to use?")
            print("\nPlease type '0' for RSRP, type '2' for RSRQ, or type '3' for SINR\n")
            thresholdKPI = input("Selection: ")
        if thresholdKPI != 'cancel':
            thresholdKPI = int(thresholdKPI)
            if thresholdKPI == 0:
                firstThreshold = input("\n\nPlease enter the first threshold or offset (in dBm): ")
            else:
                firstThreshold = input("\n\nPlease enter the first threshold or offset (in dB): ")
            while(len(firstThreshold) < 0):
                    print("Please enter a valid threshold or offset\n")
                    if thresholdKPI == 0:
                        firstThreshold = input("\n\nPlease enter the first threshold or offset (in dBm): ")
                    else:
                        firstThreshold = input("\n\nPlease enter the first threshold or offset (in dB): ")

            if firstThreshold != 'cancel':
                isTwoThresholds = input("\nWould you like to enter a second threshold or offset?\nType Yes or No: ")
                while isTwoThresholds.casefold() != 'yes' and isTwoThresholds.casefold() != 'no' and isTwoThresholds.casefold() != 'cancel':
                    print("\nThe following selection does not exist.\n")
                    isTwoThresholds = input("\nWould you like to enter a second threshold or offset?\nType Yes or No: ")
                if isTwoThresholds.casefold() == 'yes':
                    if thresholdKPI == 0:
                        secondThreshold = input("\n\nPlease enter the second threshold or offset (in dBm): ")
                        
                    else:
                        secondThreshold = input("\n\nPlease enter the second threshold or offset (in dB): ")
                    while(len(secondThreshold) < 0):
                        print("Please enter a valid threshold or offset\n")
                        if thresholdKPI == 0:
                            secondThreshold = input("\n\nPlease enter the second threshold or offset (in dBm): ")
                        
                        else:
                            secondThreshold = input("\n\nPlease enter the second threshold or offset (in dB): ")

                if isTwoThresholds.casefold() != 'cancel' and secondThreshold != 'cancel':
                    if isTwoThresholds.casefold() == 'yes':
                        isTwoThresholds = True
                    else:
                        isTwoThresholds = False
                    run = True
    if choice == '5':
        if input_source != 'wireshark':
            print("\nThe current input file/source is not from Wireshark. You can't use this option")
            run = False
        else:
            for i in INFO_DISPLAY:
                if i.find('Standard query') < 0:
                    print(i)
            print("\nPlease type 'cancel' at any time to go back to the original menu.")
            print("\nPlease enter each signaling information tab one by one.")
            infoResponse = ''
            infoTab = []
            while infoResponse.casefold() != 'done' and infoResponse.casefold() != 'cancel':
                print("\nWhich Information Tab would you like to graph from? Type 'done' when finished\n")
                infoResponse = input("Selection: ")
                while infoResponse.casefold() != 'done' and infoResponse.casefold() != 'cancel' and infoResponse not in INFO_DISPLAY:
                    print("\nThe following is an incorrect reponse.\n")
                    print("\nWhich Information Tab would you like to graph from? Type 'done' when finished\n")
                    infoResponse = input("Selection: ")
                if infoResponse.casefold() != 'done' and infoResponse.casefold() != 'cancel' :
                    infoTab.append(infoResponse)
            if len(infoTab) > 0 and infoResponse.casefold() != 'cancel':
                isInfoTab = True
                run = True
            else:
                run = False


# Check to see if the user wants to display values
displayValues = False

choice = input("\nWould you like to display the values on the graph? Enter Yes or No.\nSelection: ")
while(choice.casefold() != 'yes' and choice.casefold() != 'no'):
    print("The following response was incorrect.\n\n")
    choice = input("\nWould you like to display the values on the graph? Enter Yes or No.\nSelection: ")

# if answer choice is yes (case-insensitive)
if choice.casefold() == 'yes':
    displayValues = True






# GRAPH SETTINGS BELOW

if input_source == 'cpe':
    # table holds each of the data values, assorted by their name
    table = [RSRP, RSSI, RSRQ, SINR, PCI]


    # Create a figure and four 1-D subplots
    fig, ax = plt.subplots(4, 1, sharex=True)

    # Setup figures to maximize fit
    fig.subplots_adjust(left=0.035,
                        bottom=0.124, 
                        right=0.990, 
                        top=0.953, 
                        wspace=0.200, 
                        hspace=0.321)



    #Edit Graphing
    if isMinutes is True:
        if numOfMinutes == 'all':
            numOfMinutes = maxMinutes
        tableIndex = int(float(numOfMinutes) * 60 / 3)
        endIndex = tableIndex


    for i in range(4):

        newTable = table[i]
        newPCITable = table[4]
        x_values = []
        y_network_values = []
        y_pci_values = []
        if chooseTimeStamp is True:
            # for every range of timestamps
            for j in ranges:
                # for each time stamp
                for k in range(len(timeStamp[j[0]:j[1]])):
                    x_values.append(timeStamp[j[0]:j[1]][k])
                    y_network_values.append(newTable[j[0]:j[1]][k])
                    y_pci_values.append(newPCITable[j[0]:j[1]][k])
        elif isThreshold is True:
            for k in range(len(timeStamp)):
                if table[thresholdKPI][k] == int(firstThreshold):
                    x_values.append(timeStamp[k])
                    y_network_values.append(newTable[k])
                    y_pci_values.append(newPCITable[k])
                else:
                    if isTwoThresholds is True:
                        if table[thresholdKPI][k] == int(secondThreshold):
                            
                            x_values.append(timeStamp[k])
                            y_network_values.append(newTable[k])
                            y_pci_values.append(newPCITable[k])
        else:
            x_values = timeStamp[startIndex:endIndex]
            y_network_values = newTable[startIndex:endIndex]
            y_pci_values = newPCITable[startIndex:endIndex]
        # Create Plot with X: Time Stamp, Y: Network Value, Color: Green, LineStyle: Solid, Label: Label of Value
        ax[i].plot(x_values, y_network_values, color = 'g', linestyle = 'solid', label = headers[i+1], marker='o')

        
        # Create Plot with X: Time Stamp, Y: PCI, Color: Blue, LineStyle: Solid, Label: Label of PCI
        ax[i].plot(x_values, y_pci_values, color = 'b', linestyle = 'solid', label = headers[5], marker='o')

        if displayValues is True:

            for x,y in zip(x_values, y_network_values):
                label = "{:d}".format(y)

                ax[i].annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,5), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
            for x,y in zip(x_values, y_pci_values):
                label = "{:d}".format(y)

                ax[i].annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,5), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
        # Set Plot to rotate X Axis at a 45 Degree Angle (To See Time Stamps Easier)
        ax[i].tick_params('x', labelrotation=45, labelsize=8)

        # Set Title of Plot as Label of Value
        ax[i].set_title(headers[i+1], fontsize = 12)

        # Intialize a Legend and Grid
        ax[i].legend()
        ax[i].grid()

elif input_source == 'wireshark':
    # table holds each of the data values, assorted by their name
    table = [RSRP, RSRQ, SINR, PCI]


    # Create a figure and four 1-D subplots
    fig, ax = plt.subplots(3, 1, sharex=True)

    # Setup figures to maximize fit
    fig.subplots_adjust(left=0.035,
                        bottom=0.124, 
                        right=0.990, 
                        top=0.953, 
                        wspace=0.200, 
                        hspace=0.321)



    #Edit Graphing
    if isMinutes is True:
        if numOfMinutes == 'all':
            numOfMinutes = maxMinutes
        tableIndex = int(float(numOfMinutes) * 60)
        endIndex = tableIndex


    for i in range(3):

        newTable = table[i]
        newPCITable = table[3]
        x_values = []
        y_network_values = []
        y_pci_values = []
        if chooseTimeStamp is True:
            # for every range of timestamps
            for j in ranges:
                # for each time stamp
                for k in range(len(timeStamp[j[0]:j[1]])):
                    x_values.append(timeStamp[j[0]:j[1]][k])
                    y_network_values.append(newTable[j[0]:j[1]][k])
                    y_pci_values.append(newPCITable[j[0]:j[1]][k])
        elif isThreshold is True:
            for k in range(len(timeStamp)):
                if table[thresholdKPI][k] == int(firstThreshold):
                    x_values.append(timeStamp[k])
                    y_network_values.append(newTable[k])
                    y_pci_values.append(newPCITable[k])
                else:
                    if isTwoThresholds is True:
                        if table[thresholdKPI][k] == int(secondThreshold):
                            
                            x_values.append(timeStamp[k])
                            y_network_values.append(newTable[k])
                            y_pci_values.append(newPCITable[k])
        elif isInfoTab is True:
            for j in range(len(INFO)):
                for info in infoTab:
                    if INFO[j] == info:
                        x_values.append(timeStamp[j])
                        y_network_values.append(newTable[j])
                        y_pci_values.append(newPCITable[j])
        else:
            x_values = timeStamp[startIndex:endIndex]
            y_network_values = newTable[startIndex:endIndex]
            y_pci_values = newPCITable[startIndex:endIndex]
        # Create Plot with X: Time Stamp, Y: Network Value, Color: Green, LineStyle: Solid, Label: Label of Value
        ax[i].plot(x_values, y_network_values, color = 'g', linestyle = 'solid', label = headers[i+1], marker='o')

        
        # Create Plot with X: Time Stamp, Y: PCI, Color: Blue, LineStyle: Solid, Label: Label of PCI
        ax[i].plot(x_values, y_pci_values, color = 'b', linestyle = 'solid', label = headers[4], marker='o')

        if displayValues is True:

            for x,y in zip(x_values, y_network_values):
                if type(y) is float:
                    label = "{:f}".format(y)
                else:
                    label = "{:d}".format(y)

                ax[i].annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,5), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
            for x,y in zip(x_values, y_pci_values):
                if type(y) is float:
                    label = "{:f}".format(y)
                else:
                    label = "{:d}".format(y)

                ax[i].annotate(label, # this is the text
                    (x,y), # these are the coordinates to position the label
                    textcoords="offset points", # how to position the text
                    xytext=(0,5), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center
        # Set Plot to rotate X Axis at a 45 Degree Angle (To See Time Stamps Easier)
        ax[i].tick_params('x', labelrotation=45, labelsize=8)

        # Set Title of Plot as Label of Value
        ax[i].set_title(headers[i+1], fontsize = 12)

        # Intialize a Legend and Grid
        ax[i].legend()
        ax[i].grid()

else:
    print('DEAD')


# Show Figure
plt.show()






