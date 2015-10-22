from ..util.html import get_content
from ..util.match import match1
from ..extractor import VideoExtractor
from ..common import playlist_not_supported

import xml.etree.ElementTree as ET
from urllib.parse import unquote

class Netease(VideoExtractor):
    name = "网易视频 (163)"
    sopported_stream_types = ['shd', 'hd', 'flv']
    stream_2_profile = {'shd':'超清', 'hd':'高清', 'flv':'标清'}

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if not self.vid:
            html = get_content(self.url)
            topiccid = match1(html, 'topicid : \"([^\"]+)')
            vid = match1(html, 'vid : \"([^\"]+)')
            self.vid = (topiccid, vid)
        topiccid, _vid = self.vid
        code = _vid[-2:]
        video_xml = get_content('http://xml.ws.126.net/video/{}/{}/{}_{}.xml'.format(code[0], code[1], topiccid, _vid))
        self.title = unquote(match1(video_xml, '<title>([^<]+)'))

        for tp in self.sopported_stream_types:
            searchcode = '<{}Url><flv>([^<]+)'.format(tp)
            url = match1(video_xml, searchcode)
            if url:
                self.stream_types.append(tp)
                self.streams[tp] = {'container': 'flv', 'video_profile': self.stream_2_profile[tp], 'src' : [url], 'size': 0}

site = Netease()
download = site.download_by_url
download_playlist = playlist_not_supported('163')
