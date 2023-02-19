import requests
import pandas as pd
from bs4 import BeautifulSoup


dict_urls = {
    'Astrophysics_of_Galaxies': "astro-ph.GA",
    'Cosmology_and_Nongalactic_Astrophysics': "astro-ph.CO",
    'Earth_and_Planetary_Astrophysics': "astro-ph.EP",
    'High_Energy_Astrophysical_Phenomena': "astro-ph.HE",
    'Instrumentation_and_Methods_for_Astrophysics': "astro-ph.IM",
    'Solar_and_Stellar_Astrophysics': "astro-ph.SR"
}
for k, v in dict_urls.items():
    url = f"https://arxiv.org/list/{v}/new"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    links = list()
    items = soup.find_all('dt')
    for item in items:
        link = item.find_all('a', href=True)[0]['href']
        links.append(f'https://arxiv.org{link}')

    dict_art = {
        'title': [],
        'authors': [],
        'comment': [],
        'subjects': [],
        'abstract': []
    }

    for link in links:
        res = requests.get(link)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Title
        title = soup.findAll('h1', {"class": "title mathjax"})[0].text
        title = title.split('Title:')[1].strip()

        dict_art['title'].append(title)

        # Authors
        authors = soup.findAll('div', {"class": "authors"})[0].find_all('a')
        authors_list = list()
        for author in authors:
            authors_list.append(author.text)

        dict_art['authors'].append(authors_list)

        meta = soup.findAll('tr')

        if len(meta) < 5:
            dict_art['comment'].append(None)

            subjects = soup.findAll('tr')[0].find_all('td')
            if subjects[0].text == "Subjects:":
                dict_art['subjects'].append(subjects[1].text.replace('\n', ''))
            else:
                dict_art['subjects'].append(None)
        else:
            comments = soup.findAll('tr')[0].find_all('td')
            if comments[0].text == "Comments:":
                dict_art['comment'].append(comments[1].text)
            else:
                dict_art['comment'].append(None)

            # Subjects
            subjects = soup.findAll('tr')[1].find_all('td')
            if subjects[0].text == "Subjects:":
                dict_art['subjects'].append(subjects[1].text.replace('\n', ''))
            else:
                dict_art['subjects'].append(None)

        # Subjects
        abstract = soup.findAll(
            'blockquote', {"class": "abstract mathjax"})[0].text
        abstract = abstract.replace('\n', '').split('Abstract:  ')[1].strip()
        dict_art['abstract'].append(abstract)

    df = pd.DataFrame.from_dict(dict_art, orient='index').T
    df['nb_of_aut'] = df.authors.apply(len)
    df.to_csv(f"{k}.csv")
