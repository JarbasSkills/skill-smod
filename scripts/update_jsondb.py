from youtube_archivist import YoutubeMonitor
import shutil
import json
from os.path import dirname, isfile

archive = YoutubeMonitor("smod",
                         blacklisted_kwords=["subscribe"])

# load previous cache
cache_file = f"{dirname(dirname(__file__))}/bootstrap.json"
if isfile(cache_file):
    try:
        with open(cache_file) as f:
            data = json.load(f)
            archive.db.update(data)
            archive.db.store()
    except:
        pass  # corrupted for some reason

    shutil.rmtree(cache_file, ignore_errors=True)

urls = [
    "https://www.youtube.com/c/666MrDoom/videos",
    "https://www.youtube.com/c/StonedMeadowOfDoom2/videos",
    "https://www.youtube.com/c/StonedMeadowOfDoom1993/videos",
    "https://www.youtube.com/channel/UCWf14ZX2SZV4hF-hDVKdGvQ/videos"]
for url in urls:
    # parse new vids
    archive.parse_videos(url)

# save bootstrap cache
shutil.copy(archive.db.path, cache_file)
