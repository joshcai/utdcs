from bs4 import BeautifulSoup
import os

files = os.listdir('backup')

for file in files:
  print('Restoring file: ', file)
  path = os.path.join('backup', file)
  text = open(path, 'r').read()
  soup = BeautifulSoup(text, 'html.parser')
  title = soup.find(class_='post-title').find('strong').string
  if title:
    title = title.strip()
  else:
    title = ''
  print(title)