from api import light_novel_api
import bs4

LN_BASE_URL = "https://www.lightnovelpub.com/novel/"


class LightNovel:
    def __init__(self, private_name: str, api: light_novel_api.LightNovelApi, latest_chap: int = -1, emoji: str = None,
                 channel_id: int = -1):
        self.private_name = private_name
        self.api = api
        self.latest_chap = latest_chap
        self.emoji = emoji
        self.channel_id = channel_id

    def get_url(self) -> str:
        return LN_BASE_URL + self.private_name

    def get_chaps_url(self) -> str:
        return self.get_url() + "/chapters"

    def get_name(self) -> str:
        req = self.api.get(self.get_url())
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        return soup.find("meta", {"property": "og:title"})["content"].split("|")[0][:-1]

    def get_latest_chap(self) -> int:
        req = self.api.get(self.get_chaps_url())
        soup = bs4.BeautifulSoup(req.text, features="html.parser")
        list_page = soup.find("article", {"id": "chapter-list-page"})
        header = list_page.find("header", {"class": "container"})
        latest_chap_text: bs4.Tag = header.find_all("p")[1]
        chap_num = latest_chap_text.find("a")["href"].split("/")[-1].split("-")[-1]
        return int(chap_num)

    def update_latest_ep(self):
        self.latest_chap = self.get_latest_chap()

    def to_dict(self) -> dict:
        d = self.__dict__
        d.pop("api")
        return d

    @staticmethod
    def from_dict(origin_dict, api):
        return LightNovel(origin_dict["private_name"], api, origin_dict["latest_chap"], origin_dict["emoji"], origin_dict["channel_id"])

