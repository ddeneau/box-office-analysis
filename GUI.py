from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from MovieScript import MONTHS


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

        for i in range(12):
            months[i] = Button(text=MONTHS.__getitem__(i))
            self.add_widget(months.get(i))

    def start_season(self, instance):
        self.cols = 4
        self.rows = 3
        seasons = dict()
        seasons_names = ("First", "Second", "Third", "Fourth", "Winter", "Spring", "Summer", "Fall")

        self.remove_widget(self.button_seasons)
        self.remove_widget(self.button_months)

        for i in range(8):
            seasons[i] = Button(text=seasons_names.__getitem__(i))
            self.add_widget(seasons.get(i))


class AppM(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Movie Script"
        return StartingPage()


if __name__ == '__main__':
    AppM().run()
