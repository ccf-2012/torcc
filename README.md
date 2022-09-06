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

usage: torcc.py [-h] [-H HOST] [-P PORT] [-u USERNAME] [-p PASSWORD] [-R RSS] [-i INFO_URL] [-c COOKIE] [--regex REGEX]

torcp: a script hardlink media files and directories in Emby-happy naming and structs.

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  the qbittorrent host ip.
  -P PORT, --port PORT  the qbittorrent port.
  -u USERNAME, --username USERNAME
                        the qbittorrent usernmae.
  -p PASSWORD, --password PASSWORD
                        the qbittorrent password.
  -R RSS, --rss RSS     the rss link.
  -i INFO_URL, --info-url INFO_URL
                        the detail page contains imdb/douban id.
  -c COOKIE, --cookie COOKIE
                        the cookie to the detail page.
  --regex REGEX         regex to match the rss title.
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
