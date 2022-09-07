# torcc
用于rss下载种子，对其中各项逐一解析种子详情页面中的IMDb值，将种子加入下载器时添加IMDb标签。 

## 安装 
```sh
git clone https://github.com/ccf-2012/torcc.git
cd torcc
pip install -r requirements.txt
```


## 使用
```
python torcc.py -h

usage: torcc.py [-h] [-H HOST] [-P PORT] [-u USERNAME] [-p PASSWORD] [-R RSS] [-s SINGLE] [-c COOKIE] [--title-regex TITLE_REGEX]
                [--info-regex INFO_REGEX] [--info-not-regex INFO_NOT_REGEX] [--add-pause] [--exclude-no-imdb]

A script to rss pt site, add torrent to qbit with IMDb id as a tag.

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  the qbittorrent host ip.
  -P PORT, --port PORT  the qbittorrent port.
  -u USERNAME, --username USERNAME
                        the qbittorrent usernmae.
  -p PASSWORD, --password PASSWORD
                        the qbittorrent password.
  -R RSS, --rss RSS     the rss link.
  -s SINGLE, --single SINGLE
                        the detail page of the torrent.
  -c COOKIE, --cookie COOKIE
                        the cookie to the detail page.
  --title-regex TITLE_REGEX
                        regex to match the rss title.
  --info-regex INFO_REGEX
                        regex to match the info/detail page.
  --info-not-regex INFO_NOT_REGEX
                        regex to not match the info/detail page.
  --add-pause           Add torrent in PAUSE state.
  --exclude-no-imdb     Donot download without IMDb.
```

* 注： 不加 `--cookie` 不解析种子信息页，不加qBit的 `--host` 和 `--username` 就不会添加下载器


## 示例
* 从rss链接中，逐个获取种子详情页，提取IMDb id并将种子发送至下载器，打上IMDB标签
```sh
python torcc.py -R "https://some.pt.site/torrentrss.php?rows=10&..." -c "c_secure_uid=ABCDE; ....c_secure_tracker_ssl=bm9wZQ=="  -H qb.server.ip -P 8088 -u qb_user -p qb_pass
```

* 取单个页面，提取IMDb id并将种子发送至下载器，打上IMDB标签
```sh
python torcc.py -i "https://some.pt.site/details.php?id=60381"  -c "c_secure_uid=ABCDE; ....c_secure_tracker_ssl=bm9wZQ=="  -H qb.server.ip -P 8088 -u qb_user -p qb_pass
```

* 标题中包含 x264 且以 ADE 结尾的
```sh
python torcc.py --title-regex 'x264.*[-@]?ADE$' -i "https://some.pt.site/details.php?id=60381"  -c "c_secure_uid=ABCDE; ....c_secure_tracker_ssl=bm9wZQ=="  -H qb.server.ip -P 8088 -u qb_user -p qb_pass
```

* 信息详情页可解析到更多信息，提供了 `--info-regex` 和 `--info-not-regex` 两个正则，下面例子是：排除国语，且有IMDb的ADWeb后缀种子：
```sh
python torcc.py --title-regex '[-@]?ADWeb' --info-not-regex '\"tags tgy\"' --exclude-no-imdb -i "https://some.pt.site/details.php?id=60381"  -c "c_secure_uid=ABCDE; ....c_secure_tracker_ssl=bm9wZQ=="  -H qb.server.ip -P 8088 -u qb_user -p qb_pass
```

