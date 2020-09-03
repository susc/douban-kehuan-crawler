import dbmovies
import sqlfunctions
import time
import random


def main(start=0):
    douban = dbmovies.dbmovies()
    data = douban.get_data_collection(start)
    print('start', start, data)
    if data is not None:
        for item in data:
            title = item['title']
            url = item['url']
            urlid = item['id']
            rate = item['rate']
            if rate == '':
                rate = '0'
            sleeptime = random.randint(0, 5)
            time.sleep(sleeptime)
            year, imdb_url, rates, _5star, _4star, _3star, _2star, _1star, comments, watched, want_to_watch = douban.detail_url_parser(url)
            sqlf = sqlfunctions.dbsqlfunctions()
            if not sqlf.isurlidexists(urlid):
                sqlf.insert_movies(urlid, title, year, rate, url, imdb_url, rates, _5star, _4star, _3star, _2star, _1star, comments, watched, want_to_watch)
            else:
                sqlf.update_ww(urlid, watched, want_to_watch)
        start += 20
        main(start)
    else:
        print('ERROR!')


if __name__ == '__main__':
    main(1320)
