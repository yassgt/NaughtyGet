import requests
import pandas as pd
from scidownl import scihub_download
import streamlit as st
from st_aggrid import AgGrid


st.set_page_config(layout="wide")

st.title("Yass Get Jurnal(IEEE)😆")
st.markdown("***")

Key = st.text_input('Pencarian Topik / Author',"WASPAS")

Kword = str(Key)
page_no = 1
headers = {
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://ieeexplore.ieee.org",
    "Content-Type": "application/json",
    }
payload = {
    "newsearch": True,
    "queryText": Kword,
    "highlight": True,
    "returnFacets": ["ALL"],
    "returnType": "SEARCH",
    "pageNumber": page_no
    }

r = requests.post(
        "https://ieeexplore.ieee.org/rest/search",
        json=payload,
        headers=headers
    )
    
page_data = r.json()
listDoi = []
listName = []
listYear = []
listDlink = []
page = range(page_data["totalPages"])
for i in page:
    for record in page_data["records"]:
        listName.append(record["articleTitle"])
        try :
            listDoi.append(record["doi"])
        except KeyError:
            listDoi.append(0)
        listYear.append(record["publicationYear"])
        listDlink.append("https://ieeexplore.ieee.org"+record["documentLink"])

    
r = requests.post(
        "https://ieeexplore.ieee.org/rest/search",
        json=payload,
        headers=headers
    )
df = pd.DataFrame({'Nama Artikel': listDoi, 'Doi': listName, 'Tahun':listYear, 'Link':listDlink})
# def make_clickable(val):
#     return f'<a target="_blank" href="{val}">{val}</a>'

# df.style.format({'Link': make_clickable})


with st.sidebar:
    filter = st.radio(
    "Tahun",
    ('Semua', '5 Tahun Terakhir'))

    if filter == 'Semua':
        df["Tahun"] = df["Tahun"].astype(int)
        
    else:
        df["Tahun"] = df["Tahun"].astype(int)
        df.drop(df.index[df["Tahun"]<2017], inplace=True)
    

   

# HTML(df.to_html(render_links=True, escape=False))

st.dataframe(df)