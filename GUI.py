from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from MovieScript import MONTHS, switch_quarter, MovieScript


class StartingPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_out = Label(text='Data')
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

        seasons.get(1).bind(on_press=lambda x: self.start_script(True, 1))
        seasons.get(2).bind(on_press=lambda x: self.start_script(True, 2))
        seasons.get(3).bind(on_press=lambda x: self.start_script(True, 3))
        seasons.get(4).bind(on_press=lambda x: self.start_script(True, 4))
        seasons.get(5).bind(on_press=lambda x: self.start_script(True, 5))
        seasons.get(6).bind(on_press=lambda x: self.start_script(True, 6))
        seasons.get(7).bind(on_press=lambda x: self.start_script(True, 7))
        seasons.get(8).bind(on_press=lambda x: self.start_script(True, 8))

    def start_script(self, time_type, selector):
        if time_type:
            season = switch_quarter(selector)
            script = MovieScript(season)
            script.populate_lists_from_url(season)
            script.print_report_by_season(season)
            self.data_out.text = script.report.keys()
        else:
            script = MovieScript(switch_quarter(1))
            script.find_data_by_month(selector)
            script.print_report_by_month(selector)
            self.data_out.text = script.report.keys()

        self.add_widget(self.data_out)


class AppM(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Movie Script"
        return StartingPage()


if __name__ == '__main__':
    AppM().run()
