import requests
from bs4 import BeautifulSoup
import pandas as pd

###rest_info

x = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
}

url = "https://www.openrice.com/en/hongkong/restaurants?landmarkId=1010"

response = requests.get(
    url,
    headers=x
)

soup = BeautifulSoup(response.text, "html.parser")

ul = soup.select_one("ul.sr1-listing-content-cells")

lis = ul.select("li.sr1-listing-content-cell")


temp = []

for li in lis:

    re_id = li.select('section')[1]['data-poi-id']
    title_name = li.select_one('.title-name').text.strip()
    address = li.select_one('div.icon-info.address span').text.strip()
    like_nums = li.select_one('div.emoticon-container.smile-face span').text.strip()
    bookmark = li.select_one('.text.bookmarkedUserCount.js-bookmark-count')['data-count']
    restaurant = [re_id, title_name,address,like_nums, bookmark]

    temp.append(restaurant)
print(temp)
df = pd.DataFrame(temp,columns=['id','name','address','like_nums','bookmark'])

df.to_csv('rest_info.csv')


url = lis[0].select('.title-name')[0].a['href']
print(url)

relative_path = 'https://www.openrice.com' +  lis[0].select_one('.title-name').a['href'] + '/reviews'


re1_response = requests.get(relative_path,headers=x)

re1_soup = BeautifulSoup(re1_response.text, "html.parser")
re1_main = re1_soup.select_one("div.js-sr2-review-main.sr2-review-main")
re1_title1 = re1_main.select("div.review-title")
re1_title2 = re1_title1[0].text.strip()

re1_comment1 = re1_main.select("div.sr2-review-list-container section.review-container")
re1_comment2 = re1_comment1[1]
for i in re1_comment2.select('a'):
    i.decompose()
print(re1_comment2)
list(range(len(re1_comment2.select('a'))))
re1_comment2.select('a')

target = ['like','comment','views']
text = [i.strip() for i in re1_comment2.split('\n')]
print(text)

def text_check(row,target):
    for i in target:
        if i in row:
            return True
    return False
print(text_check(re1_comment2.split('\n')[2],target))

def clean_text(text, list1):
    cleaned_text = []
    for row in text:
        if text_check(row,list1):
            pass
        elif len(row) == 0:
            pass
        else:
            cleaned_text.append(row)
    return cleaned_text
print(clean_text(text,target))



re_id = lis[0].select_one('section.js-openrice-bookmark.openrice-bookmark')['data-poi-id']
print(re_id)

dfs = []
for i in range(len(lis)):
    re_id = lis[i].select_one('section.js-openrice-bookmark.openrice-bookmark')['data-poi-id']
    relative_path = lis[i].select_one('.title-name').a['href']
    comment_list = []
    page_count = 1
    print(relative_path)
    while True:
        url = 'https://www.openrice.com' + relative_path + f'/reviews?page={page_count}'
        print(url)
        response0 = requests.get(url, headers=x)
        soup0 = BeautifulSoup(response0.text, "html.parser")
        main = soup0.select_one("div.js-sr2-review-main.sr2-review-main")
        title = main.select("div.review-title")
        comment = main.select("div.sr2-review-list-container section.review-container")
        comment_length = len(title)
        if comment_length==0:
            break
        for i in range(comment_length):
            t = title[i].text.strip()
            c = comment[i]
            for a_tag in c.select('a'):
                a_tag.decompose()
            c = c.text.strip().replace('\n','')
            pair = [re_id,t,c]
            comment_list.append(pair)
            if len(comment_list)==20:
                break
        if len(comment_list)==20:
            break
        page_count +=1
    df0 = pd.DataFrame(comment_list, columns=['re_id', 'topic', 'comment'])
    dfs.append(df0)
df = pd.concat(dfs,axis=0)

df.to_csv('comment_info2.csv')





url_list = []
for i in range(len(lis)):
    url_list.append(lis[i].select_one('.title-name').a['href'])


dfs = []
for i in url_list:
    df0 = get_comment(url)
    dfs.append(df)



df = pd.concat(dfs,axis=0)
pd.to_csv('comment_info')


print(re1_comment1)


re1_div = re1_section.select('div.content.js-feature-review se')
print(len(re1_div))

