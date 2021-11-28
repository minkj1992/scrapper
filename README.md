# scrapper
> scrape site

- crawler with [scrapy](https://docs.scrapy.org/en/latest/index.html)
- remove background images [rembg](https://github.com/danielgatis/rembg)


## run scrapper

```bash
$ scrapy crawl juice_mouth
```

- `dk factory`

```
# pwd: ./smoke
$ scrapy crawl dk_mouth -o dk_mouth.json
$ scrapy crawl dk_lung -o dk_lung.json
```

![](./static/입호흡.png)
![크롤링된 이미지 리스트](./static/image_list.png)