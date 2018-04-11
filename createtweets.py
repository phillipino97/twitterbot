import requests
import random

def setup_webpage():
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = {'name':'input','g':'rbh', 'e':'ang'}
    req = requests.post('http://writerbot.com/lyrics',headers=headers,data=data)
    content = req.content
    content = content[content.find("<p class=\"lyrics\">")+18:]
    content = content[:content.find("  </div>")]
    content = content.replace("<br />", "")
    content = content.replace("</p>", "")
    content = content.replace("\n\n", "\n")
    return content

def get_content_lyric():
    lyrics = setup_webpage().split("\n")
    lyric = random.choice(lyrics)
    while "nigger" in lyric or "nigga" in lyric or "nig" in lyric:
        lyric = random.choice(lyrics)
    return lyric
