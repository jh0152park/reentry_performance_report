# Re-Entry Performance Test Result Excel file Generator
------------------------------------------------------------
![reentry_performance](https://user-images.githubusercontent.com/118165975/209468948-7276b7e5-13fd-41c8-b657-bb54c078d48b.png)


# Overview
We need some way to check refresh performance and average launch speed every each application more easily with our refresh test script.

We can check very simply by just one sheet on result excel file about below things.

1. Test Application
2. Re-Entry(Refresh) performance every single applications
3. Average Launch speed performance every single applications
4. Status of available memory
5. Status of swap used memory
6. Average memory size of key items
7. Average memory size of every single ADJ(Native, System, Foreground, etc...)
------------------------------------------------------------

# Requirement
1. Full time "proc/meminfo" log information by our refresh test script
2. Full time "dumpsys meminfo" log information by our refresh test script
3. Full time "event" log information by our refresh test script
------------------------------------------------------------

# Result File
One simple excel file, also can support multi test result log files by our refresh test script.
