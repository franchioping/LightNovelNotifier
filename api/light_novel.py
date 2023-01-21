from api import light_novel_api
import bs4

import discord

LN_BASE_URL = "https://www.lightnovelpub.com/novel/"


class LightNovel:
    def __init__(self, private_name: str, api: light_novel_api.LightNovelApi, latest_chap: int = -1,
                 channel_id: int = -1, role_id: int = -1, emoji: str = ""):
        self.private_name = private_name
        self.api = api
        self.latest_chap = latest_chap
        self.channel_id = channel_id
        self.role_id = role_id
        self.emoji = emoji

    def get_url(self) -> str:
        return LN_BASE_URL + self.private_name

    def get_chaps_url(self) -> str:
        return self.get_url() + "/chapters"

    def get_name(self) -> str:
        req = self.api.get(self.get_url())
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        return soup.find("meta", {"property": "og:title"})["content"].split("|")[0][:-1]

    def get_image_url(self) -> str:
        req = self.api.get(self.get_url())
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        ln_header = soup.find("body").find("main").find("header", {"class": "novel-header"})
        img_div = ln_header.find("div", {"class": "header-body container"}).find("div", {"class": "fixed-img"})
        img = img_div.find("figure").find("img")

        return img["data-src"]

    def get_latest_chap(self) -> int:
        req = self.api.get(self.get_chaps_url())
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        list_page = soup.find("article", {"id": "chapter-list-page"})
        header = list_page.find("header", {"class": "container"})
        latest_chap_text: bs4.Tag = header.find_all("p")[1]
        chap_num = latest_chap_text.find("a")["href"].split("/")[-1].split("-")[-1]
        return int(chap_num)

    def update_latest_chap(self):
        self.latest_chap = self.get_latest_chap()

    def get_embed(self, time_str: str, ep: int):
        embed = discord.Embed(title=f"New Chapter Of {self.get_name()} Manga",
                              url=self.get_chaps_url(),
                              description=f"Chapter {ep} just dropped at {time_str} GMT",
                              color=discord.Color.blue())
        embed.set_thumbnail(url=self.get_image_url())

        return embed

    def to_dict(self) -> dict:
        d = self.__dict__
        d.pop("api")
        return d

    @staticmethod
    def from_dict(origin_dict, api):
        return LightNovel(private_name=origin_dict["private_name"], api=api, latest_chap=origin_dict["latest_chap"],
                          channel_id=origin_dict["channel_id"], role_id=origin_dict["role_id"], emoji=origin_dict["emoji"])

