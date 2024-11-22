import matplotlib.pyplot as plt

def draw_gantt_chart(schedule):
    """
    Draws a Gantt chart using matplotlib.

    Parameters:
        schedule (list of tuples): List of (process_id, start_time, end_time) for each process.
    """
    fig, gnt = plt.subplots(figsize=(10, 5))
    gnt.set_ylim(0, 50)
    gnt.set_xlim(0, max([end for _, _, end in schedule]) + 1)

    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_yticks([15])
    gnt.set_yticklabels(['Processes'])
    gnt.grid(True)

    for process_id, start_time, end_time in schedule:
        gnt.broken_barh([(start_time, end_time - start_time)], (10, 10),
                        facecolors=('tab:blue'), label=f'P{process_id}')

    handles, labels = gnt.get_legend_handles_labels()
    unique_labels = list(dict(zip(labels, handles)).values())
    gnt.legend(unique_labels, [f'P{i[0]}' for i in schedule], loc='upper right')
    plt.savefig('gantt_chart.png')
    plt.show()

def fcfs(processes):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    gantt_chart = []
    schedule = []
    total_tat, total_wt = 0, 0

    for process in processes:
        pid, arrival_time, burst_time, _ = process
        start_time = max(current_time, arrival_time)
        completion_time = start_time + burst_time
        turnaround_time = completion_time - arrival_time
        waiting_time = turnaround_time - burst_time

        total_tat += turnaround_time
        total_wt += waiting_time

        schedule.append((pid, start_time, completion_time))
        gantt_chart.append((pid, start_time, completion_time))
        current_time = completion_time

        print(f"Process {pid}: TAT = {turnaround_time}, WT = {waiting_time}")

    avg_tat = total_tat / len(processes)
    avg_wt = total_wt / len(processes)

    print(f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}")
    print("Gantt Chart:", gantt_chart)
    draw_gantt_chart(schedule)


def sjf(processes):
    processes.sort(key=lambda x: (x[1], x[2]))  # Sort by arrival time, then burst time
    current_time = 0
    completed = []
    total_tat, total_wt = 0, 0

    while processes:
        available = [p for p in processes if p[1] <= current_time]
        if available:
            available.sort(key=lambda x: x[2])  # Select process with smallest burst time
            process = available[0]
            processes.remove(process)
            pid, arrival_time, burst_time, _ = process

            start_time = max(current_time, arrival_time)
            completion_time = start_time + burst_time
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - burst_time

            total_tat += turnaround_time
            total_wt += waiting_time

            completed.append((pid, start_time, completion_time))
            current_time = completion_time

            print(f"Process {pid}: TAT = {turnaround_time}, WT = {waiting_time}")
        else:
            current_time += 1

    avg_tat = total_tat / len(completed)
    avg_wt = total_wt / len(completed)

    print(f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}")
    print("Gantt Chart:", completed)

def priority_scheduling(processes):
    # Sort processes by arrival time, then priority
    processes.sort(key=lambda x: (x[1], x[3]))
    current_time = 0
    completed = []
    total_tat, total_wt = 0, 0

    while processes:
        # Get processes that have arrived
        available = [p for p in processes if p[1] <= current_time]
        if available:
            # Select the process with the highest priority (lowest value)
            available.sort(key=lambda x: x[3])  # Sort by priority
            process = available[0]
            processes.remove(process)
            pid, arrival_time, burst_time, priority = process

            start_time = max(current_time, arrival_time)
            completion_time = start_time + burst_time
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - burst_time

            total_tat += turnaround_time
            total_wt += waiting_time

            completed.append((pid, start_time, completion_time))
            current_time = completion_time

            print(f"Process {pid}: TAT = {turnaround_time}, WT = {waiting_time}")
        else:
            # If no process is available, move the clock forward
            current_time += 1

    avg_tat = total_tat / len(completed)
    avg_wt = total_wt / len(completed)

    print(f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}")
    print("Gantt Chart:", completed)

def rr(processes, time_quantum):
    processes = [[*p, p[2]] for p in processes]  # Add remaining burst time
    queue = []
    current_time = 0
    total_tat, total_wt = 0, 0
    gantt_chart = []

    while processes or queue:
        while processes and processes[0][1] <= current_time:
            queue.append(processes.pop(0))
        
        if queue:
            process = queue.pop(0)
            pid, arrival_time, burst_time, priority, remaining_time = process

            execution_time = min(remaining_time, time_quantum)
            remaining_time -= execution_time
            gantt_chart.append((pid, current_time, current_time + execution_time))
            current_time += execution_time

            if remaining_time == 0:
                turnaround_time = current_time - arrival_time
                waiting_time = turnaround_time - burst_time
                total_tat += turnaround_time
                total_wt += waiting_time
                print(f"Process {pid}: TAT = {turnaround_time}, WT = {waiting_time}")
            else:
                queue.append([pid, arrival_time, burst_time, priority, remaining_time])
        else:
            current_time += 1

    avg_tat = total_tat / len(gantt_chart)
    avg_wt = total_wt / len(gantt_chart)

    print(f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}")
    print("Gantt Chart:", gantt_chart)

def srtf(processes):
    processes = sorted(processes, key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    total_tat, total_wt = 0, 0
    completed = 0
    n = len(processes)
    remaining_times = {p[0]: p[2] for p in processes}
    gantt_chart = []
    last_pid = -1

    while completed < n:
        available = [p for p in processes if p[1] <= current_time and remaining_times[p[0]] > 0]
        if available:
            available.sort(key=lambda x: remaining_times[x[0]])  # Sort by remaining time
            process = available[0]
            pid, arrival_time, burst_time, _ = process

            if last_pid != pid:
                gantt_chart.append((pid, current_time))

            remaining_times[pid] -= 1
            last_pid = pid
            current_time += 1

            if remaining_times[pid] == 0:
                completion_time = current_time
                turnaround_time = completion_time - arrival_time
                waiting_time = turnaround_time - burst_time
                total_tat += turnaround_time
                total_wt += waiting_time
                completed += 1
                print(f"Process {pid}: TAT = {turnaround_time}, WT = {waiting_time}")
        else:
            current_time += 1

    avg_tat = total_tat / n
    avg_wt = total_wt / n

    gantt_chart = [(p[0], t, gantt_chart[i+1][1]) for i, (p, t) in enumerate(gantt_chart[:-1])]
    print(f"Average TAT: {avg_tat:.2f}, Average WT: {avg_wt:.2f}")
    print("Gantt Chart:", gantt_chart)

def main():
    print("CPU Scheduling Simulator")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Priority Scheduling (Non-Preemptive)")
    print("4. Round Robin (RR)")
    print("5. Shortest Remaining Time First (SRTF)")

    choice = int(input("Select an algorithm: "))

    n = int(input("Enter the number of processes: "))
    processes = []

    for i in range(n):
        pid = i + 1
        arrival_time = int(input(f"Enter arrival time for process {pid}: "))
        burst_time = int(input(f"Enter burst time for process {pid}: "))
        priority = int(input(f"Enter priority for process {pid} (lower value = higher priority): ")) if choice == 3 else 0
        processes.append([pid, arrival_time, burst_time, priority])

    if choice == 1:
        fcfs(processes)
    elif choice == 2:
        sjf(processes)
    elif choice == 3:
        priority_scheduling(processes)
    elif choice == 4:
        time_quantum = int(input("Enter time quantum: "))
        rr(processes, time_quantum)
    elif choice == 5:
        srtf(processes)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
