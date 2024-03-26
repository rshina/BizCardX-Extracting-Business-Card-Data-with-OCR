#........................Project Title**** BizCardX: Extracting Business Card Data with OCR****.................................
#import Useful libraries
import pandas as pd
import numpy as np
import streamlit as st
import pymysql
import easyocr
import easyocr as ocr  #OCR
import re
from PIL import Image
import io

#Connection to MySQL

myconnection1= pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123')
cur = myconnection1.cursor()
cur.execute("create database if not exists project3sql")
myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin@123',database = "project3sql")
cur = myconnection.cursor()
table_creation=cur.execute("create table if not exists  Table_Bizcard(CARD_HOLDER_NAME varchar(100),DESIGNATION varchar(100),COMPANY_NAME varchar(100),MOBILE_NUMBER varchar(100),EMAIL varchar(100),WEBSITE varchar(100),AREA varchar(100),CITY varchar(100),STATE varchar(100),PIN_CODE int(100),IMAGE LONGBLOB)")

st.set_page_config(page_title=":rainbow[BizCardX: Extracting Business Card Data with OCR]",
                        layout="wide")

     
#Home page configaration
tab1,tab2,tab3,tab4 = st.tabs([":green[ABOUT]",":green[UPLOAD & EXTRACT]",":green[INSERT]",":green[MODIFY]"])
#To set home page
with tab1:
   
    def home_page():
        st.sidebar.subheader("Process:")
        st.sidebar.caption(":red[*Upload image of Bussiness card]")
        st.sidebar.caption(":red[*Extract data fom Bizcard]") 
        st.sidebar.caption(":red[*Extracted data saved into MySQL]")
        st.sidebar.caption(":red[*Streamlit Display]")
        st.sidebar.subheader("Required packages:")
        st.sidebar.caption(":red[Python,VSCODE,Pandas,MYSQL,OCR,STREAMLIT]")
        st.title(":green[BizCardX: Extracting Business Card Data with OCR]")
        st.image("bcard.png",width=400)
        st.text_area("About Project:",
                        "I have created  a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information includes the company name, card holdername, designation, mobile number, email address, website URL, area, city, state,and pin code,Using this  application  users can save the extracted information into a database along with the uploaded business card image.")
        st.text_area("What is OCR",
                        "EasyOCR is a Python computer language Optical Character Recognition (OCR) module that is both flexible and easy to use. OCR technology is useful for a variety of tasks, including data entry automation and image analysis,Here i used to convert image data to texdata") 
        st.text_area("About Streamlit",
                        "Streamlit is a free and open-source framework to rapidly build and share beautiful machine learning and data science web apps.")
    home_page()

