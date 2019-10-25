"""
MP1 Common Shared Library
Contains shared input and output processing functions
"""
from terminaltables import SingleTable

"""
Common process object
"""
class ProcessLine:
    def __init__(self, burst_time, arrival_time, priority_number, p_num):
        self.burst_time = int(burst_time)
        self.arrival_time = int(arrival_time)
        self.priority_number = int(priority_number)
        self.completion_time = -1
        self.response_time = -1
        self.waiting_time = -1
        self.turnaround_time = -1
        self.id = p_num
        self.burst_original = int(burst_time)

"""
Input filter when reading from files
"""
def filter_numbers(inp):
    out = ""
    for x in inp:
        if ord(x) >= 48 and ord(x) <= 57:
            out = out + x
    return out

"""
Data input
Load data from file and return processlist
"""
def load_from_file(file_name):
    process_list = []
    yh = open(file_name) #百合みたい（笑）。妄想すぎだろう
    pn = 1
    for line in yh:
        vals = line.split(",")
        if len(vals) != 3:
            continue
        new_p = ProcessLine(filter_numbers(vals[0]), filter_numbers(vals[1]), filter_numbers(vals[2]), pn)
        process_list.append(new_p)
        pn = pn + 1
    yh.close()
    return process_list

"""
Print input data as table
"""
def print_input_table(process_list):
    yh = open('input_all.txt') #百合みたい（笑）。妄想すぎだろう
    pn = 1
    input_table = [
        ['Process', 'Burst Time', 'Arrival Time', 'Priority']
    ]
    for p in process_list:
        input_table.append(["P"+str(p.id),p.burst_time,p.arrival_time,p.priority_number])
    
    in_table = SingleTable(input_table)
    in_table.title = "Input Data: "
    print(in_table.table)

"""
Print RAW and AVERAGE values of simulation result
"""
def print_simulation_report(fin, history_list):
    print("Simulation Report: ")
    value_table_data = [
        ['Process', 'Burst\nTime', 'Arrival\nTime', 'Completion\nTime', 'Response\nTime', 'Waiting\nTime', 'Turnaround\nTime']
    ]
    response_time_ave = 0
    waiting_time_ave = 0
    turnaround_time_ave = 0
    counter = 0
    for x in fin:
        value_table_data.append([x.id, x.burst_original, x.arrival_time, x.completion_time, x.response_time, x.waiting_time, x.turnaround_time])
        response_time_ave += x.response_time
        waiting_time_ave += x.waiting_time
        turnaround_time_ave += x.turnaround_time
        counter += 1
    #Formulate averages for RESPONSE, WAITING, TURNAROUND
    response_time_ave = response_time_ave / counter
    waiting_time_ave = waiting_time_ave / counter
    turnaround_time_ave = turnaround_time_ave / counter
    average_table_data = [
        ['計算要素', '結果数字'],
        ['Response Time Average', response_time_ave],
        ['Waiting Time Average', waiting_time_ave],
        ['Turnaround Time Average', turnaround_time_ave]
    ]
    
    #Simulation value output
    value_table = SingleTable(value_table_data)
    value_table.title = "Scheduling Algorithm Result"
    print(value_table.table)

    #Average table output
    average_table = SingleTable(average_table_data)
    average_table.title = "Average Values"
    print(average_table.table)

    #GANTT CHART
    gantt = [[],[]]
    print("Process History: ")
    prev = None
    prev_time = None
    history_list.append(("*","*"))
    for p in history_list:
        if prev == None:
            prev = p[0]
            prev_time = p[1]
            gantt[0].append("|")
            gantt[1].append(p[1]-1)
        elif prev != p[0]:
            gantt[0].append(prev)
            gantt[0].append("|")
            gantt[1].append("")
            gantt[1].append(prev_time)
            prev = p[0]
            prev_time = p[1]
        elif prev == p[0]:
            prev_time = p[1]
    table = SingleTable(gantt)
    print(table.table)