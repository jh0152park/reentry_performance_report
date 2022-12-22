import scenario


class Miner:
    def __init__(self):
        self.log = ""
        self.cycle = 5
        self.test_scenario_package = []
        self.launch_count = {}
        self.re_entry_count = {}
        self.re_entry_performance = {}

    def set_log(self, log):
        self.log = log

    def set_test_scenario_package(self, packages):
        self.test_scenario_package = list(set(packages))

    def compute_re_entry_count(self):
        if len(self.test_scenario_package) == 0:
            print("can not compute re entry count every each apps due to scenario list is empty.")
            exit(0)

        for i in range(len(self.log)):
            line = self.log[i][:-1]

            if "run this app" in line:
                app = line.split(":")[-1].strip()
                if scenario.PACKAGE[app] not in self.launch_count.keys():
                    self.launch_count[scenario.PACKAGE[app]] = 0
                    self.re_entry_count[scenario.PACKAGE[app]] = [0, 0, 0, 0]
                self.launch_count[scenario.PACKAGE[app]] += 1

            if "Total PSS by process:" in line:
                for j in range(i, len(self.log)):
                    line = self.log[j][:-1]
                    if "Total PSS by OOM adjustment:" in line:
                        i += j
                        break

                    if "(pid " in line and "activities)" in line:
                        proc = line.split()[1]
                        if proc in self.test_scenario_package and self.launch_count[proc] < self.cycle:
                            self.re_entry_count[proc][self.launch_count[proc] - 1] += 1

    def compute_re_entry_performance(self):
        if len(self.re_entry_count.keys()) < 1:
            print("can not compute re entry performance due to re entry count is empty")
            exit(0)
        for proc in self.re_entry_count.keys():
            self.re_entry_performance[proc] = round(float(
                sum(self.re_entry_count[proc]) / len(self.re_entry_count[proc])), 2)
            print(f"{proc} / {self.re_entry_performance[proc]}")