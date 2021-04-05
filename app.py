from flask import Flask
import bs4 as bs
import urllib.request
from flask import request
from flask import redirect
import re
app = Flask(__name__)
blog = "https://hackaday.com/blog/page/"

def matchPost(link):
    match = re.match(r'^https://hackaday\.com/20\d{2}/\d{2}/\d{2}/[\S\-\d]+/$', link)
    return match

@app.route('/post', methods=['GET'])
def post():
    hpost = request.args.get('hpost')
    # Check for regex match
    if not matchPost(hpost):
        return "Link match error"

    source = urllib.request.urlopen(hpost)
    soup = bs.BeautifulSoup(source, 'lxml')
    
    # Title
    returnString = "<html><head>" + str(soup.title) + "</head><body><h1><a href=\"/\">Hackaday Lite</a></h1><h2>"
    # Header
    returnString += str(soup.title.string).replace(" | Hackaday","") + "</h2>"
    # Article image
    returnString += str(soup.find("img", {"itemprop": "image"})).replace("?w=", "?w=300&")
    # Article html
    returnString += str(soup.find("div", {"class": "entry-content"})).replace("?w=", "?w=300&").replace("srcset", "bhd").replace("https://hackaday.com/20", "/post?hpost=https://hackaday.com/20")
    returnString += "</body></html>"
    return returnString

@app.route('/page', methods=['GET'])
def page():
    pageNumber = str(request.args.get('hpage'))
    # Match number
    if not re.match(r'^\d+$', pageNumber):
        return "Page number match error"
    
    # Header
    returnString = "<html><head><title>Hackaday Lite - " + pageNumber + "</title></head><body><h1>Hackaday Lite</h1><p>Page " + pageNumber + "<ul>"
    source = urllib.request.urlopen(blog + pageNumber).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    articles = soup.find_all("article")
    for x in articles:
        returnString += "<li><a href=\"/post?hpost=" + x.find("a").get("href") + "\">" + x.find("h1").string + "</a></li>"
    returnString += "</ul>"
    # Previous page button
    if pageNumber != "1":
        returnString += "<a href=\"/page?hpage=" + str(int(pageNumber)-1) + "\">Prev page</a> "
    # Next page button
    returnString += "<a href=\"/page?hpage=" + str(int(pageNumber)+1) + "\">Next page</a></body></html>"
    return returnString

@app.route('/')
def root():
    return redirect("/page?hpage=1", code=302)

