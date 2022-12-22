import os
import model

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


models[0].compute_proc_meminfo_log()
models[0].compute_test_scenario()
models[0].compute_launch_speed()
models[0].compute_re_entry_count()
models[0].compute_re_entry_performance()
