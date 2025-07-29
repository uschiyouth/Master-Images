class Data:
    def __init__(self):
        self.main = 0
        self.sub = 0
        self.values = {1: [], 2: [], 3: [], 4: []}

    def set_field(self, value):
        self.values[self.sub].append(value)

    def get_field_length(self):
        return len(self.values[self.sub])

    def get_total_lenght(self):
        return sum(len(inner_list) for inner_list in self.values.values())

    def save(self):
        print("saving data")

