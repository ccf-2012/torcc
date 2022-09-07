# -*- coding: utf-8 -*-
"""
A script to rss and parse the info page of a torrent to get IMDb id, 
add torrent to the qbit client with this IMDb id as a tag.
"""
import re
import argparse
import requests
from http.cookies import SimpleCookie
import urllib
import qbittorrentapi
import feedparser
import datetime

from humanbytes import HumanBytes
# from lxml import etree

DOWNLOAD_URL_RE = [
    r'https?://(\w+\.)?\w+\.\w+/download\.php\?id=(\d+)&downhash=(\w+)',
    r'https?://(\w+\.)?\w+\.\w+/download\.php\?id=(\d+)&passkey=(\w+)',
]


def rssGetDetailAndDownload(rsslink):
    feed = feedparser.parse(rsslink)
    rssSum = 0
    rssAccept = 0
    for item in feed.entries:
        if not hasattr(item, 'id'):
            print('No id')
            continue
        if not hasattr(item, 'title'):
            print('No title')
            continue

        rssSum += 1
        print("%d: %s -- %s " % (rssSum, item.title, datetime.datetime.now().strftime("%H:%M:%S")))

        if ARGS.title_regex:
            if not re.search(ARGS.title_regex, item.title, re.I):
                print(' Title regex not match.')
                continue

        imdbstr = ''
        if hasattr(item, 'link'):
            if ARGS.cookie:
                match, imdbstr, downlink = parseDetailPage(item.link, ARGS.cookie)
                if not match:
                    print(' Info page regex not match.')
                    continue
                if ARGS.exclude_no_imdb and (not imdbstr):
                    print(' Exclue media without IMDb.')
                    continue

        if hasattr(item, 'links') and len(item.links) > 1:
            rssDownloadLink = item.links[1]['href']
            rssSize = item.links[1]['length']
            # Download
            rssAccept += 1
            print('   %s (%s), %s' % (imdbstr, HumanBytes.format(int(rssSize)), rssDownloadLink))
            if ARGS.host and ARGS.username:
                r = addQbitWithTag(rssDownloadLink, imdbstr)
    print('Total: %d, Accepted: %d ' % (rssSum, rssAccept))


def addQbitWithTag(downlink, imdbtag):
    qbClient = qbittorrentapi.Client(host=ARGS.host, port=ARGS.port, username=ARGS.username, password=ARGS.password)

    try:
        qbClient.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    if not qbClient:
        return False

    try:
        # curr_added_on = time.time()
        result = qbClient.torrents_add(
            urls=downlink,
            is_paused=ARGS.add_pause,
            # save_path=download_location,
            # download_path=download_location,
            # category=timestamp,
            tags=[imdbtag],
            use_auto_torrent_management=False)
        # breakpoint()
        if 'OK' in result.upper():
            print('Torrent added.')
        else:
            print('Torrent not added! something wrong with qb api ...')
    except Exception as e:
        print('Torrent not added! Exception: '+str(e))
        return False

    return True

    

# def findConfig(infoUrl):
#     hostnameList = urllib.parse.urlparse(infoUrl).netloc.split('.')
#     abbrev = hostnameList[-2] if len(hostnameList) >= 2 else ''
#     return next(filter(lambda ele: ele['host'] == abbrev, SITE_CONFIGS), None)


def parseDetailPage(pageUrl, pageCookie):
    cookie = SimpleCookie()
    cookie.load(pageCookie)
    cookies = {k: v.value for k, v in cookie.items()}
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    doc = requests.get(pageUrl, headers=headers, cookies=cookies).text

    if ARGS.info_regex:
        m0 = re.search(ARGS.info_regex, doc, flags=re.A)
        if not m0:
            # print('Info regex not match.')
            return False, '', ''
    if ARGS.info_not_regex:
        m0 = re.search(ARGS.info_not_regex, doc, flags=re.A)
        if m0:
            # print('Info regex not match.')
            return False, '', ''

    imdbstr = ''
    imdbRe = r'IMDb(链接)\s*(\<.[!>]*\>)?.*https://www\.imdb\.com/title/tt(\d+)'
    m1 = re.search(imdbRe, doc, flags=re.A)
    if m1:
        imdbstr = 'tt' + m1[3]

    for reUrl in DOWNLOAD_URL_RE:
        if re.search(reUrl, doc, flags=re.A):
            break
    downlink = ''
    m2 = re.search(reUrl, doc, flags=re.A)
    if m2:
        downlink = m2[0]

    return True, imdbstr, downlink


def loadArgs():
    parser = argparse.ArgumentParser(
        description='A script to rss pt site, add torrent to qbit with IMDb id as a tag.'
    )
    parser.add_argument('-H', '--host', help='the qbittorrent host ip.')
    parser.add_argument('-P', '--port', help='the qbittorrent port.')
    parser.add_argument('-u', '--username', help='the qbittorrent usernmae.')
    parser.add_argument('-p', '--password', help='the qbittorrent password.')
    parser.add_argument('-R', '--rss', help='the rss link.')
    parser.add_argument('-s', '--single', help='the detail page of the torrent.')
    parser.add_argument('-c', '--cookie', help='the cookie to the detail page.')
    parser.add_argument('--title-regex', help='regex to match the rss title.')
    parser.add_argument('--info-regex', help='regex to match the info/detail page.')
    parser.add_argument('--info-not-regex', help='regex to not match the info/detail page.')
    parser.add_argument('--add-pause',
                        action='store_true',
                        help='Add torrent in PAUSE state.')
    parser.add_argument('--exclude-no-imdb',
                        action='store_true',
                        help='Donot download without IMDb.')
    global ARGS
    ARGS = parser.parse_args()


def main():
    loadArgs()
    if ARGS.rss:
        rssGetDetailAndDownload(ARGS.rss)

    elif ARGS.single:
        if ARGS.cookie:
            imdbstr, downlink = parseDetailPage(ARGS.info_url, ARGS.cookie)
            if not downlink:
                print("Error: download link not found")
                return
            print(imdbstr, downlink)
            r = addQbitWithTag(downlink, imdbstr)


if __name__ == '__main__':
    main()