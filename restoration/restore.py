from bs4 import BeautifulSoup
import os
import subprocess
import time as os_time


def encode(name, content):
  return f" --data-urlencode '{name}={content}'"

def curl(author, title, content, time, link=None):
  command = """curl --location --request POST 'https://utdcs.joshcai.repl.co/submit/' --header 'Content-Type: application/x-www-form-urlencoded' """
  command += encode('title', title)
  command += encode('content', content)
  command += encode('author', author)
  command += encode('time', time)
  if link:
    command += encode('link', link)
    command += encode('linked', 'true')
  result = subprocess.check_output(command, shell=True)
  if 'Go to Replit' in result.decode('utf-8'):
    raise ValueError('curl command failed')


files = os.listdir('backup')
files.sort(key=lambda x: int(x[:-5]))
for file in files:
  print('Restoring file: ', file)
  path = os.path.join('backup', file)
  text = open(path, 'r').read()
  soup = BeautifulSoup(text, 'html.parser')
  title = soup.find(class_='post-title').find('strong')
  if title.string:
    title = title.string.strip()
    link = None
  else:
    link_element = title.find('a')
    link = link_element['href']
    print('  Link: ', link_element['href'])
    title = link_element.string
  content = soup.find(class_='fit-box').string
  author_and_time = soup.find(class_='post-title2')
  author = author_and_time.find('a').string.strip()
  time = author_and_time.getText().split(' on ')[-1].strip()
  print('  Author: ', author)
  print('  Title: ', title)
  print('  Time: ', time)

  curl(author, title, content, time, link=link)
  new_path = os.path.join('backed_up', file)
  os.system(f'mv {path} {new_path}')
  os_time.sleep(1)
  # break
