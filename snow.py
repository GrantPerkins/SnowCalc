from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class SnowGetter(HTMLParser):

    def gethtml(self, url):
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type').split(";")[0] == 'text/html':
            htmlbytes = response.read()
            htmlstring = htmlbytes.decode("utf-8")
            return htmlstring
        else:
            print("Failure to find data, content =", response.getheader('Content-Type'))
            return ""


def spider(url, word):
    parser = SnowGetter()
    try:
        data = parser.gethtml(url)
        i = data.find(word)
        print(data[i-10:i+20])
    except:
        print("Something went wrong in spider()")


if __name__ == "__main__":
    spider("https://howmuchwillitsnow.com/in/southborough/ma", "inch")