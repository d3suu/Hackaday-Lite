from flask import Flask
import bs4 as bs
import urllib.request
from flask import request
from flask import redirect
app = Flask(__name__)
blog = "https://hackaday.com/blog/page/"

@app.route('/post', methods=['GET'])
def post():
    hpost = request.args.get('hpost')
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
    # Header
    pageNumber = str(request.args.get('hpage'))
    returnString = "<html><head></head><body><h1>Hackaday Lite</h1><p>Page " + pageNumber + "<ul>"
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

#@app.route('/')
#def root():
#    returnString = "<html><head></head><body><p>made by d3suu, work in progress</p><h1>First 10 pages of Hackaday:</h1><ul>"
#    for n in range(1, 10):
#        source = urllib.request.urlopen(blog + str(n)).read()
#        soup = bs.BeautifulSoup(source, 'lxml')
#        #titles = soup.find_all("h1", {"class": "entry-title"})
#        articles = soup.find_all("article")
#        for x in articles:
#            returnString += "<li><a href=\"/post?hpost=" + x.find("a").get("href") + "\">" + x.find("h1").string + "</a></li>"
#    returnString += "</ul></body></html>"
#    return returnString