#To Uplaod an image , extract data from that and  display in streamlit 
with tab2:
    card_upload = st.file_uploader("upload here",type=["png","jpeg","jpg"])
    st.image(card_upload,width=400)

    if card_upload is not None:
        #To initialise OCR and covert image data to text data using easyocr
        
        reader = ocr.Reader(['en'],model_storage_directory='.')
     
        if isinstance(card_upload, Image.Image):
                image = card_upload
        else:
                image = Image.open(card_upload)
        image_array = np.array(image)


        #To  convert image data to bytes
        result = reader.readtext(image_array)
        Image_bytes= io.BytesIO()
        image.save(Image_bytes,format= "PNG")
        image_data= Image_bytes.getvalue()


    #For Extracting data from uplaoded bizcard
    def get_information(result1,image_data1):
                Information = { "CARD_HOLDER_NAME": [],"DESIGNATION": [],"COMPANY_NAME": [], "MOBILE_NUMBER": [], 
                               "EMAIL": [],"WEBSITE": [], "AREA": [], "CITY": [], "STATE": [], "PIN_CODE": [],"IMAGE": []}
                data_list1=[]
                
                for item1 in result1:
                        data_list1.append(item1[1])
                                


                Information["IMAGE"].append(image_data1)
                Information["CARD_HOLDER_NAME"].append(data_list1[0])
                Information["DESIGNATION"].append(data_list1[1])
                if len(data_list1[-1]) != 4:
                        if re.findall("^[A].",data_list1[-1]):
                                comp=data_list1[7]+" "+data_list1[8]
                                Information["COMPANY_NAME"].append(comp)
                        elif re.findall("^[d].",data_list1[-1])  :
                                comp1=data_list1[7]+" "+data_list1[9]
                                Information["COMPANY_NAME"].append(comp1)
                        elif re.findall("^[R].",data_list1[-1]):
                                comp2=data_list1[6]+" "+data_list1[8]
                                Information["COMPANY_NAME"].append(comp2)
                        else:
                               Information["COMPANY_NAME"].append(data_list1[-1])
                else:
                        company=data_list1[8] +" " + data_list1[10]
                        Information["COMPANY_NAME"].append(company)      
                

                for item2 in range(len(data_list1)):
                        #To get contact information
                        if "+" in data_list1[item2] or  '-' in data_list1[item2]:
                                Information["MOBILE_NUMBER"].append(data_list1[item2])
                        if len(Information["MOBILE_NUMBER"])==2:
                                Information["MOBILE_NUMBER"]=Information["MOBILE_NUMBER"][0]+ " & " + Information["MOBILE_NUMBER"][1]
                        #To get email information

                        elif "@" in data_list1[item2] and ".com" in data_list1[item2]:
                                Information["EMAIL"].append(data_list1[item2].lower())  

                        #To get website information
                        elif "WWW" in data_list1[item2] or "www" in data_list1[item2] or "wWW" in data_list1[item2] or "wWw" in data_list1[item2]  or "wwW" in data_list1[item2]:
                                Information["WEBSITE"].append(data_list1[item2].lower())
                                if Information["WEBSITE"][0]=="www":
                                          Information["WEBSITE"]=Information["WEBSITE"][0] + "." +data_list1[5]

                        #To get area,state information
                        elif re.findall('^[0-9].+[a-zA-Z]+',data_list1[item2]):
                                        
                                        Information["AREA"].append(data_list1[item2].split(',')[0])
                                                
                                        if "; TamilNadu" in  data_list1[item2]:
                                                        Information["STATE"].append(data_list1[item2].split(';')[1])
                                        elif ", TamilNadu;" in  data_list1[item2]:
                                                        
                                                Information["STATE"].append(data_list1[item2].split(',')[-1])
                        #To get city,pincode,state information                                                
                        if re.findall(".+St , ([a-zA-Z]+).+", data_list1[item2]):
                                Information["CITY"].append(data_list1[item2].split(",")[1])
                                
                        elif re.findall(".+St,, ([a-zA-Z]+).+", data_list1[item2]):
                                Information["CITY"].append(data_list1[item2].split(",,")[1])
                        
                        elif re.findall("^[E].*",  data_list1[item2]):
                                Information["CITY"].append(data_list1[item2])
                        
                        #elif pin
                        elif  data_list1[item2].isdigit():
                                Information["PIN_CODE"].append(data_list1[item2])
                        elif  re.findall('[a-zA-Z]{9} +[0-9]',data_list1[item2]):     
                                Information["PIN_CODE"].append(data_list1[item2].split(" ")[1])
                                Information["STATE"].append(data_list1[item2].split(" ")[0])
                        
                return Information
    card_Information=get_information(result,image_data) 


    #TO save extracted data as a dataframe
    dataframe=pd.DataFrame(card_Information)
    st.write(dataframe)


    #Now i have to transfer data stored as dataframe to database,ie to MySQL 
