from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from MovieScript import MONTHS, switch_quarter, switch_month, MovieScript


class StartingPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.rows = 2

        self.button_months = Button(text="Monthly Reports")
        self.add_widget(self.button_months)
        self.button_months.bind(on_press=self.start_month)

        self.button_seasons = Button(text="Seasonal or Quarterly Reports")
        self.add_widget(self.button_seasons)
        self.button_seasons.bind(on_press=self.start_season)

    def start_month(self, instance):
        self.cols = 6
        self.rows = 3
        months = dict()

        self.remove_widget(self.button_seasons)
        self.remove_widget(self.button_months)

        for i in range(1, 13):
            months[i] = Button(text=MONTHS.__getitem__(i - 1))
            self.add_widget(months.get(i))

        self.add_month_buttons(months)

    def start_season(self, instance):
        self.cols = 4
        self.rows = 3
        seasons = dict()
        seasons_names = ("First", "Second", "Third", "Fourth", "Winter", "Spring", "Summer", "Fall")

        self.remove_widget(self.button_seasons)
        self.remove_widget(self.button_months)

        for i in range(1, 9):
            seasons[i] = Button(text=seasons_names.__getitem__(i - 1))
            self.add_widget(seasons.get(i))

        self.add_season_buttons(seasons)

    def add_month_buttons(self, months):
        months.get(1).bind(on_press=lambda x: self.start_script(False, 1))
        months.get(2).bind(on_press=lambda x: self.start_script(False, 2))
        months.get(3).bind(on_press=lambda x: self.start_script(False, 3))
        months.get(4).bind(on_press=lambda x: self.start_script(False, 4))
        months.get(5).bind(on_press=lambda x: self.start_script(False, 5))
        months.get(6).bind(on_press=lambda x: self.start_script(False, 6))
        months.get(7).bind(on_press=lambda x: self.start_script(False, 7))
        months.get(8).bind(on_press=lambda x: self.start_script(False, 8))
        months.get(9).bind(on_press=lambda x: self.start_script(False, 9))
        months.get(10).bind(on_press=lambda x: self.start_script(False, 10))
        months.get(11).bind(on_press=lambda x: self.start_script(False, 11))
        months.get(12).bind(on_press=lambda x: self.start_script(False, 12))

    def add_season_buttons(self, seasons):
        seasons.get(1).bind(on_press=lambda x: self.start_script(True, 1))
        seasons.get(2).bind(on_press=lambda x: self.start_script(True, 2))
        seasons.get(3).bind(on_press=lambda x: self.start_script(True, 3))
        seasons.get(4).bind(on_press=lambda x: self.start_script(True, 4))
        seasons.get(5).bind(on_press=lambda x: self.start_script(True, 5))
        seasons.get(6).bind(on_press=lambda x: self.start_script(True, 6))
        seasons.get(7).bind(on_press=lambda x: self.start_script(True, 7))
        seasons.get(8).bind(on_press=lambda x: self.start_script(True, 8))

    def start_script(self, time_type, selector):
        data_out = ScrollableLabel()
        back_button = Button(text='Return')
        graph_button = Button(text='Graph')
        back_button.bind(on_press=lambda x: self.go_back())

        self.clear_widgets()

        if time_type:
            season = switch_quarter(selector)
            script = MovieScript(season, True)
            script.find_data_by_season(season, True)
            data_out.text = StartingPage.parse_report(script.report)
            data_out.size_hint_min = (1000, 900)
            graph_button.bind(on_press=lambda x: self.graph(script, switch_quarter(selector), False))
        else:
            script = MovieScript(switch_quarter(1), True)
            script.find_data_from_month(selector)
            data_out.text = StartingPage.parse_report(script.report)
            data_out.size_hint_min = (900, 900)
            graph_button.bind(on_press=lambda x: self.graph(script, switch_month(selector), True))

        data_out.do_scroll_x = False
        data_out.center_x
        graph_button.bind(on_press=lambda x: self.graph(script, selector, False))
        self.add_widget(data_out)
        self.add_widget(back_button)
        self.add_widget(graph_button)

    def go_back(self):
        self.clear_widgets()
        self.__init__()

    @staticmethod
    def graph(script, number, flag):
        if flag:
            script.graphics.graph_data(script.report, switch_month(number), flag)
        else:
            script.graphics.graph_data(script.report, switch_quarter(number), flag)

    @staticmethod
    def parse_report(report):
        parsed = ""

        for item in report.keys():
            parsed += item + " --- --- --- " + report.get(item) + "\n \n"

        return parsed


Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
''')


class ScrollableLabel(ScrollView):
    text = StringProperty('')


class AppM(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Box Office Reports"
        return StartingPage()


if __name__ == '__main__':
    AppM().run()
