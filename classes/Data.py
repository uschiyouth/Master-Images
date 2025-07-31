from collections import Counter

from classes.Excel import Excel

class Data:
    def __init__(self):
        """
        :author: Ruth Neeßen
        instantiate Excel object
        main = plot number
        sub = number of the picture, taken at this plot
        """
        self.excel = Excel()
        self.main = self.excel.get_to_fill()
        self.sub = 0
        self.values = {1: [], 2: [], 3: [], 4: []}

    def set_field(self, value):
        """
        :author: Ruth Neeßen
        Add the dropdown value at one point on the current picture
        :param value:
        """
        self.values[self.sub].append(value)

    def get_field_length(self):
        """
        :author: Ruth Neeßen
        :return: the field length for the current picture -> 4 means: all 4 pictures from the plot are analysed
        """
        return len(self.values[self.sub])

    def get_total_lenght(self):
        return sum(len(inner_list) for inner_list in self.values.values())

    def save(self):
        """
        :author: Ruth Neeßen
        Calculates the percentage of each type of soil cover and saves it in the excel file
        Sets the counting of images taken at a plot back to 1, deletes all the values stored in self.values
        """
        all_values = []
        for index, vals in self.values.items():
            all_values.extend(vals)

        counter = Counter(all_values)
        total = len(all_values)
        percentages = {k: v / total * 100 for k, v in counter.items()}
        self.excel.save_row(self.main, percentages)
        self.sub = 1
        self.main = self.main + 1
        self.values = {1: [], 2: [], 3: [], 4: []}


