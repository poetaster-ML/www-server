import multiprocessing

bind = ':8000'
workers = multiprocessing.cpu_count() * 2 + 1
forwarded_allow_ips = '*'
timeout = 320