with tab3:
    #To insert data into sql table   
    if  st.button("Click here to insert data into database(SQL)"):
                def Insert(dataframe1):
                                insert='''insert into Table_Bizcard(CARD_HOLDER_NAME,DESIGNATION,COMPANY_NAME,MOBILE_NUMBER
                                ,EMAIL,WEBSITE,AREA,CITY,STATE,PIN_CODE,IMAGE)   values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                                try:
                                        values=dataframe1.values.tolist()
                                        cur.executemany(insert,values)
                                        myconnection.commit()
                                except:
                                        pass
                                return st.success("Data Successfully Inserted into Dtatbase(SQL) "),st.balloons()
                Insert(dataframe)  


#To alter the data which have already saved in MySQL
with tab4:
       select__=st.radio("Select one",("ALTER","DELETE"))
       if select__=="ALTER":
                res=st.selectbox("SELECT(card holder name that already saved in database)", ("SANTHOSH","REVANTH","KARTHICK","Amit kumar","Selva"))

                
                fetch_data1=cur.execute(f"select CARD_HOLDER_NAME,DESIGNATION,COMPANY_NAME,MOBILE_NUMBER ,EMAIL,WEBSITE,AREA,CITY,STATE,PIN_CODE from Table_Bizcard where CARD_HOLDER_NAME='{res}'")
                result1=cur.fetchall()
                
                try:
                        CARD_HOLDER_NAME = st.text_input("CARD_HOLDER_NAME", result1[0][0])
                        DESIGNATION = st.text_input("DESIGNATION", result1[0][1])
                        COMPANY_NAME = st.text_input("COMPANY_NAME", result1[0][2])
                        MOBILE_NUMBER = st.text_input("MOBILE_NUMBER", result1[0][3])
                        EMAIL = st.text_input("EMAIL", result1[0][4])
                        WEBSITE = st.text_input("WEBSITE", result1[0][5])
                        AREA = st.text_input("AREA", result1[0][6])
                        CITY = st.text_input("CITY", result1[0][7])
                        STATE = st.text_input("STATE", result1[0][8])
                        PIN_CODE = st.text_input("PIN_CODE", result1[0][9])
                except:
                    pass
                if st.button("Update changes"):
                        # Update the information of the selected business card which is already saved in the database
                        cur.execute("UPDATE Table_Bizcard SET CARD_HOLDER_NAME=%s,DESIGNATION=%s,COMPANY_NAME=%s,MOBILE_NUMBER=%s,EMAIL=%s,WEBSITE=%s,AREA=%s,CITY=%s,STATE=%s,PIN_CODE=%s WHERE CARD_HOLDER_NAME=%s", (CARD_HOLDER_NAME,DESIGNATION,COMPANY_NAME,MOBILE_NUMBER ,EMAIL,WEBSITE,AREA,CITY,STATE,PIN_CODE,res))
                        myconnection.commit()
                        st.success("Information updated in database successfully.")

       #Finally,to delete bizcard data from database
       if select__=="DELETE":
                cur.execute("SELECT CARD_HOLDER_NAME FROM Table_Bizcard")
                card_holder = cur.fetchall()
                list_={}
                for item3 in card_holder:
                        list_[item3[0]] = item3[0]
                card_select=st.selectbox("SELECT BUSiNESS CARD NAME TO DELETE ",list(list_.keys()))

                if st.button("Click here to delete"):
                        cur.execute(f"DELETE FROM Table_Bizcard WHERE CARD_HOLDER_NAME='{card_select}'")
                        myconnection.commit()
                        st.success("Business Card data deleted from database successfully")

                #To view updated information in the database
                if st.button("Click here to view updated data"):
                        fetch_data3=cur.execute("select * from Table_Bizcard")
                        result2=cur.fetchall()
                        dataframe_update=pd.DataFrame(result2,columns=["CARD_HOLDER_NAME","DESIGNATION","COMPANY_NAME","MOBILE_NUMBER" ,"EMAIL","WEBSITE","AREA","CITY","STATE","PIN_CODE","IMAGE"])
                        st.write(dataframe_update)
 #Here Complete the project BizCardX: Extracting Business Card Data with OCR
                        