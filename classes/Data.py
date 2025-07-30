from collections import Counter

from classes.Excel import Excel

class Data:
    def __init__(self):
        self.excel = Excel()
        self.main = self.excel.get_to_fill()
        self.sub = 0
        self.values = {1: [], 2: [], 3: [], 4: []}

    def set_field(self, value):
        self.values[self.sub].append(value)

    def get_field_length(self):
        return len(self.values[self.sub])

    def get_total_lenght(self):
        return sum(len(inner_list) for inner_list in self.values.values())

    def save(self):
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


