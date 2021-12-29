import random
from os.path import join, dirname

from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_workshop.skills.common_play import OVOSCommonPlaybackSkill, \
    ocp_search, ocp_featured_media
from youtube_archivist import YoutubeArchivist


class SMODSkill(OVOSCommonPlaybackSkill):
    def __init__(self):
        super().__init__("SMOD")
        self.skill_icon = join(dirname(__file__), "ui", "smod_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "smod_logo.png")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.VIDEO,
                                MediaType.MUSIC]
        # load video catalog
        self.archive = YoutubeArchivist("smod", blacklisted_kwords=["subscribe"])
        self.n_mixes = 5

    def initialize(self):
        if len(self.archive.db):
            # update db sometime in the next 12 hours, randomized to avoid a huge network load every boot
            # (every skill updating at same time)
            self.schedule_event(self._scheduled_update, random.randint(3600, 12 * 3600))
        else:
            # no database, sync right away
            self.schedule_event(self._scheduled_update, 5)

    def _scheduled_update(self):
        self.update_db()
        self.schedule_event(self._scheduled_update, random.randint(3600, 12 * 3600))  # every 6 hours

    def update_db(self):
        urls = [
            "https://www.youtube.com/c/666MrDoom/videos",
            "https://www.youtube.com/c/StonedMeadowOfDoom2/videos",
            "https://www.youtube.com/c/StonedMeadowOfDoom1993/videos",
            "https://www.youtube.com/channel/UCWf14ZX2SZV4hF-hDVKdGvQ/videos"]
        for url in urls:
            self.archive.archive(url)
        self.archive.remove_unavailable()  # check if video is still available

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
