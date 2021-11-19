from requests_html import HTMLSession

session = HTMLSession()
url = "https://www.youtube.com/results?search_query=programming&sp=CAISBAgBEAE%253D"
response = session.get(url)
response.html.render(sleep=1, keep_page = True, scrolldown = 2)

for links in response.html.find('a#video-title'):
    link = next(iter(links.absolute_links))
    break

print(link)
