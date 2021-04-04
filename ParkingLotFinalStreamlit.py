import datetime
import matplotlib.pyplot as plt
import streamlit as st
import json
import random
import pandas as pd
import os
import time
import requests

# python -m streamlit run ToDo.py

ParkingLotlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
InformationTank = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
MoneyDue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
AccountInfo = []
Revenue = 0

st.write("# Smallest Parking Lot")
st.write("## There are ten [10] spots in total.")

apiurl = "abdd9cce-f791-4875-be4e-dd35a0ec12f9"
headers = {"Api-Key": apiurl, "Content-Type": "application/json"}
storename = "streamlitcloud-json"
storeurl = f"https://json.psty.io/api_v1/stores/{storename}"

def load_data():
    res = requests.get(storeurl, headers=headers)
    listdata = res.json()["data"]
    return listdata
store = pd.DataFrame(load_data())

def opening_statements_READ():
    infofileread = load_data()
    for infofileaction in infofileread:
        try:
            if infofileaction["Reserve or Free"] == "Reserve":
                InformationTank[int(infofileaction["Spot"])] = infofileaction["Information"]
                ParkingLotlist[int(infofileaction["Spot"]) - 1] = 1
            if infofileaction["Reserve or Free"] == "Free":
                InformationTank[int(infofileaction["Spot"])] = 0
                ParkingLotlist[int(infofileaction["Spot"]) - 1] = 0
                global Revenue
                Revenue+=10
                try:
                    AccountInfo.append(infofileaction["Information"])
                except:
                    continue
        except:
            st.write("You are our first customer. Welcome to the Grand Opening of THE SMALLEST PARKING LOT.")

def check_spot_reservation_and_free():
    whichsinfo = st.text_input("Which spots revervations/frees do you want to see? - ")  
    if int(whichsinfo) <= 10 and int(whichsinfo) >= 1:
        Reserve = 0
        Freed = 0
        infofileread2 = load_data()
        for infofileaction2 in infofileread2:
            if infofileaction2["Spot"] == int(whichsinfo):
                if infofileaction2["Reserve or Free"] == "Reserve":
                    Reserve+=1
                if infofileaction2["Reserve or Free"] == "Free":
                    Freed+=1
        st.write("Spot num. " + whichsinfo + " has been RESERVED " + str(Reserve) + " time/s and has been FREED " + str(Freed) + " time/s.")
    else:
        st.write("Please Choose a Spot Between 1 [One] and 10 [Ten]")

