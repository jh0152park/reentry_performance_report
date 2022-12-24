import os
import model
import report_generator as rp

models = []
log_files = [file for file in os.listdir(os.getcwd()) if file.endswith(".txt")]

for file in log_files:
    if "full_time_logcat" in file:
        models.append(model.Model(file.split("_")[0]))

for file in log_files:
    id = file.split("_")[0]
    read = open(file, "r").readlines()
    for model in models:
        if model.id == id:
            if "full_time_logcat" in file:
                model.set_logcat_log(read)
            elif "full_time_eventlog" in file:
                model.set_event_log(read)
            elif "proc_meminfo" in file:
                model.set_proc_meminfo_log(read)
            elif "dumpsys_meminfo" in file:
                model.set_dumpsys_meminfo_log(read)

for model in models:
    model.compute_proc_meminfo_log()
    model.compute_test_scenario()
    model.compute_launch_time()
    model.compute_re_entry_count()
    model.compute_re_entry_performance()
    model.compute_pss_size_by_adj()

report = rp.Report("reentry_performance_report.xlsx", models)

report.write_summary_sheet()
report.write_proc_meminfo_sheet()
report.write_dumpsys_meminfo_sheet()

report.close_report()
