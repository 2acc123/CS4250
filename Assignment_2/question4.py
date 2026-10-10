import re
from bs4 import BeautifulSoup
 
# HTML needed
html = """
<html>
<head>
<title>My first web page</title>
</head>
<body>
<h1>My first web page</h1>
<h2>What this is tutorial</h2>
<p>A simple page put together using HTML. <em>I said a simple page.</em>.</p>
<ul>
 <li>To learn HTML</li>
 <li>
 To show off
 <ol>
 <li>To my boss</li>
 <li>To my friends</li>
 <li>To my cat</li>
 <li>To the little talking duck in my brain</li>
 </ol>
 </li>
 <li>Because I have fallen in love with my computer.</li>
</ul>
<h3>Where to find the tutorial</h3>
<p><a href="http://www.aaa.com"><img src=http://www.aaa.com/badge1.gif></a></p>
<h4>Some random table</h4>
<table>
 <tr class="tutorial1">
 <td>Row 1, cell 1</td>
 <td>Row 1, cell 2<img src=http://www.bbb.com/badge2.gif></td>
 <td>Row 1, cell 3</td>
 </tr>
 <tr class="tutorial2">
 <td>Row 2, cell 1</td>
 <td>Row 2, cell 2</td>
 <td>Row 2, cell 3<img src=http://www.ccc.com/badge3.gif></td>
 </tr>
</table>
</body>
</html>
"""
 
soup = BeautifulSoup(html, "html.parser")
 
# a
print("a.")
print(soup.title.text)
 
# b
print("\nb.")
print(soup.find("ol").find_all("li")[1].text)
 
# c
rows = soup.find("table").find_all("tr")
print("\nc.")
for td in rows[0].find_all("td"):
    print(td)
 
# d
print("\nd.")
print(soup.find("h2", string=re.compile("tutorial")).text)
 
# e
print("\ne.")
for text in soup.find_all(string=re.compile("HTML")):
    print(text)
 
# f
print("\nf.")
for td in rows[1].find_all("td"):
    print(td)
 
# g
print("\ng.")
for img in soup.find("table").find_all("img"):
    print(img)
