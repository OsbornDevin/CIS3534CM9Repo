#!/usr/bin/env python3
#Devin Osborn - GPA 8.py
#Devin Osborn
#Nov 7th, 2023
#Update routers and switches;
#read equipment from a file, write updates & errors to file

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error: The JSON module is not available.")

##---->>>> Create file constants for the file names; file constants can be reused
##         There are 2 files to read this program: equip_r.txt and equip_s.txt
##         There are 2 files to write in this program: updated.txt and errors.txt
      
EQUIP_R_TXT = "equip_r.txt"
EQUIP_S_TXT = "equip_s.txt"
UPDATED_TXT = "updated.txt"
ERRORS_TXT = "errors.txt"


#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object
        
def main():

    ##---->>>> open files here

    #dictionaries
    ##---->>>> read the routers and addresses into the router dictionary
    try:
        with open(EQUIP_R_TXT, 'r') as file_r:
            routers = json.load(file_r)
    except FileNotFoundError:
        print(f"Error: {EQUIP_R_TXT} not found.")
        routers = {}


    ##---->>>> read the switches and addresses into the switches dictionary
    try:
        with open(EQUIP_S_TXT, 'r') as file_s:
            switches = json.load(file_s)
    except FileNotFoundError:
        print(f"Error: {EQUIP_S_TXT} not found.")
        switches = {}


    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            #print("routers", routers)
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file
    try:
        with open(UPDATED_TXT, 'w') as file_updated:
            json.dump(updated, file_updated, indent=2)
    except Exception as e:
        print(f"Error writing to {UPDATED_TXT}: {e}")

    print("Number of invalid addresses attempted:", invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file
    try:
        with open(ERRORS_TXT, 'w') as file_errors:
            for address in invalidIPAddresses:
                file_errors.write(address + '\n')
    except Exception as e:
        print(f"Error writing to {ERRORS_TXT}: {e}")

#top-level scope check
if __name__ == "__main__":
    main()




