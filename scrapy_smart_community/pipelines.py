# -*- coding: utf-8 -*-

from MySQLdb import cursors

from twisted.enterprise import adbapi

from scrapy_smart_community.items import ContentItem, NewsItem, NoticeItem


class SmartCommunityPipeline(object):
      # 初始化函数
    # def __init__(self, db_pool):
    #     self.db_pool = db_pool
    #
    # # 从setting配置文件中读取参数
    # @classmethod
    # def form_setting(cls, settings):
    #     # 用一个db_params接受连接数据库的参数
    #     db_params = dict(
    #         host=settings['MYSQL_HOST'],
    #         db=settings['MYSQL_DBNAME'],
    #         user=settings['MYSQL_USER'],
    #         password=settings['MYSQL_PASSWORD'],
    #         port=settings['MYSQL_PORT'],
    #         charset='utf8',
    #         # 设置游标类型
    #         cursorclass=MySQLdb.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     # 创建连接
    #     db_pool = adbapi.ConnectionPool('MySQLdb', **db_params)
    #     # 返回一个pipeline对象
    #     return cls(db_pool)
    #
    # # 处理item函数
    # def process_item(self, item, spider):
    #     # 把要执行的sql放入连接池
    #     query = self.db_pool.runInteraction(self.do_insert, item)
    #     # 添加 sql 错误
    #     query.addErrback(self.handel_error)
    #     return item
    #
    # # 错误输出函数
    # def handel_error(self, failure):
    #     print failure
    #
    # # sql处理
    # def do_insert(self, cursor, item):
    #     insert_sql = """insert into `t_content` (`id`, `title`, `content`) values ( %s, %s, %s)"""
    #     cursor.execute(insert_sql, (item["id"], item["title"], item["publish_time"]))

    # 保存到数据库中对应的class
    # 1、在settings.py文件中配置
    # 2、在自己实现的爬虫类中yield item,会自动执行

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 1、@classmethod声明一个类方法，而对于平常我们见到的叫做实例方法。
        # 2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
        # 3、可以通过类来调用，就像C.f()，相当于java中的静态方法
        # 读取settings中配置的数据库参数
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    # pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, ContentItem):
            # 咨询详情
            query = self.dbpool.runInteraction(self._conditional_insert, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        elif isinstance(item, NewsItem):
            # 新闻
            query = self.dbpool.runInteraction(self._news_insert, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法
        elif isinstance(item, NoticeItem):
            # 公告
            query = self.dbpool.runInteraction(self._notice_insert, item)  # 调用插入的方法
            query.addErrback(self._handle_error, item, spider)  # 调用异常处理方法

    # 写入t_content中
    # SQL语句在这里
    def _conditional_insert(self, tx, item):
        results = self.get_old_new(tx, item)
        print results
        if not results:
            sql = "insert into `t_content` (`id`, `title`, `content`, `community_id`) " \
                  "values (%s, %s, %s, %s)"
            params = (item["id"], item["title"], item["content"], "1097")
            tx.execute(sql, params)


# 写入t_content中
    def _news_insert(self, tx, item):
        results = self.get_old_new(tx, item)
        print results
        if not results:
            get_tab_id = "select `id` from `t_news_tab` where `name` = '社区新闻';"
            tx.execute(get_tab_id)
            results = tx.fetchall()
            sql = "insert into `t_news` (`id`, `tab_id`, `content_id`, `publish_time`, `community_id`) " \
                  "values (%s, %s, %s, %s, %s)"
            params = (item["id"], results[0]['id'], item["content_id"], item["publish_time"], "1097")
            tx.execute(sql, params)

    # 写入t_content中
    def _notice_insert(self, tx, item):
        results = self.get_old_new(tx, item)
        print results
        if not results:
            get_tab_id = "select `id` from `t_news_tab` where `name` = '社区公告';"
            tx.execute(get_tab_id)
            results = tx.fetchall()
            sql = "insert into `t_news` (`id`, `tab_id`, `content_id`, `publish_time`, `community_id`) " \
                  "values (%s, %s, %s, %s, %s)"
            params = (item["id"], results[0]['id'], item["content_id"], item["publish_time"], "1097")
            tx.execute(sql, params)

    def get_old_new(self, tx, item):
        get_new_id = "select n.`id` from `t_news` n,`t_content` c " \
                     "where n.`publish_time` = %s and c.`title`= %s " \
                     "and n.`content_id` = c.`id` and n.`is_deleted`=0;"
        params = (item["publish_time"], item["title"])
        tx.execute(get_new_id, params)
        results = tx.fetchall()
        return results

    # 错误处理方法
    def _handle_error(self, failue, item, spider):
        print failue
