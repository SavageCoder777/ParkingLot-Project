import datetime
import matplotlib.pyplot as plt
import streamlit as st
import json
import random
import pandas as pd
import os

# python -m streamlit run ToDo.py

ParkingLotlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
InformationTank = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0}
MoneyDue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
AccountInfo = []
Revenue = 0
stfile = "d:\\Prahlad.V.C\\Documents\\Python\\Python Coding\\Other\\ParkingLot\\Streamlit.json"

st.write("# Smallest Parking Lot")
st.write("## There are ten [10] spots in total.")

def opening_statements_READ():
    infofileread = open("d:\\Prahlad.V.C\\Documents\\Python\\Python Coding\\Other\\ParkingLot\\Streamlit.json", "r")
    for action in infofileread:
        infofileaction = json.loads(action)
        try:
            try:
                if infofileaction["Reserve"] == "Reserve":
                    InformationTank[int(infofileaction["Spot"])] = infofileaction["Information"]
                    ParkingLotlist[int(infofileaction["Spot"]) - 1] = 1
                    global Revenue
                    Revenue+=10
            except:
                continue
            try:
                if infofileaction["Leave"] == "Leave":
                    InformationTank[int(infofileaction["Spot"])] = 0
                    ParkingLotlist[int(infofileaction["Spot"]) - 1] = 0
                    try:
                        AccountInfo.append(infofileaction["Information"])
                    except:
                        continue
            except:
                continue
        except:
            st.write("You are our first customer. Welcome to the Grand Opening of THE SMALLEST PARKING LOT.")
    st.write("### Our current revenue is $" + str(Revenue) + " ... make it better.")
    infofileread.close()

def check_spot_reservation_and_free():
    whichsinfo = st.text_input("Which spots revervations/frees do you want to see? - ")  
    Reserve = 0
    Freed = 0
    infofileread2 = open("d:\\Prahlad.V.C\\Documents\\Python\\Python Coding\\Other\\ParkingLot\\Streamlit.json", "r")
    for action2 in infofileread2:
        infofileaction2 = json.loads(action2)
        if infofileaction2["Spot"] == whichsinfo:
            try:
                if infofileaction2["Reserve"] == "Reserve":
                    Reserve+=1
            except:
                continue
            try:
                if infofileaction2["Leave"] == "Leave":
                    Leave+=1
            except:
                continue
    st.write("          Spot num. " + whichsinfo + " has been RESERVED " + str(Reserve) + " time/s and has been FREED " + str(Freed) + " time/s.")
    infofileread2.close()

# def make_pie_chart(rof, rof2):
#     Leave = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     Leave2_0 = []
#     colorchoices = ["darkgray", "gray", "lightgray", "lightblue", "lightgreen", "skyblue", "aqua", "red", "lightpink", "yellowgreen", "b", "g", "r", "c", "m", "y", "k", "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
#     colors = []
#     spots = []
#     infofileread3 = open("d:\\Prahlad.V.C\\Documents\\Python\\Python Coding\\Other\\ParkingLot\\InformationFileJson.txt", "r")
#     for action3 in infofileread3:
#         infofileaction3 = json.loads(action3)
#         if infofileaction3[rof] == rof2:
#                 whichcolor = random.randint(0, 21)
#                 Leave[int(infofileaction3["Spot"]) - 1]+=1
#                 isrepeat = 0
#                 for spot in range(len(spots)):
#                     if spots[spot] != ("Spot " + str(infofileaction3["Spot"])):
#                         isrepeat+=1
#                 if isrepeat == len(spots):
#                     spots.append("Spot " + str(infofileaction3["Spot"]))
#                     colors.append(colorchoices[whichcolor])
#         else:
#             print("There is no data.")
#             return
#     for unnecessary in range(len(Leave)):
#         if Leave[unnecessary] != 0:
#             Leave2_0.append(Leave[unnecessary])
#     plt.pie(Leave2_0, labels = spots, colors = colors, startangle = 90, shadow = True, radius = 1.2, autopct = '%1.1f%%') 
#     plt.legend()
#     plt.show()
#     infofileread3.close()

# def make_graphs():
#     questioninputgraph = input("               Do you want a graph which shows the (1) Reserved /or/ (2) Freed /spots? - ")
#     if questioninputgraph == "1":
#         make_pie_chart("Reserve", "Reserve")
#     elif questioninputgraph == "2":
#         make_pie_chart("Leave", "Leave")

