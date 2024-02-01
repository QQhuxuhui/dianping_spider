# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
import sys

from bs4 import BeautifulSoup

from utils.logger import logger
from utils.get_font_map import get_search_map_file
from utils.requests_utils import requests_util
from utils.spider_config import spider_config
from utils.saver.saver import saver


class Search():
    def __init__(self):
        self.is_ban = False

    def search(self, search_url, request_type='proxy, cookie', last_chance=False):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('搜索页请求被ban，程序终止')
            sys.exit()

        r = requests_util.get_requests(search_url, request_type=request_type)
        # 给一次retry的机会，如果依然403则判断为被ban
        if r.status_code == 403:
            if last_chance is True:
                self.is_ban = True
            return self.search(search_url=search_url, request_type=request_type, last_chance=True)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # 如果页面出现了not-found(无数据)提示，返回None给上一层，让上一层的for循环退出
        if html.select(".not-found-right"):
            return None
        shop_all_list = html.select('.shop-list')[0].select('li')

        search_res = []
        for shop in shop_all_list:
            try:
                image_path = shop.select('.pic')[0].select('a')[0].select('img')[0]['src']
            except:
                image_path = '-'
            try:
                shop_id = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['data-shopid']
            except:
                shop_id = '-'
            try:
                detail_url = shop.select('.txt')[0].select('.tit')[0].select('a')[0]['href']
            except:
                detail_url = '-'
            try:
                name = shop.select('.txt')[0].select('.tit')[0].select('a')[0].text.strip()
            except:
                name = '-'
            # 两个star方式，有的页面显示详细star分数，有的显示icon
            # 解析icon
            try:
                star_point = \
                    shop.select('.txt')[0].select('.comment')[0].select('.star_icon')[0].select('span')[0]['class'][
                        1].split('_')[1]
                star_point = float(star_point) / 10
                star_point = str(star_point)
            except:
                star_point = '-'
            # 解析详细star
            try:
                star_point = \
                    shop.select('.txt')[0].select('.comment')[0].select('.star_score')[0].text
                star_point = float(star_point)
                star_point = str(star_point)
            except:
                pass
            try:
                review_number = shop.select('.txt')[0].select('.comment')[0].select('.review-num')[0].text.replace(
                    '\n', '')
            except:
                review_number = '-'
            try:
                mean_price = shop.select('.txt')[0].select('.comment')[0].select('.mean-price')[0].select('b')[
                    0].text
            except:
                mean_price = '￥0'
            try:
                tags = shop.select('.txt')[0].select('.tag-addr')[0].select('.tag')
                tag1 = tags[0].text.replace('\n', ' ').strip()
                tag2 = tags[1].text.replace('\n', ' ').strip()
            except:
                tag1 = '-'
                tag2 = '-'
            try:
                addr = shop.select('.txt')[0].select('.tag-addr')[0].select('.addr')[0].text.replace('\n',
                                                                                                     ' ').strip()
            except:
                addr = '-'
            try:
                recommend = shop.select('.recommend')[0].text.replace('\n', ' ').strip()
            except:
                recommend = '-'
            try:
                comment_list = shop.select('.comment-list')[0].text.replace('\n', ' ').strip()
            except:
                comment_list = '-'
            one_step_search_res = {
                '店铺id': shop_id,
                '店铺名': name,
                '评论总数': review_number,
                '人均价格': mean_price,
                '标签1': tag1,
                '标签2': tag2,
                '店铺地址': addr,
                '详情链接': detail_url,
                '图片链接': image_path,
                '店铺均分': comment_list,
                '推荐菜': recommend,
                '店铺总分': star_point,
            }
            search_res.append(one_step_search_res)
            # yield one_step_search_res
        return search_res



    def searchParams(self, search_url, request_type='proxy, cookie', last_chance=False):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('搜索页请求被ban，程序终止')
            sys.exit()

        r = requests_util.get_requests(search_url, request_type=request_type)
        # 给一次retry的机会，如果依然403则判断为被ban
        if r.status_code == 403:
            if last_chance is True:
                self.is_ban = True
            return self.search(search_url=search_url, request_type=request_type, last_chance=True)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # 如果页面出现了not-found(无数据)提示，返回None给上一层，让上一层的for循环退出
        if html.select(".not-found-right"):
            return None
        
        # 获取地点列表
        region_list = self.regions('https://www.dianping.com/search/keyword/92/10_%E7%BE%8E%E9%A3%9F/r3862',request_type)
        for region in region_list:
            print('保存区域：', region)
            saver.save_data(region, 'region_1')


        # 获取分类列表
        classfy_a = html.select('#classfy a')
        classfy_list = []
        for classfy in classfy_a:
            try:
                classfy_href = classfy.get('href')
            except:
                classfy_href = None
            try:
                classfy_id = classfy.get('data-cat-id')
            except:
                classfy_id = None
            try:
                classfy_text = classfy.find('span').text
            except:
                classfy_text = None   
            # 一级分类
            if classfy_href is not None and classfy_id is not None and classfy_text is not None:  
                one_step_search_res = {
                    'href': classfy_href,
                    '分类id': classfy_id, 
                    '分类名称': classfy_text
                }
                print(one_step_search_res)
            # print(one_step_search_res)
            # if classfy_href is not None and classfy_id is not None and classfy_text is not None:             
            #     # 获取子分类
            #     print("子分类连接：", classfy_href)
            #     classfy_sub_list = self.classfySub(classfy_href, request_type);
            # if not classfy_sub_list: # 子分类为空，则以第一级分类查询
            #     one_step_search_res = {
            #         'href': classfy_href,
            #         '分类id': classfy_id, 
            #         '分类名称': classfy_text
            #     }
            #     # print(one_step_search_res)
            #     classfy_sub_list.append(one_step_search_res)
                
            classfy_list.append(one_step_search_res)
        for classfy in classfy_list:
            print('保存分类：', classfy)
            saver.save_data(classfy, 'classfy_1')

        return classfy_list
    


    def classfySub(self, search_url, request_type='proxy, cookie', last_chance=False):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('搜索页请求被ban，程序终止')
            sys.exit()

        r = requests_util.get_requests(search_url, request_type=request_type)
        # 给一次retry的机会，如果依然403则判断为被ban
        if r.status_code == 403:
            if last_chance is True:
                self.is_ban = True
            return self.search(search_url=search_url, request_type=request_type, last_chance=True)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # print(html)
        # 如果页面出现了not-found(无数据)提示，返回None给上一层，让上一层的for循环退出
        if html.select(".not-found-right"):
            return None
        # 获取分类列表
        search_res = []
        classfy_sub_list = html.select('#classfy-sub a')
        print("子分类连接列表：", classfy_sub_list)
        if not classfy_sub_list:
            # 返回空表示没有子分类，交予上层调用空数组
            return [];
        for classfy_sub in classfy_sub_list:
            # print("-------", classfy_sub)
            # 获取子分类列表
            try:
                classfy_href = classfy_sub.get('href')
            except:
                classfy_href = None
            try:
                classfy_id = classfy_sub.get('data-cat-id')
            except:
                classfy_id = None
            try:
                classfy_text = classfy_sub.find('span').text
            except:
                classfy_text = None    
            # 一级分类
            if classfy_id is not None and classfy_href is not None and classfy_text:
                one_step_search_res = {
                    'href': classfy_href,
                    '分类id': classfy_id, 
                    '分类名称': classfy_text
                }
            # print(one_step_search_res)
            search_res.append(one_step_search_res)                
            # if classfy_id is not None and classfy_href is not None and classfy_text:
            #     one_step_search_res = {
            #         'href': classfy_href,
            #         '分类id': classfy_id, 
            #         '分类名称': classfy_text
            #     }
            #     # print(one_step_search_res)
            #     search_res.append(one_step_search_res)
        return search_res    
    
    #  获取所有行政区地点位置，这里的url需要写死，爬取徐州的就写死：https://www.dianping.com/search/keyword/92/10_%E7%BE%8E%E9%A3%9F/r3862
    def regions(self, search_url, request_type='proxy, cookie', last_chance=False):
        """
        搜索
        :param key_word: 关键字
        :param only_need_first: 只需要第一条
        :param needed_pages: 需要多少页
        :return:
        """
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('搜索页请求被ban，程序终止')
            sys.exit()

        r = requests_util.get_requests(search_url, request_type=request_type)
        # 给一次retry的机会，如果依然403则判断为被ban
        if r.status_code == 403:
            if last_chance is True:
                self.is_ban = True
            return self.search(search_url=search_url, request_type=request_type, last_chance=True)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # print(html)
        # 如果页面出现了not-found(无数据)提示，返回None给上一层，让上一层的for循环退出
        if html.select(".not-found-right"):
            return None
        # 获取一级区域
        one_region_list = html.select('#region-nav a')
        print("一级区域", one_region_list)
        search_res = []
        for one_region in one_region_list:
            print("-------", one_region)
            # 获取子分类列表
            try:
                one_region_href = one_region.get('href')
            except:
                one_region_href = None
            try:
                one_region_id = one_region.get('data-cat-id')
            except:
                one_region_id = None
            try:
                one_region_text = one_region.find('span').text
            except:
                one_region_text = None 
            one_step_search_res = {
                'href': one_region_href,
                '区域id': one_region_id, 
                '区域名称': one_region_text
            }
            search_res.append(one_step_search_res)                   
            # if one_region_id is not None and one_region_href is not None and one_region_text:
            #     result = self.subRegion(one_region_href, request_type)
            #     search_res.extend(result)
        return search_res      
    
    # 通过一级区域连接获取二级区域
    def subRegion(self, search_url, request_type='proxy, cookie', last_chance=False):
        if self.is_ban and spider_config.USE_COOKIE_POOL is False:
            logger.warning('搜索页请求被ban，程序终止')
            sys.exit()
        r = requests_util.get_requests(search_url, request_type=request_type)
        # 给一次retry的机会，如果依然403则判断为被ban
        if r.status_code == 403:
            if last_chance is True:
                self.is_ban = True
            return self.search(search_url=search_url, request_type=request_type, last_chance=True)
        text = r.text
        # 获取加密文件
        file_map = get_search_map_file(text)
        # 替换加密文件
        text = requests_util.replace_search_html(text, file_map)

        # 网页解析
        html = BeautifulSoup(text, 'lxml')
        # 如果页面出现了not-found(无数据)提示，返回None给上一层，让上一层的for循环退出
        if html.select(".not-found-right"):
            return None
        # 获取二级区域列表
        two_region_list = html.select('#region-nav-sub a')
        two_region_res = []
        for two_region in two_region_list:
            try:
                two_region_href = two_region.get('href')
            except:
                two_region_href = None
            try:
                two_region_id = two_region.get('data-cat-id')
            except:
                two_region_id = None
            try:
                two_region_text = two_region.find('span').text
            except:
                two_region_text = None
            if two_region_id is not None and two_region_href is not None and two_region_text:
                one_step_search_res = {
                    'href': two_region_href,
                    '区域id': two_region_id, 
                    '区域名称': two_region_text
                }
                two_region_res.append(one_step_search_res)
        return two_region_res