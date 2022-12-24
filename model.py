import scenario
import event_log_miner
import proc_meminfo_miner
import dumpsys_meminfo_miner


class Model:
    def __init__(self, id):
        self.id = id

        self.event_log = ""
        self.logcat_log = ""
        self.proc_meminfo_log = ""
        self.dumpsys_meminfo_log = ""

        self.event_log_miner = event_log_miner.Miner()
        self.proc_meminfo_miner = proc_meminfo_miner.Miner()
        self.dumpsys_meminfo_minder = dumpsys_meminfo_miner.Miner()

        self.proc_meminfo_info = {}
        self.test_scenario = []
        self.test_scenario_package = []

    def set_event_log(self, log):
        self.event_log = log
        self.event_log_miner.set_log(self.event_log)

    def set_logcat_log(self, log):
        self.logcat_log = log

    def set_proc_meminfo_log(self, log):
        self.proc_meminfo_log = log
        self.proc_meminfo_miner.set_log(self.proc_meminfo_log)

    def set_dumpsys_meminfo_log(self, log):
        self.dumpsys_meminfo_log = log
        self.dumpsys_meminfo_minder.set_log(self.dumpsys_meminfo_log)

    def get_event_log(self):
        return self.event_log

    def get_logcat_log(self):
        return self.logcat_log

    def get_proc_meminfo_log(self):
        return self.proc_meminfo_log

    def get_dumpsys_meminfo_log(self):
        return self.dumpsys_meminfo_log

    def compute_proc_meminfo_log(self):
        self.proc_meminfo_miner.read_all_categories()
        self.proc_meminfo_info = self.proc_meminfo_miner.get_proc_meminfo_info()

    def compute_test_scenario(self):
        self.proc_meminfo_miner.read_test_scenario()
        self.test_scenario = self.proc_meminfo_miner.get_test_scenario()

        for app in self.test_scenario:
            self.test_scenario_package.append(scenario.PACKAGE[app])
        self.event_log_miner.set_test_scenario_package(self.test_scenario_package)
        self.dumpsys_meminfo_minder.set_test_scenario_package(self.test_scenario_package)

    def compute_launch_time(self):
        self.event_log_miner.compute_launch_time()

    def compute_re_entry_count(self):
        self.dumpsys_meminfo_minder.compute_re_entry_count()

    def compute_re_entry_performance(self):
        self.dumpsys_meminfo_minder.compute_re_entry_performance()

    def compute_pss_size_by_adj(self):
        self.dumpsys_meminfo_minder.compute_pss_size_by_adj()
        # print(self.dumpsys_meminfo_minder.get_average_pss("Native"))
        # print(self.dumpsys_meminfo_minder.get_average_pss("Cached"))

    def get_test_scenario(self) -> list:
        return self.test_scenario

    def get_re_entry_performance(self) -> dict:
        return self.dumpsys_meminfo_minder.get_re_entry_performance()

    def get_adj_list(self) -> list:
        return self.dumpsys_meminfo_minder.get_adj_list()

    def get_average_launch_time(self) -> dict:
        return self.event_log_miner.get_average_launch_time()

    def get_average_by_category(self, category) -> float:
        # print(f"return value is {self.proc_meminfo_miner.get_average_by_category(category)}")
        return self.proc_meminfo_miner.get_average_by_category(category)

    def get_average_pss_by_adj(self, adj):
        return self.dumpsys_meminfo_minder.get_average_pss_by_adj(adj)

    def get_proc_meminfo_categories_sequence(self) -> list:
        return self.proc_meminfo_miner.get_proc_meminfo_categories_sequence()