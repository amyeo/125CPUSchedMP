"""
CMSC 125 MP1
Round robin CPU scheduler simulator
Follows new timing pattern

Input from file.
"""
import threading
from MP1 import ProcessLine, load_from_file, print_input_table, print_simulation_report
from terminaltables import SingleTable

def simulator(PLPending_list, quantum_time=4):
    finished_list = []
    current_task = None
    pending = PLPending_list
    time = 0
    set_time_quantum = quantum_time 
    time_quantum = set_time_quantum
    time_left = -1
    history = []
    while len(pending) > 0 or current_task != None:
        ### Report Stats
        if current_task:
            history.append(("P"+str(current_task.id),time))

        ### Tick Timer
        time_quantum = time_quantum - 1

        ### Unload Job
        if current_task: #task currently loaded
            if time_quantum <= 0 or time_left <= 0:
                #Time to remove from the queue!
                if time_left <= 0:
                    #write final codes
                    current_task.completion_time = time
                    current_task.turnaround_time = time
                    finished_list.append(current_task)
                else:
                    #current_task.burst_time = current_task.burst_time
                    pending.append(current_task)
                current_task = None

        ### Load Job
        if not current_task: #NO task currently loaded. Find one.
            for p in pending: #handle start
                if p.arrival_time <= time and current_task == None:
                    current_task = p
                    current_task.response_time = time
                    current_task.waiting_time = time
                    pending.remove(p)
                    time_left = current_task.burst_time
                    break

        ### Tick Current Job
        if current_task: #task currently loaded
            time_left = time_left - 1
            current_task.burst_time = current_task.burst_time - 1

        if time_quantum <= 0: #reset.
            time_quantum = set_time_quantum
        time = time + 1
    return (finished_list, history)

def simulator(PLPending_list, quantum_time=4):
    finished_list = []
    current_task = None
    pending = PLPending_list
    time = 0
    time_quantum = quantum_time #reset
    history = []
    while len(pending) > 0 or current_task != None:
        ### Report Stats
        if current_task:
            history.append(("P"+str(current_task.id),time))

        ### Tick Timer

        ### Unload Job
        if current_task != None: #task currently loaded
            #卒業事情確認優先
            if current_task.burst_time <=0: #卒業状況あった
                #UNLOAD and graduate
                current_task.completion_time = time
                current_task.turnaround_time = time
                finished_list.append(current_task)
                current_task = None
            elif time_quantum <=0:
                #hibernate process
                pending.append(current_task)
                current_task = None
                #time_quantum = quantum_time #reset


        ### Load Job
        #FCFS MODE
        if current_task == None: #NO task currently loaded. Find one.
            #no current task executing! Start selection.
            #find minimum
            pending_minimum_arr = []
            for x in pending:
                if x.arrival_time <= time: #confine to present processes
                    pending_minimum_arr.append(x.arrival_time)
            if len(pending_minimum_arr) > 0:
                pending_minimum = min(pending_minimum_arr)
                for p in pending: #handle start
                    #choose shortest and load.
                    if p.arrival_time == pending_minimum and current_task == None and p.arrival_time <= time:
                        current_task = p
                        current_task.response_time = time
                        current_task.waiting_time = time
                        pending.remove(p)
                        time_quantum = quantum_time #reset
                        break

        ### Tick Current Job
        if current_task: #task currently loaded
            current_task.burst_time = current_task.burst_time - 1
            time_quantum = time_quantum - 1

        time = time + 1
    return (finished_list, history)

if __name__ == '__main__':
    input_file = "input_all.txt"
    print("Round-robin Scheduling Simulator")
    print("Input File: ", input_file)
    qtime = int(input("Input quantim time: "))
    print()
    process_list = load_from_file(input_file)
    #Print input table
    print_input_table(process_list)
    #Simulation Report (output)
    fin, history_list = simulator(process_list, quantum_time=qtime)
    print_simulation_report(fin, history_list)