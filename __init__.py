from os.path import join, dirname, basename
import random

from mycroft.skills.core import intent_file_handler
from ovos_plugin_common_play.ocp import MediaType, PlaybackType
from ovos_workshop.skills.common_play import ocp_search
from ovos_workshop.skills.video_collection import VideoCollectionSkill
from pyvod import Collection


class SMODSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("SMOD")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.default_image = join(dirname(__file__), "ui", "smod_logo.png")
        self.skill_icon = join(dirname(__file__), "ui", "smod_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "smod_logo.png")
        self.supported_media = [MediaType.GENERIC,
                                MediaType.VIDEO,
                                MediaType.MUSIC]
        path = join(dirname(__file__), "res", "smod.jsondb")
        # load video catalog
        self.media_collection = Collection("smod", logo=self.skill_icon,
                                           db_path=path)
        self.n_mixes = 3

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    def get_base_score(self, phrase, media_type):
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
        score = self.get_base_score(phrase, media_type)
        if score < 50:
            return
        pl = [
            {
                "match_confidence": score,
                "media_type": MediaType.MUSIC,
                "uri": "youtube//" + entry["url"],
                "playback": PlaybackType.AUDIO,
                "image": entry["logo"],
                "bg_image": self.default_bg,
                "skill_icon": self.skill_icon,
                "title": entry["title"]
            } for entry in self.videos  # VideoCollectionSkill property
        ]
        for i in range(self.n_mixes):
            random.shuffle(pl)
            yield {
                "match_confidence": score,
                "media_type": MediaType.MUSIC,
                "playlist": pl[:50],
                "playback": PlaybackType.AUDIO,
                "skill_icon": self.skill_icon,
                "image": self.skill_icon,
                "bg_image": self.default_bg,
                "title": f"Stoned Meadow of Doom (Mix {i + 1})"
            }


def create_skill():
    return SMODSkill()
