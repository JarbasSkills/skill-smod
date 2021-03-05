from pyvod import Collection
from os.path import join, dirname, basename
from ovos_utils.skills.templates.video_collection import VideoCollectionSkill
from mycroft.skills.core import intent_file_handler
from pyvod import Collection, Media
from os.path import join, dirname, basename
from ovos_utils.playback import CPSMatchType, CPSPlayback, CPSMatchConfidence


class SMODSkill(VideoCollectionSkill):

    def __init__(self):
        super().__init__("SMOD")
        self.message_namespace = basename(dirname(__file__)) + ".jarbasskills"
        self.default_image = join(dirname(__file__), "ui", "smod_logo.png")
        self.skill_logo = join(dirname(__file__), "ui", "smod_icon.png")
        self.skill_icon = join(dirname(__file__), "ui", "smod_icon.png")
        self.default_bg = join(dirname(__file__), "ui", "smod_logo.png")
        self.supported_media = [CPSMatchType.GENERIC,
                                CPSMatchType.VIDEO,
                                CPSMatchType.MUSIC]

        path = join(dirname(__file__), "res", "smod.jsondb")
        # load video catalog
        self.media_collection = Collection("smod", logo=self.skill_logo,
                                           db_path=path)
        self.settings["min_duration"] = 20 * 60

    def get_intro_message(self):
        self.speak_dialog("intro")

    @intent_file_handler('home.intent')
    def handle_homescreen_utterance(self, message):
        self.handle_homescreen(message)

    def match_media_type(self, phrase, media_type):
        score = 0

        if self.voc_match(phrase,
                          "music") or media_type == CPSMatchType.MUSIC:
            score += 10

        if self.voc_match(phrase, "doom"):
            score += 5

        if self.voc_match(phrase, "stoner"):
            score += 20
            if self.voc_match(phrase, "doom"):
                score += 10

        if self.voc_match(phrase, "smod"):
            score += 50

        return score


def create_skill():
    return SMODSkill()
