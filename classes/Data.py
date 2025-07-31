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
        self.values = {
            1: [None, None, None, None],
            2: [None, None, None, None],
            3: [None, None, None, None],
            4: [None, None, None, None]
        }

    def set_field(self, index, value):
        """
        :author: Ruth Neeßen
        :param value: String, the chosen value from the dropdown
        :param index: Integer, the index of the current dropdown
        Add the dropdown value at one point on the current picture
        """
        self.values[self.sub][index - 1] = value

    def has_all_points(self):
        """
        :author: Ruth Neeßen
        :return: checks if all values for the current picture are not None -> 4 values != None
        """
        return all(value is not None for value in self.values[self.sub])

    def get_total_length(self):
        """
        :author: Ruth Neeßen
        :return: returns the length of all elements that are not None
        """
        total = 0
        for inner_list in self.values.values():
            for value in inner_list:
                if value is not None:
                    total += 1
        return total

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
        self.values = {
            1: [None, None, None, None],
            2: [None, None, None, None],
            3: [None, None, None, None],
            4: [None, None, None, None]
        }


