
# coding: utf-8

# In[36]:

import requests
import re
from bs4 import BeautifulSoup


# ### 1 Basic Set

# In[48]:

base_url = "http://api.genius.com"
token = 'Bearer dSpCBWS1LuPJXAy-ypyysbdThrG2ugK60OoWKK0Feq22BjayS5Hmtyd0JMg4iKMQ'
headers = {'Authorization': token}
search_url = base_url + "/search"


# ### 2 Get song data - example with Drake's Hotline Bling

# In[24]:

song_title = "Hotline Bling"
song_artist = "Drake"
data = {'q' : song_title}
response = requests.get(search_url, params=data, headers=headers)
json = response.json()


# In[25]:

# select unique song
song_info = None
for hit in json["response"]["hits"]:
    if hit["result"]["primary_artist"]["name"] == song_artist:
    song_info = hit
    break
if song_info:
    pass


# In[31]:

# store song id
song_id = song_info['result']['id']


# In[49]:

song_url = 'https://genius.com/api/songs/'+str(song_id) 
r = requests.get(song_url)


# In[60]:

r_json = r.json()
r_json['response']['song']['album']['name']


# In[66]:

r_json['response']['song']['producer_artists']


# In[67]:

r_json['response']['song']['writer_artists']


# In[68]:

r_json['response']['song']['release_date']


# ### 3 Get annotations

# from Cristian git

# In[13]:

def annotation_content(annotation_id):
    '''Given the annotation ID, returns a single string with the annotation content'''
    annotation_url = 'https://genius.com/api/annotations/'+str(annotation_id)
    r = requests.get(annotation_url)
    annot = []
    for a in r.json()['response']['annotation']['body']['dom']['children']:
        note = []
        if a != '':
            if (a['tag'] == 'p')|(a['tag'] == 'a'):
                for aa in a['children']:
                    if not isinstance(aa, dict):
                        note.append(aa.strip())
                    else:
                        if 'children' in aa.keys():
                            for aaa in aa['children']:
                                if not isinstance(aaa, dict):
                                    note.append(aaa.strip())
                                else:
                                    if 'children' in aaa.keys():
                                        for aaaa in aaa['children']:
                                            if not isinstance(aaaa, dict):
                                                note.append(aaaa.strip())
                                            else:
                                                if 'children' in aaaa.keys():
                                                    for aaaaa in aaaa['children']:
                                                        if not isinstance(aaaaa, dict):
                                                            note.append(aaaaa.strip())
                                                        else:
                                                            print ('Warning: Depth exceeded for annotation:',annotation_id)
        annot.append(''.join(note).strip())
    annot = '\n'.join(annot).strip()
    annot = re.sub(r'\n+','\n',annot)
    return annot


# In[15]:

def song_annotations(page_url):
    '''Given the song url, returns a list with all the annotation IDs.'''
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    annotation_ids = [link['data-id'] for link in html.find_all(name='a',attrs={'class':"referent",'classification':"accepted"})]
    return annotation_ids


# In[14]:

def song_id2url(song_id):
    '''Given the song ID, returns the song url'''
    song_url = 'https://genius.com/api/songs/'+str(song_id) 
    r = requests.get(song_url)
    page_url = "http://genius.com" + r.json()["response"]["song"]["path"]
    return page_url


# In[140]:

def get_all_annotations_unique(song_id):
    page_url = song_id2url(song_id)
    print (page_url)
    annotations = [(i,annotation_content(i)) for i in song_annotations(page_url)]
    unique_annotations = list(set(annotations))
    return unique_annotations
# for i,a in annotations:
#     print (i)
#     print (a)
#     print ('--------')


# ### 4 Get lyrics

# In[137]:

def get_lyrics_from_song_url(page_url):
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.findAll("div", { "class" : "lyrics" })
#     lyrics = html.find("lyrics")
    lyrics_txt = lyrics[0].get_text()
    lyrics_txt = lyrics_txt.split('\n')
    lyrics_txt = [l for l in lyrics_txt if (l != '') and ('[' not in l)]
    return lyrics_txt


# In[138]:

print (get_lyrics_from_song_url(page_url))


# ### 5 Get all data for a given song ID

# In[141]:

song_title = "Hotline Bling"
song_artist = "Drake"
# song_id = get_id()

data_song = [song_id, song_title, song_artist, get_lyrics_from_song_url(page_url), get_all_annotations_unique(song_id)]


# ## TODO: cure the annotations text

# In[142]:

data_song


# In[ ]:



