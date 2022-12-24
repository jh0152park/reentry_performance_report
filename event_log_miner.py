class Miner:
    def __init__(self):
        self.log = ""
        self.test_scenario_package = []
        self.launch_time = {}
        self.launch_count = {}
        self.average_launch_time = {}

    def set_log(self, log):
        self.log = log

    def set_test_scenario_package(self, packages):
        self.test_scenario_package = list(set(packages))

    def compute_launch_time(self):
        for log in self.log:
            line = log[:-1]

            if "am_app_transition" in line:
                proc = line.split(",")[0].split("[")[-1]
                if proc in self.test_scenario_package:
                    if proc not in self.launch_time.keys():
                        self.launch_time[proc] = []
                        self.launch_count[proc] = 0
                    self.launch_count[proc] += 1
                    self.launch_time[proc].append(int(line.split(",")[-3]))

        for proc in self.launch_time.keys():
            try:
                self.average_launch_time[proc] = \
                    1.00 * sum(self.launch_time[proc][1:]) / (len(self.launch_time[proc]) - 1)
            except BaseException as ex:
                print("\noccurred compute error to get average launch time.")
                print(f"error is {ex}")
                print("please check detail below")
                print(f"{proc} / {self.launch_time[proc]}")
                self.average_launch_time[proc] = \
                    1.00 * sum(self.launch_time[proc]) / (len(self.launch_time[proc]))

            # print(f"{proc} / {self.average_launch_time[proc]}")
        # print(self.launch_time["com.soundcloud.android"])

    def get_average_launch_time(self) -> dict:
        if not self.average_launch_time:
            self.compute_launch_time()
        return self.average_launch_time