import matplotlib.pyplot as plt

def draw_gantt_chart(schedule, output_file):
    """
    Draws a Gantt chart using matplotlib for the given schedule.

    Parameters:
        schedule (list of tuples): List of (process_id, start_time, end_time) for each process.
        output_file (str): File name to save the chart as a PNG image.
    """
    fig, gnt = plt.subplots(figsize=(12, 6))
    
    # Extract unique processes for the chart
    process_ids = list(set(pid for pid, _, _ in schedule))
    process_positions = {pid: i for i, pid in enumerate(sorted(process_ids))}

    gnt.set_xlim(0, max(end_time for _, _, end_time in schedule) + 1)
    gnt.set_ylim(0, 10 * len(process_positions))
    
    gnt.set_xlabel('Time')
    gnt.set_ylabel('Processes')
    gnt.set_yticks([5 + i * 10 for i in range(len(process_positions))])
    gnt.set_yticklabels([f"P{pid}" for pid in sorted(process_positions.keys())])
    gnt.grid(True)

    for process_id, start_time, end_time in schedule:
        gnt.broken_barh([(start_time, end_time - start_time)], 
                        (process_positions[process_id] * 10, 8), 
                        facecolors=('tab:blue'))

    plt.title("Gantt Chart")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    print(f"Gantt chart saved as {output_file}")

def fcfs(processes, output_file):
    processes.sort(key=lambda x: x[1])  # Sort by arrival time
    current_time = 0
    total_tat, total_wt = 0, 0
    schedule = []
    results = []

    for process in processes:
        pid, arrival_time, burst_time, _ = process
        start_time = max(current_time, arrival_time)
        completion_time = start_time + burst_time
        turnaround_time = completion_time - arrival_time
        waiting_time = turnaround_time - burst_time

        total_tat += turnaround_time
        total_wt += waiting_time

        schedule.append((pid, start_time, completion_time))
        results.append(f"P{pid}: TAT = {turnaround_time}, WT = {waiting_time}")
        current_time = completion_time

    avg_tat = total_tat / len(processes)
    avg_wt = total_wt / len(processes)

    results.append(f"Average TAT: {avg_tat:.2f}")
    results.append(f"Average WT: {avg_wt:.2f}")
    with open(output_file, 'w') as f:
        f.write("\n".join(results))
        f.write("\n")
    draw_gantt_chart(schedule, "fcfs_gannt.png")


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
    input_file = input("Enter the input file name: ")
    output_file = input("Enter the output file name: ")

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        algorithm = int(lines[0].strip())
        num_processes = int(lines[1].strip())
        processes = []
        time_quantum = None

        for i in range(num_processes):
            parts = list(map(int, lines[i + 2].strip().split()))
            if len(parts) == 3:
                processes.append([i + 1, parts[0], parts[1], parts[2]])  # Priority Scheduling
            else:
                processes.append([i + 1, parts[0], parts[1], 0])  # FCFS, SJF, or RR

        if algorithm == 4:  # Round Robin
            time_quantum = int(lines[-1].strip())

        if algorithm == 1:
            fcfs(processes, output_file)
        # Add similar calls for other algorithms like sjf_with_file, priority_with_file, rr_with_file, etc.
        else:
            print("Algorithm not implemented yet.")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except ValueError:
        print("Invalid input format.")

if __name__ == "__main__":
    main()
