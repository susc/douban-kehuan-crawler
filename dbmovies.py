import requests
import json
import bs4
import re
from requests.cookies import RequestsCookieJar


class dbmovies:
    # 构造请求头
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Referer': 'https://movie.douban.com/tag/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }

    def init_cookie_jar(self):
        cookie_jar = RequestsCookieJar()
        # movie.douban.com部分
        cookie_jar.set("__utma", "223695111.763158393.1538141798.1538226726.1538230909.5", domain=".movie.douban.com")
        cookie_jar.set("__utmb", "223695111.0.10.1538230909", domain=".movie.douban.com")
        cookie_jar.set("__utmc", "223695111", domain=".movie.douban.com")
        cookie_jar.set("__utmv", "", domain=".movie.douban.com")
        cookie_jar.set("__utmz", "223695111.1538141798.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic", domain=".movie.douban.com")
        cookie_jar.set("_pk_id.100001.4cf6", "0481396e936faae0.1538141798.5.1538232563.1538227688.", domain="movie.douban.com")
        cookie_jar.set("_pk_ref.100001.4cf6", "%5B%22%22%2C%22%22%2C1538230909%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DyIaqR-O7pLp-2HfDE2fu7KMvunDeZu3UsflzIcKG7UIOBzlegP3XA7PTm19cTWLz%26wd%3D%26eqid%3Dec34c79e0005754a000000065bae2e60%22%5D", domain="movie.douban.com")
        cookie_jar.set("_pk_ses.100001.4cf6", "*", domain="movie.douban.com")
        # douban.com部分
        cookie_jar.set("__utma", "30149280.232355676.1531973660.1538226726.1538230909.9", domain=".douban.com")
        cookie_jar.set("__utmb", "30149280.0.10.1538230909", domain=".douban.com")
        cookie_jar.set("__utmc", "30149280", domain=".douban.com")
        cookie_jar.set("__utmz", "30149280.1538141798.5.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic", domain=".douban.com")
        cookie_jar.set("_vwo_uuid_v2", "DD84753EC87AAD23B5A27AF4962E7FB54|4981c59d4caccff1cea20dc20ec2fef4", domain=".douban.com")
        cookie_jar.set("ap_v", "0,6.0", domain=".douban.com")
        cookie_jar.set("bid", "DVml1RQSWvE", domain=".douban.com")
        cookie_jar.set("ck", "ZdGN", domain=".douban.com")
        cookie_jar.set("dbcl2", '"185173302:EGD8RTKUVUw"', domain=".douban.com")
        cookie_jar.set("douban-fav-remind", "1", domain=".douban.com")
        cookie_jar.set("gr_user_id", "6aa0dd47-4120-485c-bee9-f46bcc5a13a8", domain=".douban.com")
        cookie_jar.set("ll", '"118282"', domain=".douban.com")
        cookie_jar.set("ps", "y", domain=".douban.com")
        cookie_jar.set("push_doumail_num", "0", domain=".douban.com")
        cookie_jar.set("push_noty_num", "0", domain=".douban.com")
        cookie_jar.set("viewed", '"27001447"', domain=".douban.com")
        # doubanio.com部分
        cookie_jar.set("bid", 'KX7V55VhclE', domain=".doubanio.com")
        # www.douban.com部分
        cookie_jar.set("_pk_id.100001.8cb4", 'be69c408a06675f4.1531973659.3.1535962395.1533005359.', domain="www.douban.com")
        # m.douban.com部分
        cookie_jar.set("frodotk", '"a2509b8f1eb8ded4e6f1d2ad5c2a9c7c"', domain=".m.douban.com")
        return cookie_jar


    # 获取电影数据集合
    def get_data_collection(self, start=0):
        s = requests.session()
        cookie_jar = self.init_cookie_jar()
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}&genres=%E7%A7%91%E5%B9%BB'.format(start)
        request = s.get(url, headers=self.headers, cookies=cookie_jar)
        s.cookies.update(cookie_jar)
        if request.status_code == 200:
            data = json.loads(request.text)
            return data['data']
        else:
            return None

    # 获取IMDb链接
    def get_imdb_url(self, soup):
        imdb_url = soup.find_all('span', attrs={'class': 'pl'})
        for item in imdb_url:
            if isinstance(item.string, str):
                if 'IMDb' in item.string:
                    return item.next_sibling.next_sibling['href']

    # URL内容解析
    def detail_url_parser(self, url):
        s = requests.session()
        cookie_jar = self.init_cookie_jar()
        request = s.get(url, headers=self.headers, cookies=cookie_jar)
        s.cookies.update(cookie_jar)
        request.encoding = 'utf-8'
        html = request.text
        soup = bs4.BeautifulSoup(html, 'lxml')
        # 获取年份
        try:
            year = soup.find('span', attrs={'class': 'year'}).string.strip('()')
        except Exception as e:
            print(url, '获取年份失败：', str(e))
            year = '0'
        # 获取IMDb链接
        try:
            imdb_url = self.get_imdb_url(soup)
        except Exception as e:
            print(url, '获取IMDb链接失败：', str(e))
        # 获取评分人数
        try:
            rates = soup.find('span', attrs={'property': 'v:votes'}).string.strip()
        except Exception as e:
            print(url, '获取评分人数失败：', str(e))
            rates = '0'
        # 获取一到五星百分比
        try:
            _5star = soup.find('span', attrs={'class': 'stars5'}).parent.find('span', attrs={'class': 'rating_per'}).string.strip('%')
            _4star = soup.find('span', attrs={'class': 'stars4'}).parent.find('span', attrs={'class': 'rating_per'}).string.strip('%')
            _3star = soup.find('span', attrs={'class': 'stars3'}).parent.find('span', attrs={'class': 'rating_per'}).string.strip('%')
            _2star = soup.find('span', attrs={'class': 'stars2'}).parent.find('span', attrs={'class': 'rating_per'}).string.strip('%')
            _1star = soup.find('span', attrs={'class': 'stars1'}).parent.find('span', attrs={'class': 'rating_per'}).string.strip('%')
        except Exception as e:
            print(url, '获取星级百分比失败：', str(e))
            _5star = '0'
            _4star = '0'
            _3star = '0'
            _2star = '0'
            _1star = '0'
        # 获取评论人数
        try:
            comments = soup.find('div', attrs={'class': 'mod-hd'}).find('h2').find('a').string
            com_compile = re.compile(r'\d+')
            comments = com_compile.findall(comments)[0]
        except Exception as e:
            print(url, '获取评论人数失败：', str(e))
            comments = '0'
        # 获取看过的人数以及想看的人数
        try:
            ww = soup.find('div', attrs={'class': 'subject-others-interests-ft'})
            ww_links = ww.find_all('a')
            watched = com_compile.findall(ww_links[0].string)[0]
            want_to_watch = com_compile.findall(ww_links[1].string)[0]
        except Exception as e:
            print(url, '获取看过的人数以及想看的人数失败：', str(e))
            watched = '0'
            want_to_watch = '0'
        return year, imdb_url, rates, _5star, _4star, _3star, _2star, _1star, comments, watched, want_to_watch
