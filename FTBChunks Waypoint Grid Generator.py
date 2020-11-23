import json, glob, os, copy, re
from collections import OrderedDict

def WriteOutputFile(data):
    with open(waypoints_file_name, "w") as file:
        # print(json.dumps(data))
        print('Writing waypoints file with updated data')
        json.dump(data, file)
        file.close()

def IsGridWaypoint(inString):
    return re.search('^Grid\d+$', inString)

def ShowGridWaypoints(data):
    print("Showing all grid waypoints.")
    for i in waypoints:
        if(IsGridWaypoint(i['name'])):
            i['hidden'] = False
    WriteOutputFile(data)


def HideGridWaypoints(data):
    print("Hiding all grid waypoints.")
    for i in waypoints:
        if(IsGridWaypoint(i['name'])):
            i['hidden'] = True
    WriteOutputFile(data)


def DeleteGridPoints(data):
    print("Deleting all grid waypoints. Original source waypoints are preserved.")
    index = len(waypoints) - 1
    for i in reversed(waypoints):
        if(re.search('^Grid\d+$', i['name'])):
            print("deleting waypoint: ", i, "at index ", index)
            waypoints.pop(index)
        index -= 1
    WriteOutputFile(data)

waypoints_file_name = "waypoints.json"

try:
    with open(waypoints_file_name, "r") as file:
        data = json.load(file)
        waypoints = data["waypoints"]
        file.close()
except FileNotFoundError:
    print("waypoints.json not found in {}\n\tProgram will exit...".format(os.getcwd()))
    input("\nPress enter to terminate...")
    exit()


while(True):
    index = 0
    for i in waypoints:
        # if i['name'] != "":\ # Removed due to causing index mismatches when we reference the waypoint later on. Should fix for quality of life.
        # print(index, "-", i['name'], "\"\tIs Hidden:", i['hidden'])
        print("{0} - {1:20} \tIs Hidden: {2}".format(index, "\"" + i['name'] + "\"", i['hidden']))
        index += 1
        
    print("\nPick the waypoint you would like to use as the starting point\nType delete to delete all grid waypoints. Will remove points called \"Grid{N}\"\nOr type exit to exit\n")
    chosen_waypoint = input('>> ')
    if(chosen_waypoint.lower() == "exit"):
        exit()
    elif (chosen_waypoint.lower() == "hide"):
        HideGridWaypoints(data)
    elif (chosen_waypoint.lower() == "show"):
        ShowGridWaypoints(data)
    elif (chosen_waypoint.lower() == "delete"):
        DeleteGridPoints(data)
    else:
        try:
            chosen_waypoint = int(chosen_waypoint)
        except ValueError:
            print("Please only enter an integer or 'delete' - program will now exit.")
            exit()
        print("\nPick the offsets and grid size.\nThe offset is how many blocks will be between each waypoint in the grid.\nUse negative offsets to change the direction the grid is created in.\n")
        try:
            print("+ E\n- W")
            offset_x = int(input('X Offset >> '))
            print("+ S\n- N")
            offset_z = int(input('Z Offset >> '))
            grid_w = int(input('Grid Width >> '))
            grid_h = int(input('Grid Height >> '))
        except ValueError as identifier:
            print("Lmao you broke it. You gotta only enter integers. Program will now exit.")
            exit()

        pulled_waypoint = copy.copy(waypoints[chosen_waypoint])
        print("Operating on waypoint: ", pulled_waypoint)

        original_x = pulled_waypoint["x"]
        # original_z = pulled_waypoint["z"]

        index = 0
        for i in range(grid_h):
            for i in range(grid_w):
                pulled_waypoint['name'] = "Grid{}".format(index)
                print("Iteration: ", pulled_waypoint['name'], pulled_waypoint['x'], pulled_waypoint['z'])
                waypoints.append(copy.copy(pulled_waypoint))
                pulled_waypoint["x"] = int(pulled_waypoint["x"]) + offset_x # Increment X pos
                index += 1
            pulled_waypoint["z"] = pulled_waypoint["z"] + offset_z # Increment Z pos
            pulled_waypoint["x"] = original_x

        WriteOutputFile(data)
    print("== Done! ==")
    input("Press enter to continue...")

