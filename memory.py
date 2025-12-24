# Real-Time Memory Allocation Tracker
# Paging and Segmentation Simulation
TOTAL_MEMORY = 64   # Total memory in KB
PAGE_SIZE = 4       # Page size in KB
FRAMES = TOTAL_MEMORY // PAGE_SIZE
# PAGING
frames = [-1] * FRAMES          # Frame table, -1 means free
process_pages = {}              # Stores pages used by each process

def paging_allocate(pid, size):
    # Calculation of how much pages needed
    pages = (size + PAGE_SIZE - 1) // PAGE_SIZE
    free = [i for i in range(FRAMES) if frames[i] == -1]

    if len(free) < pages:
        print("Not enough memory for paging")
        return

    # Allocate frames
    for i in range(pages):
        frames[free[i]] = pid
    process_pages[pid] = pages
    print(f"Process {pid} allocated using paging")

def paging_deallocate(pid):
    # Free frames of the process
    for i in range(FRAMES):
        if frames[i] == pid:
            frames[i] = -1
    process_pages.pop(pid, None)
    print(f"Process {pid} removed from paging")

def paging_fragmentation():
    # Internal fragmentation
    used_frames = sum(1 for f in frames if f != -1)
    allocated = used_frames * PAGE_SIZE
    actual = sum(process_pages[pid] * PAGE_SIZE for pid in process_pages)
    return allocated - actual

def show_paging():
    print("\nPaging Memory:")
    for i, f in enumerate(frames):
        print(f"Frame {i}: {'Free' if f == -1 else 'P'+str(f)}")
    print("Internal Fragmentation:", paging_fragmentation(), "KB")

# SEGMENTATION
segments = []   # Each segment = (start, size, pid)

def segment_allocate(pid, size):
    current = 0
    for seg in segments:
        if seg[0] - current >= size:
            segments.append((current, size, pid))
            segments.sort()
            print(f"Process {pid} allocated using segmentation")
            return
        current = seg[0] + seg[1]

    if TOTAL_MEMORY - current >= size:
        segments.append((current, size, pid))
        segments.sort()
        print(f"Process {pid} allocated using segmentation")
    else:
        print("Not enough memory for segmentation")

def segment_deallocate(pid):
    global segments
    segments = [s for s in segments if s[2] != pid]
    print(f"Process {pid} removed from segmentation")

def external_fragmentation():
    if not segments:
        return TOTAL_MEMORY

    segments.sort()
    free = 0
    current = 0
    for seg in segments:
        free += seg[0] - current
        current = seg[0] + seg[1]
    free += TOTAL_MEMORY - current
    return free

def show_segments():
    print("\nSegmentation Memory:")
    if not segments:
        print("All memory free")
    for s in segments:
        print(f"P{s[2]} -> Start: {s[0]} KB, Size: {s[1]} KB")
    print("External Fragmentation:", external_fragmentation(), "KB")

#  MAIN MENU 
while True:
    print("\n=== Real-Time Memory Allocation Tracker ===")
    print("1 Paging Allocate")
    print("2 Paging Deallocate")
    print("3 Show Paging")
    print("4 Segmentation Allocate")
    print("5 Segmentation Deallocate")
    print("6 Show Segments")
    print("0 Exit")

    ch = input("Choice: ")

    if ch == "1":
        pid = int(input("PID: "))
        size = int(input("Size(KB): "))
        paging_allocate(pid, size)

    elif ch == "2":
        pid = int(input("PID: "))
        paging_deallocate(pid)

    elif ch == "3":
        show_paging()

    elif ch == "4":
        pid = int(input("PID: "))
        size = int(input("Size(KB): "))
        segment_allocate(pid, size)

    elif ch == "5":
        pid = int(input("PID: "))
        segment_deallocate(pid)

    elif ch == "6":
        show_segments()

    elif ch == "0":
        break
