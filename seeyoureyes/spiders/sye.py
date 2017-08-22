# coding: utf-8

import json
import urllib

import scrapy
from scrapy import Request

class sye(scrapy.Spider):

    name = "sye"

    __wanna_sim_numbers = 100
    __get_id_list_url = "https://stye.sourceaudio.com/ajax.php?p=track_info&o=release_date&d=d&show=50&pg={}&no=title&req=1"
    __search_url      = "https://stye.sourceaudio.com/ajax.php?p=track_info&s={}&show=50&req=1"
    __detail_info_url = "https://stye.sourceaudio.com/ajax.php?p=track_info&customs=1&id={}"
    __sim_tracks_url  = "https://stye.sourceaudio.com/ajax.php?p=track_info&sim={}&show=50&pg={}&req=1"
    __headers         = {"Host": "stye.sourceaudio.com", "Connection": "keep-alive", "Pragma": "no-cache", "Cache-Control": "no-cache", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Accept-Encoding": "deflate, br", "Accept-Language": "en,zh-CN;q=0.8,zh;q=0.6"}

    def start_requests(self):

        track_page_range = xrange(0, 324)

        for page_index in track_page_range:
            search_url = self.__get_id_list_url.format(urllib.quote(str(page_index)))
            req = Request(
                    url = search_url,
                    headers = self.__headers,
                    meta = {

                        },
                    callback = self.get_track_id,
                    )
            yield req

    '''
    def start_request(self):

        track_names = []

        for track_name in track_names:
            search_url = self.__search_url.format(urllib.quote(track_name))
            req = Request(
                    url = search_url,
                    headers = self.__headers,
                    meta = {
                        'search_name': track_name,

                        },
                    callback = self.get_track_id,
                    )
            yield req
    '''

    def get_track_id(self, response):
        if response.status not in [200, ]:
            pass
        data = json.loads(response.body)

        ''' deal with json data
        '''
        ids = list(map(lambda x: x.get('id', '-1'), data.get('content', [{}, ])[1:]))

        for track_id in ids:

            req = Request(
                    url = self.__detail_info_url.format(urllib.quote(str(track_id))),
                    headers = self.__headers,
                    meta = {
                        'track_id': track_id,

                        },
                    callback = self.deal_with_detail_info,
                    )
            yield req

    def deal_with_detail_info(self, response):
        if response.status not in [200, ]:
            pass
        data = json.loads(response.body)

        '''deal with json data
        '''

        track_detail_info = {
                'data': data,
                }

        ''' return track detail info
            yield track_detail_info
        '''

        sim_page_indexes = range(self.__wanna_sim_numbers / 50)
        req = Request(
                url = self.__sim_tracks_url.format(urllib.quote(str(response.meta['track_id'])), urllib.quote(str(sim_page_indexes[0]))),
                headers = self.__headers,
                meta = {
                    'track_id': response.meta['track_id'],
                    'detail_info': track_detail_info,
                    'sim_page_indexes': sim_page_indexes,
                    'sim_tracks_lists': [],
                    },
                callback = self.deal_with_sim_tracks_list,
                )

        yield req

    def deal_with_sim_tracks_list(self, response):
        if response.status not in [200, ]:
            pass
        data = json.loads(response.body)

        '''deal with json data
        '''

        sim_tracks_list = {
                'data': data,
                }

        sim_tracks_lists = response.meta['sim_tracks_lists']
        sim_tracks_lists.append(sim_tracks_list)

        sim_page_indexes = response.meta['sim_page_indexes']
        del sim_page_indexes[0]

        if len(sim_page_indexes) == 0:
            result = {
                'track_id': response.meta['track_id'],
                'detail_info': response.meta['detail_info'],
                'sim_tracks_list': sim_tracks_lists,

                }

            yield result

        else:
            req = Request(
                    url = self.__sim_tracks_url.format(urllib.quote(str(response.meta['track_id'])), urllib.quote(str(sim_page_indexes[0]))),
                    headers = self.__headers,
                    meta = {
                        'track_id': response.meta['track_id'],
                        'detail_info': response.meta['detail_info'],
                        'sim_page_indexes': sim_page_indexes,
                        'sim_tracks_lists': sim_tracks_lists,

                        },
                    callback = self.deal_with_sim_tracks_list,
                    )
            yield req

