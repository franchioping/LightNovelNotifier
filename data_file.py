import json
from api import light_novel
import discord


class DataFile:
    def __init__(self, filename="data.json"):
        self.data = {}
        self.filename = filename

        self._load()

    def _get_guilds(self) -> dict:
        return self.data["guilds"]

    def get_lns(self, guild: int | discord.Guild) -> list[dict]:
        return self._get_guild(guild)["light_novels"]

    def _get_guild(self, guild: int | discord.Guild):
        guild_id = guild if type(guild) == int else guild.id
        return self._get_guilds()[str(guild_id)]

    def _load(self):
        with open(self.filename, "r") as f:
            self.data = json.load(f)

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def get_guild_id_list(self) -> list[int]:
        guild_list: dict = self.data["guilds"]
        return [int(x) for x in list(guild_list.keys())]

    def set_guild_ln_category_id(self, guild: int | discord.Guild, value: int) -> None:
        guild_id = guild if type(guild) == int else guild.id
        self._get_guild(guild_id)["ln_category"] = value

    def get_guild_ln_category_id(self, guild: int | discord.Guild) -> int:
        guild_id = guild if type(guild) == int else guild.id
        return int(self._get_guild(guild_id)["ln_category"])

    def set_guild_select_channel_id(self, guild: int | discord.Guild, value: int) -> None:
        guild_id = guild if type(guild) == int else guild.id
        self._get_guild(guild_id)["select_channel_id"] = value

    def get_guild_select_channel_id(self, guild: int | discord.Guild) -> int:
        guild_id = guild if type(guild) == int else guild.id
        return int(self._get_guild(guild_id)["select_channel_id"])

    def set_guild_select_message_id(self, guild: int | discord.Guild, value: int) -> None:
        guild_id = guild if type(guild) == int else guild.id
        self._get_guild(guild_id)["select_message_id"] = value

    def get_guild_select_message_id(self, guild: int | discord.Guild) -> int:
        guild_id = guild if type(guild) == int else guild.id
        return int(self._get_guild(guild_id)["select_message_id"])

    def add_ln(self, guild: int | discord.Guild, ln: light_novel.LightNovel):
        self.get_lns(guild).append(ln.to_dict())
        print(self.data)
        self._save()

    def update_ln(self, guild: int | discord.Guild, ln: light_novel.LightNovel):
        lns = self._get_guild(guild)["light_novels"]
        for i in range(len(lns)):
            if lns[i]["private_name"] == ln.private_name:
                lns[i] = ln.to_dict()