import xlsxwriter
import scenario
import report_format


class Report:
    def __init__(self, title, models):
        self.models = models
        self.workbook = xlsxwriter.Workbook(title)
        self.summary_sheet = self.workbook.add_worksheet("Summary")

        self.test_scenario = []
        self.memory_agenda = [
            "Total Memory",
            "Free Memory",
            "Cached Memory",
            "Available Memory",
            "Mlocked",
            "Rbin Total",
            "Rbin Alloced",
            "Rbin Free",
            "Swap Total",
            "Swap Free",
            "Swap Used",
            "System Heap",
            "System Heap Pool",
            "Graphic Memory"
        ]
        self.memory_agenda_key = {
            "Total Memory": "MemTotal",
            "Free Memory": "MemFree",
            "Cached Memory": "Cached",
            "Available Memory": "NeedCompute",
            "Mlocked": "Mlocked",
            "Rbin Total": "RbinTotal",
            "Rbin Alloced": "RbinAlloced",
            "Rbin Free": "RbinFree",
            "Swap Total": "SwapTotal",
            "Swap Free": "SwapFree",
            "Swap Used": "NeedCompute",
            "System Heap": "SystemHeap",
            "System Heap Pool": "SystemHeapPool",
            "Graphic Memory": "KgslSharedmem"
        }

        self.adj = []
        self.proc_meminfo_sheet = []
        self.dumpsys_meminfo_sheet = []

    def close_report(self):
        self.workbook.close()

    @staticmethod
    def write_string(sheet, x, y, content, form):
        sheet.write_string(y - 1, x - 1, content, form)

    @staticmethod
    def write_number(sheet, x, y, content, form):
        sheet.write_number(y - 1, x - 1, content, form)

    @staticmethod
    def set_column(sheet, x, y, size):
        sheet.set_column(y - 1, x - 1, size)

    @staticmethod
    def set_merge(sheet, from_x, from_y, to_x, to_y, content):
        sheet.merge_range(from_y - 1, from_x - 1, to_y - 1, to_x - 1, content)

    def set_test_scenario(self):
        for model in self.models:
            self.test_scenario += model.get_test_scenario()
        self.test_scenario = list(set(self.test_scenario))

    def set_adj_list(self):
        self.adj = self.models[0].get_adj_list()
        for model in self.models[1:]:
            for adj in model.get_adj_list():
                if adj not in self.adj:
                    self.adj.append(adj)

    def write_sub_title(self):
        self.set_column(self.summary_sheet, 1, 1, 40)
        self.set_column(self.summary_sheet, 2, 2, 15)
        self.write_string(self.summary_sheet, 1, 2, "Package", None)
        self.write_string(self.summary_sheet, 2, 2, "Application", None)

        for i in range(len(self.models)):
            self.set_column(self.summary_sheet, 3 + (i * 2), 3 + (i * 2), 15)
            self.set_column(self.summary_sheet, 4 + (i * 2), 4 + (i * 2), 15)

            self.set_merge(self.summary_sheet, 3 + (i * 2), 1, 4 + (i * 2), 1, self.models[i].id)
            self.write_string(self.summary_sheet, 3 + (i * 2), 2, "Re-Entry(개)", None)
            self.write_string(self.summary_sheet, 4 + (i * 2), 2, "AVG Speed(ms)", None)

    def write_test_scenario(self):
        if not self.test_scenario:
            self.set_test_scenario()

        y = 0
        for app in self.test_scenario:
            package = scenario.PACKAGE[app]
            self.write_string(self.summary_sheet, 1, 3 + y, package, None)
            self.write_string(self.summary_sheet, 2, 3 + y, app, None)
            y += 1

    def write_re_entry_performance(self):
        if not self.test_scenario:
            self.set_test_scenario()

        y = 0
        for app in self.test_scenario:
            for i in range(len(self.models)):
                proc = scenario.PACKAGE[app]
                re_entry_performance = self.models[i].get_re_entry_performance()
                re_entry = 0.0 if proc not in re_entry_performance.keys() else re_entry_performance[proc]
                self.write_number(self.summary_sheet, 3 + (i * 2), 3 + y, re_entry, None)
            y += 1

    def write_average_launch_time(self):
        if not self.test_scenario:
            self.set_test_scenario()

        y = 0
        for app in self.test_scenario:
            for i in range(len(self.models)):
                proc = scenario.PACKAGE[app]
                average_launch_time = self.models[i].get_average_launch_time()
                launch_time = 0.0 if proc not in average_launch_time.keys() else average_launch_time[proc]
                self.write_number(self.summary_sheet, 4 + (i * 2), 3 + y, launch_time, None)
            y += 1

    def write_simple_memory_agenda(self):
        if not self.test_scenario:
            self.set_test_scenario()

        y = 5 + len(self.test_scenario)
        self.write_string(self.summary_sheet, 1, y - 1, "AVG Memory Info", None)
        for category in self.memory_agenda:
            self.write_string(self.summary_sheet, 1, y, category, None)
            y += 1

    def write_simple_avg_memory_info(self):
        x = 2
        for model in self.models:
            y = 4 + len(self.test_scenario)
            self.write_string(self.summary_sheet, x, y, model.id, None)

            for category in self.memory_agenda:
                y += 1
                average_mem = None if self.memory_agenda_key[category] == "NeedCompute" \
                    else model.get_average_by_category(self.memory_agenda_key[category])

                if average_mem is None:
                    if category == "Available Memory":
                        average_mem = model.get_average_by_category(self.memory_agenda_key["Free Memory"]) + \
                                        model.get_average_by_category(self.memory_agenda_key["Cached Memory"])
                    elif category == "Swap Used":
                        average_mem = model.get_average_by_category(self.memory_agenda_key["Swap Total"]) - \
                                        model.get_average_by_category(self.memory_agenda_key["Swap Free"])
                self.write_number(self.summary_sheet, x, y, average_mem, None)
            x += 1

    def write_simple_memory_info(self):
        self.write_simple_memory_agenda()
        self.write_simple_avg_memory_info()

    def write_simple_adj_list(self):
        if not self.adj:
            self.set_adj_list()
        if not self.test_scenario:
            self.set_test_scenario()

        y = 7 + len(self.test_scenario) + len(self.memory_agenda)
        self.write_string(self.summary_sheet, 1, y - 1, "AVG PSS Info", None)
        for adj in self.adj:
            self.write_string(self.summary_sheet, 1, y, adj, None)
            y += 1

    def write_simple_pss_memory_info(self):
        x = 2
        for model in self.models:
            y = 6 + len(self.test_scenario) + len(self.memory_agenda)
            self.write_string(self.summary_sheet, x, y, model.id, None)

            for adj in self.adj:
                y += 1
                pss = model.get_average_pss_by_adj(adj)
                self.write_number(self.summary_sheet, x, y, pss, None)
            x += 1

    def write_simple_adj_memory_info(self):
        self.write_simple_adj_list()
        self.write_simple_pss_memory_info()

    def draw_re_entry_performance_graph(self):
        graph = self.workbook.add_chart({"type": "line"})
        for i in range(len(self.models)):
            graph.add_series({
                "marker": {"type": "diamond"},
                "name": ["Summary", 0, 2 + (i * 2)],
                "categories": ["Summary", 2, 1, 1 + len(self.test_scenario), 1],
                "values": ["Summary", 2, 2 + (i * 2), 1 + len(self.test_scenario), 2 + (i * 2)]
            })
        graph.set_style(10)
        graph.set_legend({"position": "top"})
        graph.set_title({"name": "Re-Entry Performance"})
        graph.set_x_axis({"name": "Scenario", "name_font": {"size": 15, "bold": True}})
        graph.set_y_axis({"name": "Performance", "name_font": {"size": 10, "bold": True}})
        # graph.set_size({"width": 715, "height": 456})
        # self.summary_sheet.insert_chart(1, 7, graph)
        self.summary_sheet.insert_chart(1, 7, graph, {"x_scale": 1.467, "y_scale": 1.25})

    def write_summary_sheet(self):
        self.write_sub_title()
        self.write_test_scenario()

        self.write_re_entry_performance()
        self.write_average_launch_time()

        self.write_simple_memory_info()
        self.write_simple_adj_memory_info()

        # have to write down draw graph function
        self.draw_re_entry_performance_graph()

    def create_proc_meminfo_sheet(self):
        for model in self.models:
            self.proc_meminfo_sheet.append(
                self.workbook.add_worksheet(model.id + "_proc_meminfo"))

    def compute_proc_meminfo_categories(self) -> list:
        categories = self.models[0].get_proc_meminfo_categories_sequence()
        for model in self.models[1:]:
            for category in model.get_proc_meminfo_categories_sequence():
                if category not in categories:
                    categories.append(category)
        return categories

    def write_proc_meminfo_categories(self):
        if not self.proc_meminfo_sheet:
            self.create_proc_meminfo_sheet()

        categories = self.compute_proc_meminfo_categories()
        for sheet in self.proc_meminfo_sheet:
            x = 2
            for category in categories:
                self.set_column(sheet, x, x, 15)
                self.write_string(sheet, x, 1, category, None)
                x += 1

    def write_test_sequence(self):
        if not self.proc_meminfo_sheet:
            self.create_proc_meminfo_sheet()

        for i in range(len(self.models)):
            model = self.models[i]
            sheet = self.proc_meminfo_sheet[i]
            self.set_column(sheet, 1, 1, 25)
            y = 2
            for app in model.get_test_scenario():
                self.write_string(sheet, 1, y, app, None)
                y += 1

    def write_proc_meminfo_detail(self):
        if not self.proc_meminfo_sheet:
            self.create_proc_meminfo_sheet()

        categories = self.compute_proc_meminfo_categories()
        for i in range(len(self.models)):
            model = self.models[i]
            sheet = self.proc_meminfo_sheet[i]
            proc_meminfo = model.get_proc_meminfo_info()

            for x in range(len(categories)):
                category = categories[x]
                memories = [0 for i in range(len(model.get_test_scenario()))] \
                    if category not in proc_meminfo.keys() else proc_meminfo[category]
                sheet.write_column(1, 1 + x, memories)

    def write_proc_meminfo_sheet(self):
        self.create_proc_meminfo_sheet()

        self.write_test_sequence()
        self.write_proc_meminfo_categories()
        self.write_proc_meminfo_detail()

    def create_dumpsys_meminfo_sheet(self):
        for model in self.models:
            self.dumpsys_meminfo_sheet.append(
                self.workbook.add_worksheet(model.id + "_dumpsys_meminfo"))

    def write_test_sequence_on_dumpsys(self):
        if not self.dumpsys_meminfo_sheet:
            self.create_dumpsys_meminfo_sheet()

        for i in range(len(self.models)):
            model = self.models[i]
            sheet = self.dumpsys_meminfo_sheet[i]
            self.set_column(sheet, 1, 1, 25)
            y = 2
            for app in model.get_test_scenario():
                self.write_string(sheet, 1, y, app, None)
                y += 1

    def write_dumpsys_meminfo_adj(self):
        if not self.dumpsys_meminfo_sheet:
            self.create_dumpsys_meminfo_sheet()
        if not self.adj:
            self.set_adj_list()

        for sheet in self.dumpsys_meminfo_sheet:
            x = 2
            for adj in self.adj:
                self.set_column(sheet, x, x, 15)
                self.write_string(sheet, x, 1, adj, None)
                x += 1

    def write_dumpsys_meminfo_detail(self, model=None):
        if not self.dumpsys_meminfo_sheet:
            self.create_dumpsys_meminfo_sheet()

        for i in range(len(self.models)):
            model = self.models[i]
            sheet = self.dumpsys_meminfo_sheet[i]
            pss_info = model.get_pss_by_adj()

            for x in range(len(self.adj)):
                adj = self.adj[x]
                memories = [0 for i in range(len(model.get_test_scenario()))] \
                    if adj not in pss_info.keys() else pss_info[adj]
                sheet.write_column(1, 1 + x, memories)

    def write_dumpsys_meminfo_sheet(self):
        self.create_dumpsys_meminfo_sheet()

        self.write_test_sequence_on_dumpsys()
        self.write_dumpsys_meminfo_adj()
        self.write_dumpsys_meminfo_detail()
