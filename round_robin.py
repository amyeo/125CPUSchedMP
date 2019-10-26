"""
CMSC 125 MP1
Round robin CPU scheduler simulator
Follows new timing pattern

Input from file.
"""
import threading
from MP1 import ProcessLine, load_from_file, print_input_table, print_simulation_report
from terminaltables import SingleTable

def arrival(inp):
    return inp.arrival_time

def simulator(PLPending_list, quantum_time=4):
    finished_list = []
    current_task = None
    pending = PLPending_list
    time = 0
    time_quantum = quantum_time #reset
    history = []
    ##before starting, sort pending by ARRIVAL TIME
    #pending.sort(key=arrival)
    run = []
    while len(pending) > 0 or current_task != None:
        ### Report Stats
        if current_task:
            history.append(("P"+str(current_task.id),time))
        else:
            history.append(("X",time))

        ### Add to queue applicable
        for x in pending:
            if x.arrival_time <= time:
                #run.insert(0,x)
                run.append(x)
                pending.remove(x)


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
            elif time_quantum <=0:
                #hibernate process
                run.append(current_task)
                current_task = None
                #time_quantum = quantum_time #reset


        ### Load Job
        #FCFS MODE
        if current_task == None: #NO task currently loaded. Find one.
            for p in run: #handle start
                #choose shortest and load.
                if current_task == None and p.arrival_time <= time:
                    current_task = p
                    if current_task.response_time == -1:
                        current_task.response_time = time - current_task.arrival_time
                    #current_task.waiting_time = time
                    run.remove(p)
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