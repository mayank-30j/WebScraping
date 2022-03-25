# importing all the required libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import html5lib
import os

# importing the dataset from Input.xlsx
df = pd.read_excel(r'C:\Users\mayan\OneDrive\Desktop\Internshala\Blackcoffer\Input.xlsx', index_col=False)
# print(df['URL'][0])
# print(df.count())

urls = df['URL']  # list of all the URLs

# Changing the directory to save files in different locations
os.chdir(r'C:\Users\mayan\OneDrive\Desktop\Internshala\Blackcoffer')

# User agent to get access for the website
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
}

counter = 1
delete_item = "- Blackcoffer Insights"
for i in urls:
    r = requests.get(i, headers=header)  # receiving the response data from server
    htmlContent = r.content  # getting the HTML of the website
    soup = BeautifulSoup(htmlContent, features='html5lib')  # Creating object to hold the html

    # Code to extract title of the article from website
    title = soup.title.string
    # print(title)

    # Creating a file and writing data into it, that is extracted from the website

    # Code to extract text from article
    with open('text_{}.txt'.format(counter), 'a+', encoding="utf-8") as f:
        f.write('Title : {}'.format(title))
        # for line in f:
        #     for word in delete_item:
        #         line = line.replace(word, "")
        #     f.write(line)
        f.write('\n')
        f.write('\n')
        for para in soup.find_all('p'):
            Text = para.get_text()
            # print(Text)
            for t in Text:
                f.write(t)

    counter += 1
