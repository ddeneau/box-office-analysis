#  Manages CSV file with box office data.
import csv
import datetime
import time
from MovieScript import MovieScript, switch_month


# Run once a day to populate moviedata.csv
class Saver:

    def __init__(self):
        self.file = 'moviedata.csv'
        self.script = None
        self.time_stamp = ""

    def main(self):
        current_date = datetime.datetime.today()
        self.time_stamp = str(current_date).split().__getitem__(0)
        self.script = MovieScript(switch_month(current_date.month), True)
        self.script.find_data_from_month(current_date.month)

        while True:
            self.write_to_init('a')
            time.sleep(60 * 60 * 24)

    def write_to_init(self, mode):
        key_set = list(self.script.report.keys())

        with open(self.file, mode, newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([self.time_stamp] + [key_set.__getitem__(0)] +
                            [self.script.report.get(key_set.__getitem__(0))])


if __name__ == '__main__':
    Saver().main()
