from tkinter import *
from psutil import disk_partitions, disk_usage, virtual_memory, cpu_percent
from tabulate import tabulate

window = Tk()
window.geometry("900x600")
window.title("DISK - ANALYZER")

def show_cpu_info():
    cpu_use = cpu_percent(interval=1)
    cpu_label.config(text='{} %'.format(cpu_use))
    cpu_label.after(200, show_cpu_info)

def conversor_bytes_to_gb(byte):
    one_gigabyte = 1073741824
    return '{0:.1F}'.format(byte / one_gigabyte)

def show_ram_info():
    ram_usage = virtual_memory()
    ram_usage = dict(ram_usage._asdict())
    for key in ram_usage:
        if key != 'percent':
            ram_usage[key] = conversor_bytes_to_gb(ram_usage[key])
    ram_label.config(text='{} GB / {} GB ({}%)'.format(ram_usage["used"], ram_usage["total"], ram_usage["percent"]))
    ram_label.after(200, show_ram_info)

data = disk_partitions(all=False)

def details(device_name):
    for i in data:
        if i.device == device_name:
            return i

def get_device_name():
    return [i.device for i in data]

def disk_info(device_name):
    disk_info = {}
    try:
        usage = disk_usage(device_name)
        disk_info['Device'] = device_name
        disk_info['Total'] = f"{conversor_bytes_to_gb(usage.used + usage.free)} GB"
        disk_info['Used'] = f"{conversor_bytes_to_gb(usage.used)} GB"
        disk_info['Free'] = f"{conversor_bytes_to_gb(usage.free)} GB"
        disk_info['Percent'] = f"{usage.percent} %"
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    info = details(device_name)
    if info:
        disk_info.update({"Device": info.device, "Mount Point": info.mountpoint, "FS-Type": info.fstype})
    return disk_info

def all_disk_info():
    return [disk_info(i) for i in get_device_name()]

title_program = Label(window, text='Disk Analyzer', font="arial 40 bold", fg='#14747F')
title_program.place(x=110, y=20)

cpu_title_label = Label(window, text='CPU usage: ', font="arial 24 bold", fg='#FA5125')
cpu_title_label.place(x=20, y=155)

cpu_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=20)
cpu_label.place(x=230, y=150)

ram_title_label = Label(window, text='RAM Usage: ', font="arial 24 bold", fg='#34A96C')
ram_title_label.place(x=20, y=255)

ram_label = Label(window, bg='#071C1E', fg='#FA5125', font="Arial 30 bold", width=20)
ram_label.place(x=230, y=250)

disk_title_label = Label(window, text='Disk Usage: ', font="arial 24 bold", fg='#797E1E')
disk_title_label.place(x=350, y=360)

textArea = Text(window, bg="#071C1E", fg="yellow", width=85, height=6, padx=10, font=("consolas", 14))
textArea.place(x=15, y=410)

if __name__ == '__main__':
    show_cpu_info()
    show_ram_info()
    info = all_disk_info()
    infoTabulated = tabulate([i.values() for i in info], headers=info[0].keys(), tablefmt="simple", missingval="-")
    textArea.insert(END, infoTabulated)

window.mainloop()
