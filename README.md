# BizCardX-Extracting-Business-Card-Data-with-OCR

## Overview:

This project aims to build a Streamlit web application that allows users to upload images of business cards, extract relevant information using OCR (Optical Character Recognition), store the extracted data  in a MySQL database.And also Allow the user to Update/delete the data through the streamlit UI

## Technologies Used:

*Python

*Easy OCR

*MySQL

*VSCODE

*Pandas

*Streamlit

## Imported Libraries :

****Libraries for Image Processing :

*import numpy 

*import easyocr

*import re

*from PIL import Image


*import io

****Libraries for Database:

*import pymysql

****Libraries for Dataframe:

*import pandas

****Libraries for Dashboard :

*import streamlit

## Process:

1)Uplaod data:

     Upload a bussiness card and display the image of bussiness card in streamlit using easyocr

2)Extract data:

    Extract relevant information(Company name, Card Holder, Designation, Mobile Number, Email,Website, Area, City, State, and Pincode) from uploaded bussiness card , ad saved as dataframe finally display the dataframe in streamlit

3)Load data:


   In this process save the dataframe of relevant information into database MySQL

4)Display 


    Finally,Extract data from database to update and delete and display of modified data in streamlit


## User Guide:


*If you Click the "Home" button then you will get breaif information about the project  BizCardX-Extracting-Business-Card-Data-with-OCR


*If you Click "Upload and Extract data" you have to upload a bizcard image by clicking "upload here"  Then You will get image of selected bussiness card and relevent information of selected Bizcard.


*Third one is insert,By clicking insert you can insert the extracted data into database MySQL.


*Finally..,Modify if you click modify you will get two options first one is Alter,if you select alter you can alter the data and update the changes,second one is delete ,it allows you to delete the relevent data of selected biscard in MySQL

This is the project BizCardX-Extracting-Business-Card-Data-with-OCR

End














   




