def make_pie_chart(rof):
    Leave = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Leave2_0 = []
    colorchoices = ["darkgray", "gray", "lightgray", "lightblue", "lightgreen", "skyblue", "aqua", "red", "lightpink", "yellowgreen", "b", "g", "r", "c", "m", "y", "k", "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
    colors = []
    spots = []
    infofileread3 = load_data()
    try:
        for infofileaction3 in infofileread3:
            if infofileaction3["Reserve or Free"] == rof:
                whichcolor = random.randint(0, 21)
                Leave[int(infofileaction3["Spot"]) - 1]+=1
                isrepeat = 0
                for spot in range(len(spots)):
                    if spots[spot] != ("Spot " + str(infofileaction3["Spot"])):
                        isrepeat+=1
                if isrepeat == len(spots):
                    spots.append("Spot " + str(infofileaction3["Spot"]))
                    colors.append(colorchoices[whichcolor])
    except:
        st.write("There is no data.")
        return
    for unnecessary in range(len(Leave)):
        if Leave[unnecessary] != 0:
            Leave2_0.append(Leave[unnecessary]) 
    fig, ax = plt.subplots()
    ax.pie(Leave2_0, labels = spots)
    st.pyplot(fig)

def make_graphs():
    questioninputgraph = st.selectbox("Do You want to See a Chart which Shows the Reserved or Freed Spots?", ["", "Reserved", "Freed"], key = "Which Pie")
    if "Reserved" in questioninputgraph:
        make_pie_chart("Reserve")
    elif "Freed" in questioninputgraph:
        make_pie_chart("Free")

def make_spot_graph():
    st.write("Legend ~" + "\n" + "Yellow - Reserved" + "\n" + "Purple - Free" + "\n" + "\n" + "(Side Note: Please disregard the 0th spot. It does not count)")
    ParkingLotlistduplicate = ParkingLotlist
    ParkingLotlistduplicate.append(0)
    for _ in range(len(ParkingLotlistduplicate) - 1):
        for movedown in range(len(ParkingLotlistduplicate) - 1):
            a = ParkingLotlistduplicate[movedown]
            b = ParkingLotlistduplicate[movedown + 1]
            c = a
            a = b
            b = c
            ParkingLotlistduplicate[movedown] = a
            ParkingLotlistduplicate[movedown + 1] = b
    spotchart = [ParkingLotlistduplicate]
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(spotchart)
    ax[0].set_title("Spots")
    st.pyplot(fig)

def add_reservation(name, licenseplate, car, color, whichspot):
    time = datetime.datetime.now()
    timestring = time.strftime("%m/%d/%Y %H:%M:%S")
    reservationinfo = {
        "Time": timestring,
        "Reserve or Free": "Reserve",
        "Spot": whichspot,
        "Information": {        
            "Name": name,
            "License Plate": licenseplate,
            "Car Type": car,
            "Car Color": color
            },
        "Money": 10,
        "Enter": "\n"
    }
    data = load_data()
    data.append(reservationinfo)
    res = requests.put(storeurl, headers=headers, data=json.dumps(data))

def reserve_spot_INSERT(uoa, whatuseroption):
    whichspot = st.text_input("Which spot do you want?")
    place = (int(whichspot) - 1)
    if int(whichspot) <= 10 and int(whichspot) >= 1:
        if ParkingLotlist[place] == 0:
            name = st.text_input("Name")
            licenseplate = st.text_input("License Plate")
            car = st.text_input("Car Type")
            color = st.text_input("Car Color")
            if st.button("Add Reservation", key = "Add Reservation"):
                add_reservation(name, licenseplate, car, color, int(whichspot))
                name = ""
                licenseplate = ""
                car = ""
                color = ""
                whichspot = ""
                whatuseroption = ""
                uoa = ""
                st.write("Reservation Successfully Added!")
            ParkingLotlist[int(whichspot)] = 1
            InformationTank[int(whichspot)] = (name, licenseplate, car, color)
        else:
            st.write("I'm sorry, but that spot is full. Please try again.")
    else:
        st.write("Please Choose a Spot Between 1 [One] and 10 [Ten]")

def check_spot_info_READ():
    questioninputinfo = st.text_input("Which spot do you want to check in on?")
    if int(questioninputinfo) <= 10 and int(questioninputinfo) >= 1:
        checkinfo = int(questioninputinfo)
        if ParkingLotlist[(checkinfo - 1)] == 0:
            st.write("I'm sorry, but I'm afraid that there are no car/s in that spot.")
        else:
            st.write("Name: " + InformationTank[checkinfo]["Name"])
            st.write("License Plate: " + InformationTank[checkinfo]["License Plate"])
            st.write("Car Type: " + InformationTank[checkinfo]["Car Type"])
            st.write("Color: " + InformationTank[checkinfo]["Car Color"])
            st.write("Money Due: $10 [Ten Dollars]")
    else:
        st.write("Please Choose a Spot Between 1 [One] and 10 [Ten]")

def remove_reservation(cardtype, cardname, cardcvv, cardexpiry, whichspot2):
    time = datetime.datetime.now()
    timestring = time.strftime("%m/%d/%Y %H:%M:%S")
    leaveinfo = {
        "Time": timestring,
        "Spot": whichspot2,
        "Reserve or Free": "Free",
        "Information": {
            "Card Type": cardtype,
            "Card Name": cardname,
            "Card CVV": cardcvv,
            "Card Expiry": cardexpiry
        },
        "Money": 0,
        "Enter": "\n"
    }
    data = load_data()
    data.append(leaveinfo)
    res = requests.put(storeurl, headers=headers, data=json.dumps(data))

def delete_spot_info_DELETE(uoa, whatuseroption):
    carretrieval = st.text_input("What spot is your car in?")
    if int(carretrieval) <= 10 and int(carretrieval) >= 1:
        retrieval = int(carretrieval) - 1
        if ParkingLotlist[retrieval] == 0:
            st.write("I'm sorry, but I'm afraid that there are no car/s in that spot.")
        else:
            coc = st.selectbox("Will You Pay with Cash or Card?", ["", "Cash", "Card"], key = "coc")
            if "Cash" in coc:
                if st.button("Retrieve Car", key = "Retrieve Car via Cash"):
                    remove_reservation("N/A", "N/A", "N/A", "N/A", int(carretrieval))
                    st.write("Thank you for parking at The Smallest Parking Lot!  Hope to see you soon!")
                    time.sleep(0.5)
                    whatuseroption = ""
                    uoa = ""
            elif "Card" in coc:
                cardtype = st.text_input("Card Type")
                cardname = st.text_input("Card Name")
                cardcvv = st.text_input("CVV")
                cardexpiry = st.text_input("Card Expiry")
                if st.button("Retrieve Car", key = "Retrieve Car via Card"):
                    remove_reservation(cardtype, cardname, cardcvv, cardexpiry, int(carretrieval))
                    st.write("Thank you for parking at The Smallest Parking Lot!  Hope to see you soon!")
                    time.sleep(0.5)
                    cardtype = ""
                    cardname = ""
                    cardcvv = ""
                    cardexpiry = ""
                    whatuseroption = ""
                    uoa = ""
            ParkingLotlist[int(carretrieval)] = 0
            InformationTank[int(carretrieval)] = 0
    else:
        st.write("Please Choose a Spot Between 1 [One] and 10 [Ten]")

opening_statements_READ()
uoa = st.selectbox("Are you a user or an admin?", ["", "User", "Admin"], key = "uoa")
if "User" in uoa:
    st.write("### Our fee is only $10 [Ten Dollars]! You're free to come! Choose spots from 1 [One] to 10 [Ten].")
    whatuseroption = st.selectbox("What do you want to do?", ["", "Reserve a Spot", "Retrieve a Car", "Show Spots"], key = "whatuseroption")
    if "Reserve a Spot" in whatuseroption:
        reserve_spot_INSERT(uoa, whatuseroption)

    elif "Retrieve a Car" in whatuseroption:
        delete_spot_info_DELETE(uoa, whatuseroption)

    elif "Show Spots" in whatuseroption:
        make_spot_graph()

if "Admin" in uoa:
    username = st.text_input("## Enter Username", type = "default")
    password = st.text_input("## Enter Password", type = "password")
    if username == "admin" and password == "pass":
        st.write("### Our current revenue is $" + str(Revenue) + " ... make it better.")
        whatadminoption = st.selectbox("What do you want to do?", ["", "Check Spot Information", "Check Full Spots", "Check Empty Spots", "Check Num. of Times a Spot has been Reserved and Freed", "See Chart Detailing Spot Preferences", "See Complete Spot Information"], key = "whatadminoption")
        if "Check Spot Information" in whatadminoption:
            check_spot_info_READ()

        elif "Check Full Spots" in whatadminoption:
            fullLots = 0
            fullLotslist = []
            for check in range(len(ParkingLotlist)):
                if ParkingLotlist[check] == 1:
                    fullLots += 1
                    fullLotslist.append((check + 1))
            st.write("          There are " + str(fullLots) + " full lots. They are the spots that follow: " + str(fullLotslist))

        elif "Check Empty Spots" in whatadminoption:
            emptyLots = 0
            emptyLotslist = []
            for check in range(len(ParkingLotlist)):
                if ParkingLotlist[check] == 0:
                    emptyLots += 1
                    emptyLotslist.append((check + 1))
            st.write("          There are " + str(emptyLots) + " empty lots. They are the spots that follow: " + str(emptyLotslist))

        elif "Check Num. of Times a Spot has been Reserved and Freed" in whatadminoption:
            check_spot_reservation_and_free()

        elif "See Chart Detailing Spot Preferences" in whatadminoption:
            make_graphs()
            # st.write("Function Not Available Now.")
        
        elif "See Complete Spot Information" in whatadminoption:
            st.write(store)
    else:
        st.write("Wrong Username and/or Password.")