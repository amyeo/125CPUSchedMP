"""
CMSC 125 MP1
Preemptive priority CPU scheduler simulator
Follows new timing pattern

Input from file.
"""
import threading
from MP1 import ProcessLine, load_from_file, print_input_table, print_simulation_report
from terminaltables import SingleTable

def simulator(PLPending_list):
    finished_list = []
    current_task = None
    pending = PLPending_list
    time = 0
    history = []
    while len(pending) > 0 or current_task != None:
        ### Report Stats
        if current_task:
            history.append(("P"+str(current_task.id),time))
        else:
            history.append(("X",time))

        ### Tick Timer

        ### Unload Job
        if current_task != None: #task currently loaded
            #卒業事情確認優先
            if current_task.burst_time <=0: #卒業状況あった
                #UNLOAD and graduate
                current_task.completion_time = time
                #current_task.turnaround_time = time
                current_task.turnaround_time = current_task.completion_time-current_task.arrival_time
                current_task.waiting_time = int(current_task.turnaround_time - current_task.burst_original)
                finished_list.append(current_task)
                current_task = None
            else:
                #find minimum
                pending_minimum_arr = []
                for x in pending:
                    if x.arrival_time <= time: #confine to present processes
                        pending_minimum_arr.append(x.priority_number)
                if len(pending_minimum_arr) > 0:
                    pending_minimum = min(pending_minimum_arr)
                    #Check for UNLOAD condition: pending minimum is less than current
                    if pending_minimum < current_task.priority_number:
                        #UNLOAD temporarily
                        pending.append(current_task)
                        current_task = None

        ### Load Job
        if current_task == None: #NO task currently loaded. Find one.
            #no current task executing! Start selection.
            #find minimum
            pending_minimum_arr = []
            for x in pending:
                if x.arrival_time <= time: #confine to present processes
                    pending_minimum_arr.append(x.priority_number)
            if len(pending_minimum_arr) > 0:
                pending_minimum = min(pending_minimum_arr)
                for p in pending: #handle start
                    #choose shortest and load.
                    if p.priority_number == pending_minimum and current_task == None and p.arrival_time <= time:
                        current_task = p
                        current_task.response_time = time - current_task.arrival_time
                        #current_task.waiting_time = time
                        pending.remove(p)
                        break

        ### Tick Current Job
        if current_task: #task currently loaded
            current_task.burst_time = current_task.burst_time - 1

        time = time + 1
    return (finished_list, history)

if __name__ == '__main__':
    input_file = "input_all.txt"
    print("Preemptive Priority Scheduling Simulator")
    print("Input File: ", input_file)
    print()
    process_list = load_from_file(input_file)
    #Print input table
    print_input_table(process_list)
    #Simulation Report (output)
    fin, history_list = simulator(process_list)
    print_simulation_report(fin, history_list)