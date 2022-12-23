class Miner:
    def __init__(self):
        self.log = ""
        self.categories = {}
        self.scenario = []

    def set_log(self, log):
        self.log = log

    def read_all_categories(self):
        for log in self.log:
            line = log[:-1]

            if " kB" in line:
                category = line.split()[0][:-1]
                if category not in self.categories.keys():
                    self.categories[category] = []
                self.categories[category].append(int(line.split()[-2]))

    def get_average_by_category(self, category):
        if category not in self.categories.keys():
            return 0
        return sum(self.categories[category]) / len(self.categories[category])

    def get_proc_meminfo_info(self) -> dict:
        return self.categories

    def read_test_scenario(self):
        for log in self.log:
            line = log[:-1]
            if "run this app" in line:
                self.scenario.append(line.split(":")[-1].strip())

    def get_test_scenario(self) -> list:
        return self.scenario