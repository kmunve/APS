import branca.element as be
# currently using the static info page ava_info_static.html

class SatSkredInfoPage():

    def __init__(self):
        self.f = be.Figure()

    def make_header(self):
        pass

    def add_map(self, map_name="./ava_map.html", h="600px"):
        self.f.html.add_child(be.Element("<H2>Kart over detekterte skred</H2>"))
        # self.f.html.add_child(be.Element('''<iframe src="./ava_map.html:text/html;charset=utf-8;base64,CiAgICAuL2F2YtYXAuaHRtbA==" width="100%" style="border:none !important;" height="600px"></iframe>''')
        self.f.html.add_child(be.Element('<iframe src="./ava_map.html", height="600px"></iframe>')
        # self.f.html.add_child(be.IFrame(map_name, height=h))


    def save(self, filename="ava_info.html"):
        self.f.render()
        self.f.save(filename)


if __name__ == "__main__":
    page = SatSkredInfoPage()
    page.add_map()
    page.save()