import random
from os.path import join, dirname

from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_utils.log import LOG
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media
from youtube_archivist import YoutubeMonitor


class SMODSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__("SMOD")
        self.skill_icon = join(dirname(__file__), "ui", "smod_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "smod_logo.png")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.VIDEO,
                                MediaType.MUSIC]
        # load video catalog
        self.archive = YoutubeMonitor("smod", logger=LOG, blacklisted_kwords=["subscribe"])
        self.n_mixes = 5

    def initialize(self):
        bootstrap = f"https://raw.githubusercontent.com/OpenJarbas/streamindex/main/{self.archive.db.name}.json"
        self.archive.bootstrap_from_url(bootstrap)
        self.archive.setDaemon(True)
        self.archive.start()
        urls = [
            "https://www.youtube.com/c/666MrDoom/videos",
            "https://www.youtube.com/c/StonedMeadowOfDoom2/videos",
            "https://www.youtube.com/c/StonedMeadowOfDoom1993/videos",
            "https://www.youtube.com/channel/UCWf14ZX2SZV4hF-hDVKdGvQ/videos"]
        for url in urls:
            self.archive.monitor(url)

    def match_skill(self, phrase, media_type):
        score = 0
        if self.voc_match(phrase, "music") or media_type == MediaType.MUSIC:
            score += 10
        if self.voc_match(phrase, "doom"):
            score += 25
        if self.voc_match(phrase, "metal"):
            score += 15
        if self.voc_match(phrase, "stoner"):
            score += 30
            if self.voc_match(phrase, "doom"):
                score += 30
        if self.voc_match(phrase, "smod"):
            score += 80
        return score

    @ocp_search()
    def ocp_smod(self, phrase, media_type):
        score = self.match_skill(phrase, media_type)
        if score < 50:
            return
        pl = self.featured_media()
        for i in range(self.n_mixes):
            random.shuffle(pl)
            yield {
                "match_confidence": score,
                "media_type": MediaType.MUSIC,
                "playlist": pl[:100],
                "playback": PlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "skill_id": self.skill_id,
                "image": self.skill_icon,
                "bg_image": self.default_bg,
                "title": f"Stoned Meadow of Doom (Mix {i + 1})"
            }

    @ocp_featured_media()
    def featured_media(self, num_entries=250):
        return [
                   {
                       "match_confidence": 90,
                       "media_type": MediaType.MUSIC,
                       "uri": "youtube//" + entry["url"],
                       "playback": PlaybackType.AUDIO,
                       "image": entry["thumbnail"],
                       "bg_image": self.default_bg,
                       "skill_icon": self.skill_icon,
                       "skill_id": self.skill_id,
                       "title": entry["title"]
                   } for entry in self.archive.sorted_entries()
               ][:num_entries]


def create_skill():
    return SMODSkill()
