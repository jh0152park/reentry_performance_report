import scenario


class Miner:
    def __init__(self):
        self.log = ""
        self.cycle = 5
        self.test_scenario_package = []
        self.launch_count = {}
        self.re_entry_count = {}
        self.re_entry_performance = {}
        self.adj = []
        self.pss_by_adj = {}

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
            self.re_entry_performance[proc] = 1.00 * sum(self.re_entry_count[proc]) / len(self.re_entry_count[proc])
            # print(f"{proc} / {self.re_entry_performance[proc]}")

    def compute_all_adj(self):
        is_pss = False

        for log in self.log:
            line = log[:-1]

            if "Total PSS by OOM adjustment:" in line:
                is_pss = True
            elif "Total PSS by category:" in line:
                is_pss = False

            if is_pss:
                if "K: " in line and "(pid" not in line:
                    adj = line.split("K: ")[-1]
                    # print(f"raw data is {line}\nand adj is {adj}")
                    if adj not in self.adj:
                        self.adj.append(adj)
                        self.pss_by_adj[adj] = []

    def fill_in_pss_by_scenario(self):
        for adj in self.pss_by_adj.keys():
            self.pss_by_adj[adj].append(0)

    def compute_pss_size_by_adj(self):
        is_pss = False
        self.compute_all_adj()

        for log in self.log:
            line = log[:-1]

            if "Total PSS by OOM adjustment:" in line:
                is_pss = True
                self.fill_in_pss_by_scenario()
            elif "Total PSS by category:" in line:
                is_pss = False

            if is_pss:
                if "K: " in line and "(pid" not in line:
                    pss = int(line.split("K:")[0].strip().replace(",", ""))
                    adj = line.split("K: ")[-1]
                    self.pss_by_adj[adj][-1] = pss

        # for adj in self.pss_by_adj.keys():
        #     print(f"adj is {adj} and len is {len(self.pss_by_adj[adj])}")

    def get_average_pss_by_adj(self, adj: str) -> float:
        # self.compute_pss_size_by_adj()
        if adj not in self.pss_by_adj.keys():
            return 0.00
        return 1.00 * sum(self.pss_by_adj[adj]) / (len(self.pss_by_adj[adj]) - self.pss_by_adj[adj].count(0))

    def get_adj_list(self) -> list:
        return self.adj

    def get_pss_by_adj(self) -> dict:
        return self.pss_by_adj

    def get_re_entry_performance(self) -> dict:
        if not self.re_entry_performance:
            self.compute_re_entry_count()
        return self.re_entry_performance
