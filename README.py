# Module-11
#covid

import pandas as pd
import plotly.express

#load data
data = pd.read_excel("C:/Users/michelle/Desktop/temp/COVID19_data.xlsx")

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = data
all_dims = ["OBJECTID_12_13","OBJECTID","DEPCODE","COUNTY","COUNTYNAME","DATESTAMP","ShapeSTAre","ShapeSTLen","OBJECTID_1","County_1","State","OBJECTID_12","DEPCODE_1","COUNTYN","PUIsTotal","Age_0_9","Age_10_19","Age_20_29","Age_30_39","Age_40_49","Age_50_59","Age_60_69","Age_70_79","Age_80plus","Age_Unkn","C_Age_0_9","C_Age_10_19","C_Age_20_29","C_Age_30_39","C_Age_40_49","C_Age_50_59","C_Age_60_69","C_Age_70_79","C_Age_80plus","C_Age_Unkn","PUIAgeRange","PUIAgeAvrg","C_AgeRange","C_AgeAvrg","C_AllResTypes","C_NonResDeaths","PUIFemale","PUIMale","PUISexUnkn","PUIFLRes","PUINotFLRes","PUIFLResOut","PUITravelNo","PUITravelUnkn","PUITravelYes","C_ED_NO","C_ED_NoData","C_ED_Yes","C_Hosp_No","C_Hosp_Nodata","C_Hosp_Yes","FLResDeaths","PUILab_Yes","TPositive","TNegative","TInconc","TPending","PUIContNo","PUIContUnkn","PUIContYes","CasesAll","C_Men","C_Women","C_TravelYes","C_TravelNo","C_TravelUnkn","C_FLRes","C_NotFLRes","C_FLResOut","T_NegRes","T_NegNotFLRes","T_PendRes","T_PendNotRes","T_total","T_negative","T_pending","T_positive","FLandNonFLDeaths","EverMon","MonNow","Shape__Area","Shape__Length","Shape_Length","Shape_Area"]

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x}
                 for x in all_dims],
        value=all_dims[:2],
        multi=True
    ),
    dcc.Graph(id="splom"), #do not touch
])

@app.callback(
    Output("splom", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(dims):
    fig = px.scatter_matrix(
        df, dimensions=dims, color="Age_80plus")
    return fig

app.run_server()


#web scrape
import requests
import pandas as pd
import os
import fitz #best pdf reader in the land. pip install pymupdf
os.chdir("C:/Users/Michele/Desktop/temp")

url = "https://www.berkshirehathaway.com/letters/letters.html"

response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})

response.content

#1998+ has html
from bs4 import BeautifulSoup as b

Soup = b(response.content, features="lxml")

table = Soup.find(class_="MsoNormalTable")
elements = table.find_all("a")


#
url = "https://www.berkshirehathaway.com/letters/"
mergedText = ""
for element in elements:
    SecondUrl = element.attrs['href']
    Url = url  + SecondUrl
    year = SecondUrl[:4]
    if ".html" in SecondUrl:
        #Get pdf files
        if int(year) >= 1998:
            grabbedElements = requests.get(Url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                        'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})
            Soup = b(grabbedElements.content, features="lxml")
            aTypeElements = Soup.find_all("a")
            
            Flag = False
            urlXXX = ""
            for aElement in aTypeElements:
                if "html" in aElement.text.lower():
                    Flag = True
                    urlXXX = aElement.attrs['href']
                    break
            if Flag: #Not pdfs
                #url+urlXXX = (Url.replace(".","").replace("html","htm") + ".html").replace("www","www.").replace("com",".com")
                ConstructedUrl = url + urlXXX
                if "/" in urlXXX:
                    ConstructedUrl = "https://www.berkshirehathaway.com" + urlXXX
                    
                Response2 = requests.get(ConstructedUrl, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                            'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})
                #Check for 404 not found
                if Response2.status_code == 404:
                    print("404",url+urlXXX)
                    continue
                    
                Soup = b(Response2.content, features="lxml")
                filteredStuff = Soup.find("body") 
                cleanedUpStuff = filteredStuff.text
                f = open(f"ShareHolderLetters{year}.txt", "w")
                f.write(cleanedUpStuff)
                f.close()
                #Create merged file
                mergedText += ("-"*10) + year + ("-"*10)
                mergedText += cleanedUpStuff
            else: #Parse PDFS Type 1
                BuiltUrl = url+aTypeElements[-1].attrs['href']
                Response2 = requests.get(BuiltUrl, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                            'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})
                text = ""

                #Read pdf
                with fitz.open(stream=Response2.content, filetype="pdf") as doc:
                    for page in doc:
                        text += page.getText()
                f = open(f"ShareHolderLetters{year}.txt", "w")
                text = text.encode('ascii', 'ignore').decode('ascii')
                f.write(text)
                f.close()
                #Merge to merged file
                mergedText += "\n" + ("-"*10) + year + ("-"*10)
                mergedText += text
        else:
            #Iterate through links
            response = requests.get(Url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                            'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})
        
            Soup = b(response.content, features="lxml")
           
            if year == "1997":
                bodyObject = Soup.find("body") #get bodied
                cleanedUpStuff = bodyObject.text
            else:   
                filteredStuff = Soup.find_all("pre") 
                cleanedUpStuff = filteredStuff[0].text
            
            f = open(f"ShareHolderLetters{year}.txt", "w")
            f.write(cleanedUpStuff)
            f.close()
            #Create merged file
            mergedText += "\n" + ("-"*10) + year + ("-"*10)
            mergedText += cleanedUpStuff
    else:#This is where it goes straight to pdfs (#Parse PDFS Type 2)
        Response2 = requests.get(Url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9', 'x-api-key': 'O8EgITyUaoI9ac10lUAuOl8Z3ySn1JQ3r1J'})

        with fitz.open(stream=Response2.content, filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.getText()            
        f = open(f"ShareHolderLetters{year}.txt", "w")
        text = text.encode('ascii', 'ignore').decode('ascii')
        f.write(text)
        f.close()
        #Merge to merged file
        mergedText += "\n" + ("-"*10) + year + ("-"*10)
        mergedText += text
f = open("ShareHolderLetters.txt", "w")
f.write(mergedText)
f.close()
