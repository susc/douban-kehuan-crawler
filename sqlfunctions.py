import pymysql


class dbsqlfunctions:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'alpha'
    MYSQL_PASS = 'alpha520'
    MYSQL_DB = 'douban_kehuan'

    # 向movies表中插入记录
    def insert_movies(self, urlid, title, year, rate, url, imdb_url, rates, _5star, _4star, _3star, _2star, _1star, comments, watched, want_to_watch):
        db = pymysql.connect(self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASS, self.MYSQL_DB)
        cursor = db.cursor()
        url = pymysql.escape_string(url)
        sql = r"INSERT INTO `movies` (`sysid`, `urlid`, `title`, `year`, `rate`, `url`, `imdb_url`, `rates`, `_5star`, `_4star`, `_3star`, `_2star`, `_1star`, `comments`, `watched`, `want_to_watch`) VALUES (NULL , '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(urlid, title, year, rate, url, imdb_url, rates, _5star, _4star, _3star, _2star, _1star, comments, watched, want_to_watch)
        try:
            cursor.execute(sql)
            db.commit()
            print('插入成功：URL:{}, 标题:{}, 评分:{}'.format(url, title, rate))
        except Exception:
            print('\033[1;30;41m【错误】\033[0m插入失败, SQL:', sql)
            db.rollback()
        db.close()

    # 判断当前电影是否存在
    def isurlidexists(self, urlid):
        db = pymysql.connect(self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASS, self.MYSQL_DB)
        cursor = db.cursor()
        sql = r"SELECT * FROM `movies` WHERE `urlid` = {}".format(str(urlid))
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        return result is not None

    # 更新看过的人数以及想看的人数
    def update_ww(self, urlid, watched, want_to_watch):
        db = pymysql.connect(self.MYSQL_HOST, self.MYSQL_USER, self.MYSQL_PASS, self.MYSQL_DB)
        cursor = db.cursor()
        sql = r"UPDATE `movies` SET `watched` = '{}', `want_to_watch` = '{}' WHERE `movies`.`urlid` = {}".format(watched, want_to_watch, urlid)
        try:
            cursor.execute(sql)
            db.commit()
            print('更新成功：URL id:{}, 看过的人:{}, 想看的人: {}'.format(urlid, watched, want_to_watch))
        except Exception:
            print('\033[1;30;41m【错误】\033[0mERROR in update_clickcount, SQL:', sql)
            db.rollback()
        db.close()
