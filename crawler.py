from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):
    """
    This web spider looks for links on any given page. It really
    likes to start with a menu, becuase it's good at exploring
    through pages of menus. It will return a list of links.
    """

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for key, value in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]

    def getlinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type').split(";")[0] == 'text/html':
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print("Failure to find links, content =",response.getheader('Content-Type'))
            return "", []

def spider(url, next, additional):
    good = []
    snow_days = set()
    to_visit = set()
    to_visit.add(url)
    visited = [url]
    parser = LinkParser()
    while len(to_visit)>0:
        visited.append(url)
        url = to_visit.pop()
        if True:
            if next not in url:
                good.append(url)
            data, links = parser.getlinks(url)
            data = data.lower()
            if next not in url: #is not a link to another list of articles
                if data.find("datetime")>-1: #patch
                    i = data.find("datetime")+10
                    date = [int(n) for n in data[i:i + 10].split('-')]
                else:
                    i = url.find("2")
                    date = [int(n) for n in url[i:i + 10].split('/')]
                date = " ".join(map(str,[date[1], date[2]+1, date[0]]))
                snow_days.add(date)
            for link in links:
                contains_words = link.find(url[0:10])==0 and ((next in link) or
                                 (any([word in link for word in additional]) and "#" not in link))
                if contains_words and link not in visited and link not in to_visit:
                    to_visit.add(link)

        else:
            print("Failed")
            print(url)
    return snow_days

if __name__ == "__main__":
    days = []
    days.extend(list(spider("https://patch.com/massachusetts/northborough/schools", "massachusetts/northborough/schools", ("schools-closed", "-delay-"))))
    days.extend(list(spider("http://www.mysouthborough.com/category/news/schools/","/category/news/schools/", ("snow-day", "dismissal"))))
    print(*sorted(days),sep='\n')
