def make_spot_graph():
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
        "Reserve": "Reserve",
        "Spot": whichspot,
        "Information": {        
            "Name": name,
            "License Plate": licenseplate,
            "Car Type": car,
            "Car Color": color
            },
        "Money": 10
    }
    with open(stfile, "a") as appendstfile:
        json.dump(reservationinfo, appendstfile)
        appendstfile.write("\n")

def load_data():
    if os.path.exists(stfile):
        return pd.read_json(stfile, lines=True)
    else:
        with open(stfile):
            pass

def reserve_spot_INSERT():
    whichspot = st.text_input("Which spot do you want?")
    place = (int(whichspot) - 1)
    print("Which Spot: ", place)
    if ParkingLotlist[place] == 0:
        name = st.text_input("Name")
        licenseplate = st.text_input("License Plate")
        car = st.text_input("Car Type")
        color = st.text_input("Car Color")
        if st.button("Add Reservation", key = "Add Reservation"):
            add_reservation(name, licenseplate, car, color, int(whichspot))

        ld = load_data()
        st.write(ld)
        InformationTank[int(whichspot)] = (name, licenseplate, car, color)
    else:
        st.write("I'm sorry, but that spot is full. Please try again.")

def check_spot_info_READ():
    questioninputinfo = st.text_input("Which spot do you want to check in on?")
    checkinfo = int(questioninputinfo)
    if ParkingLotlist[(checkinfo - 1)] == 0:
        st.write("                    I'm sorry, but I'm afraid that there are no car/s in that spot.")
    else:
        st.write("                    Name: " + InformationTank[checkinfo]["Name"])
        st.write("                    License Plate: " + InformationTank[checkinfo]["License Plate"])
        st.write("                    Car Type: " + InformationTank[checkinfo]["Car Type"])
        st.write("                    Color: " + InformationTank[checkinfo]["Color"])
        st.write("                    Money Due: $10 [Ten Dollars]")

def remove_reservation(cardtype, cardname, cardcvv, cardexpiry, whichspot2):
    time = datetime.datetime.now()
    timestring = time.strftime("%m/%d/%Y %H:%M:%S")
    leaveinfo = {
        "Time": timestring,
        "Spot": whichspot2,
        "Information": {
            "Card Type": cardtype,
            "Card Name": cardname,
            "Card CVV": cardcvv,
            "Card Expiry": cardexpiry
        },
        "Money": 0
    }
    with open(stfile, "a") as appendstfile:
        json.dump(leaveinfo, appendstfile)
        appendstfile.write("\n")

def delete_spot_info_DELETE():
    carretrieval = st.text_input("What spot is your car in?")
    retrieval = int(carretrieval) - 1
    if ParkingLotlist[retrieval] == 0:
        st.write("I'm sorry, but I'm afraid that there are no car/s in that spot.")
    else:
        coc = st.selectbox("Will You Pay with Cash or Card?", ["Cash", "Card"], key = "coc")
        if "Cash" in coc:
            st.write("Thank you for parking at The Smallest Parking Lot!")
        elif "Card" in coc:
            cardtype = st.text_input("Card Type")
            cardname = st.text_input("Card Name")
            cardcvv = st.text_input("CVV")
            cardexpiry = st.text_input("Card Expiry")
            if st.button("Retrieve Car", key = "Retrieve Car"):
                remove_reservation(cardtype, cardname, cardcvv, cardexpiry, int(carretrieval))
        ld2 = load_data()
        st.write(ld2)
        InformationTank[int(carretrieval)] = 0
        st.write("Thank you for using The Smallest Parking Lot! Hope to see you soon!")

opening_statements_READ()
questionnaire = True
uoa = st.selectbox("Are you a user or a customer?", ["", "User", "Admin"], key = "uoa")
if "User" in uoa:
    whatuseroption = st.selectbox("What do you want to do?", ["", "Reserve a Spot", "Retrieve a Car", "Show Spots"], key = "whatuseroption")
    if "Reserve a Spot" in whatuseroption:
        reserve_spot_INSERT()

    elif "Retrieve Car" in whatuseroption:
        delete_spot_info_DELETE()

    elif "Show Spots" in whatuseroption:
        make_spot_graph()

if "Admin" in uoa:
    whatadminoption = st.selectbox("What do you want to do?", ["", "Check Spot Information", "Check Full Spots", "Check Empty Spots", "Check Num. of Times a Spot has been Reserved and Freed", "See Chart Detailing Spot Preferences"], key = "whatadminoption")
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

    elif "Check # of Times a Spot has been Reserved & Freed" in whatadminoption:
        check_spot_reservation_and_free()

    elif "See Chart Detailing Spot Preferences" in whatadminoption:
        # make_graph()
        st.write("Function Not Available Now.")