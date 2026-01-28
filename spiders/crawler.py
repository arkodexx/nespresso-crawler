import scrapy
from scrapy.http import JsonRequest
from datetime import datetime, timezone

class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["nespresso.com", "platform-eu.cloud.coveo.com"]

    queries = ["Machines", "Accessory"] # Enter which queries you want
    query_now = 0
    URL = "https://platform-eu.cloud.coveo.com/rest/search/v2?organizationId=nespressoproductiong3iqhhz5"
    firstresult = 0
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

    headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0",
      "Accept": "*/*",
      "Accept-Language": "de,en-US;q=0.9,en;q=0.8",
      "Accept-Encoding": "gzip, deflate, br, zstd",
      "Content-Type": "application/json",
      "Authorization": "Bearer xxc997e6c1-d94a-4d9f-b8fb-0c641f6813f3",
      "Connection": "keep-alive",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "cross-site",
      "Sec-GPC": "1",
      "Priority": "u=4",
      "origin": "https://www.nespresso.com"
    }

    params = {
  "locale": "en",
  "timezone": "Europe/Berlin",
  "visitorId": "db19847b-aa14-4db5-84dc-03e1d62c8f58",
  "aq": "@commontab==\"Products\"",
  "enableDidYouMean": True,
  "q": queries[query_now],
  "numberOfResults": 15,
  "firstResult": firstresult,
  "fieldsToInclude": [
    "author",
    "language",
    "urihash",
    "objecttype",
    "collection",
    "source",
    "permanentid",
    "date",
    "parents",
    "commontab",
    "filetype",
    "nes_prd_sku",
    "nes_prd_image_url",
    "nes_prd_categories",
    "nes_prd_sleeve_main_price",
    "nes_prd_name",
    "nes_prd_price",
    "nes_prd_technology",
    "nes_prd_technology_name",
    "faq_question",
    "faq_answer",
    "nes_prd_cup_size_oz",
    "nes_prd_sales_multiple",
    "nes_prd_cup_size",
    "nes_prd_unit_quantity",
    "nes_article_category",
    "nes_prd_color",
    "nes_prd_color_css",
    "nes_prd_usage",
    "nes_prd_intensity",
    "nes_prd_quantities",
    "nes_prd_bundled",
    "nes_prd_strikethrough_price",
    "nes_prd_tasting_notes",
    "nes_prd_rating",
    "nes_prd_in_stock",
    "nes_prd_collection"
  ],
  "facetOptions": {
    "freezeFacetOrder": True
  },
  "facets": [
    {
      "facetId": "nes_prd_technology",
      "field": "nes_prd_technology",
      "type": "specific",
      "currentValues": [
        { "value": "Vertuo", "state": "idle" },
        { "value": "Original", "state": "idle" },
        { "value": "Pro", "state": "idle" },
        { "value": "Milk Devices", "state": "idle" }
      ]
    },
    {
      "facetId": "nes_prd_categories",
      "field": "nes_prd_categories",
      "type": "specific",
      "currentValues": [
        { "value": "Capsule", "state": "idle" },
        { "value": "Machine", "state": "idle" },
        { "value": "Accessory", "state": "idle" }
      ]
    },
    {
      "facetId": "nes_prd_price",
      "field": "nes_prd_price",
      "type": "numericalRange",
      "currentValues": [
        { "start": 0, "end": 25, "state": "idle" },
        { "start": 25, "end": 50, "state": "idle" },
        { "start": 50, "end": 100, "state": "idle" },
        { "start": 100, "end": 200, "state": "idle" },
        { "start": 200, "end": 1000, "state": "idle" }
      ]
    }
  ],
  "searchHub": "Nespresso_US_EN_Search",
  "analytics": {
    "clientId": "db19847b-aa14-4db5-84dc-03e1d62c8f58",
    "clientTimestamp": timestamp,
    "originContext": "Search",
    "documentLocation": f"https://www.nespresso.com/us/en/search?q=Machines&tab=Products&p=1"
  },
  "context": {
    "website": "Nespresso_US",
    "sitename": "Nespresso_US",
    "language": "en",
    "locale": "en-US",
    "country": "us"
  }
}
    async def start(self):
        yield self.build_request()

    def build_request(self):
        self.now = datetime.now(timezone.utc)
        self.timestamp = self.now.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        self.params["firstResult"] = self.firstresult
        self.params["q"] = self.queries[self.query_now]
        payload = self.params
        return JsonRequest(url=self.URL, callback=self.parse, dont_filter=True, data=payload, headers=self.headers, method="POST", meta={"impersonate": "chrome120"})

    def parse(self, response):
        data = response.json()
        items = data["results"]
        if not items:
            self.query_now += 1
            self.firstresult = 0
            if self.query_now <= len(self.queries):
                yield self.build_request()
            else:
                return
        for item in items:
            yield {
                "title": item["title"],
                "price": item["raw"]["nes_prd_price"],
                "category": item["raw"]["nes_prd_categories"],
                "url": item["uri"],
            }
        self.firstresult += 15
        yield self.build_request()