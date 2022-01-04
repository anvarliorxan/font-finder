import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import cssutils
import urllib3


class SiteParser:

    def __init__(self, web_site):
        self.__web_site = web_site
        self.__session = requests.Session()
        self.__session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        self.__css_cdn_list = []
        self.__font_famliy_list = []
        self.__error_message = None
        self.parsing()
        self.cdn_parsing()

    def parsing(self):
        try:
            urllib3.disable_warnings()
            page = self.__session.get(self.__web_site, verify=False, timeout=5).content
            soup = bs(page, "html.parser")

            for styles in soup.select('style'):
                sheet = cssutils.parseString(styles.encode_contents())
                for rule in sheet:
                    if rule.type == rule.STYLE_RULE:
                        for property in rule.style:
                            if property.name == 'font-family':
                                if property.value not in self.__font_famliy_list:
                                    self.__font_famliy_list.append(property.value)

            for link in soup.find_all("link"):
                if link.attrs.get("href"):
                    link_url = urljoin(self.__web_site, link.attrs.get("href"))
                    if '.css' in link_url:
                        self.__css_cdn_list.append(link_url)

        except:
            self.__error_message = "Connection refused"

    def cdn_parsing(self):
        for cdn_url in self.__css_cdn_list:
            try:
                css_content = self.__session.get(cdn_url, verify=False, timeout=5).content
                sheet = cssutils.parseString(css_content)

                for rule in sheet:
                    if rule.type == rule.STYLE_RULE:
                        for property in rule.style:
                            if property.name == 'font-family':
                                if property.value not in self.__font_famliy_list:
                                    self.__font_famliy_list.append(property.value)
            except:
                pass

    def get_font_famliy_list(self):
        return self.__font_famliy_list

    def get_error_message(self):
        return self.__error_message