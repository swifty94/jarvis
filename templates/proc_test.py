def process_monitor():
    import psutil
    names = []
    paths = []
    cpus = []
    mems = []
    print('START \n')
    procs = psutil.pids()
    for i in procs:
        try:
            p = psutil.Process(i)
            name = p.name()
            path = p.exe()
            cpu = p.cpu_percent(interval=0.02)
            mem = round((p.memory_info()[1] / 1024 / 1024), 2)
            if p.is_running() == True:
                if cpu >= 0.1:
                        names.append(name)
                        paths.append(path)
                        cpus.append(cpu)
                        mems.append(mem)
        except psutil.NoSuchProcess as nsp:
            pass
        except psutil.AccessDenied as ad:
            pass
        except Exception as e:
            print(e)

    result = list(zip(names,paths,cpus,mems))
    print('DONE \n')
    result.sort(key=lambda x: x[2], reverse=True)
    return result

print(process_monitor())