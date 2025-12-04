"""
Lab Assignment 10: Print Summary Statistics
Submitted by Jaymie Redman
Submitted: November 25, 2025


Assignment 10: Adds the ability to load a temperature CSV file, choose units,
convert units, and display summary statistics for the dataset.

Assignment 9: This assignment adds the ability to load a temperature data file.
The program reads the CSV, filters out non-temperature entries, stores the
cleaned data in the TempDataset object, reports how many samples were loaded,
and lets the user name the dataset.

Assignment 8: This project defines a class to manage temperature data. It
includes placeholder methods for loading data, calculating statistics, and
tracking the number of TempDataset objects created. A unit test is provided to
verify the class and methods work as expected.

Assignment 7: This assignment introduces two methods (in detail).
print_filter() - prints a list of sensors that are active and inactive.
change_filter() - allows a user to activate a sensor or deactivate it.
The change_filter() is initiated through the menu prompt #3 choice.
The change_filter() method will print the filter list showing active or
inactive states, and it will allow the user to turn a sensor on or off.

Assignment 6: Bubble sort a sensor list but using recursion. Use a test case
as provided (similar to assignment 5, but with reference to the sensor list
information from assignment 4).

Assignment 5: A separate recursion assignment (as another project; see
assignment 5)

Assignment 4: Creating a Sensor List and Filter List using a dictionary and
list comprehensions.

Assignment 3: Adds a menu interface for the user, which prompts them to select
different options.

Assignment 2: This assignment adds code to prompt the user for a temperature
in Celsius and then converts that temperature to a specified different
temperature unit.

Assignment 1: This program demonstrates printing lines of text to the screen
"""
import math

UNITS = {
    0: ("Celsius", "C"),
    1: ("Fahrenheit", "F"),
    2: ("Kelvin", "K")
}

current_unit = 0

def print_header():
    """Print project title and name"""
    print()
    print("STEM Center Temperature Project")
    print("Jaymie Redman")
    
    
def convert_units(celsius_value, units):
    """Convert Celsius to specified units"""
    if units == 0:
        return celsius_value
    elif units == 1:
        return (celsius_value * 1.8) + 32
    elif units == 2:
        return celsius_value + 273.15
    else:
        return None


def print_menu():
    """Print the main menu"""
    print()
    print("Main Menu")
    print("---------")
    print("1 - Process a new data file")
    print("2 - Choose units")
    print("3 - Edit room filter")
    print("4 - Show summary statistics")
    print("5 - Show temperature by date and time")
    print("6 - Show histogram of temperatures")
    print("7 - Quit")
    print()


def recursive_sort(list_to_sort, key, n=None):
    """Recursively sort list_to_sort by the given key index"""
    if n is None:
        n = len(list_to_sort)
    if n == 1:
        return list_to_sort
    for i in range(n - 1):
        if list_to_sort[i][key] > list_to_sort[i + 1][key]:
            list_to_sort[i], list_to_sort[i + 1] = (list_to_sort[i + 1],
                                                    list_to_sort[i])
    return recursive_sort(list_to_sort, key, n - 1)


def print_filter(sensor_list, filter_list):
    """Print [ACTIVE] or toggle it off"""
    print()
    for room_number, room_name, sensor_num in recursive_sort(sensor_list,
                                                             0):
        status = "[ACTIVE]" if sensor_num in filter_list else ""
        print(f"{room_number}: {room_name} {status}")
    print()


def change_filter(sensor_list, filter_list):
    """Allow user to toggle sensors on or off"""
    while True:
        print_filter(sensor_list, filter_list)
        choice = input("Type the sensor to toggle (e.g. 4201) or x to end: ")
        if choice.lower() == 'x':
            break
        matched = [sensor_num for room, name, sensor_num in sensor_list if room
                   == choice]
        if matched:
            sensor_num = matched[0]
            if sensor_num in filter_list:
                filter_list.remove(sensor_num)
            else:
                filter_list.append(sensor_num)
        else:
            print("Invalid Sensor")


def new_file(current_set):
    """Prompt user to load a new dataset and set its name."""
    filename = input("Please enter the filename of the new dataset: ")
    if current_set.process_file(filename):
        print(f"Loaded {current_set.get_loaded_temps()} samples.")
        while True:
            try:
                name_input = input("\nPlease provide a 3 to 20 character "
                                   "name for the dataset Test Week: ")
                current_set.name = name_input
                break
            except ValueError:
                print("Bad name! Must enter good name!")
    else:
        print("Unable to load.")
        
        
def choose_unit():
    """Prompt the user to select a temperature unit and update current_unit."""
    global current_unit
    
    print(f"\nCurrent unit in {UNITS[current_unit][0]}")
    print("\nChoose new unit:")
    for key in UNITS:
        print(f"{key} - {UNITS[key][0]}")
    print()
    user_input = input("Which unit? ")
    try:
        users_choice = int(user_input)
    except ValueError:
        print("*** Please enter a number only ***\n")
        choose_unit()
    else:
        if users_choice in UNITS:
            current_unit = users_choice
            return users_choice
        else:
            print("*** Please choose unit from the list ***\n")
            choose_unit()
            
            
def print_summary_statistics(dataset, filter_list):
    """Print summary statistics for the dataset"""
    stats = dataset.get_summary_statistics(filter_list)
    if stats is None:
        print(
            "Please load data file and make sure at least one sensor is "
            "active")
    else:
        min_temp, max_temp, avg_temp = stats
        print("\nSummary statistics for Test Week")
        print(f"Minimum Temperature: {min_temp:.2f} {UNITS[current_unit][1]}")
        print(f"Maximum Temperature: {max_temp:.2f} {UNITS[current_unit][1]}")
        print(f"Average Temperature: {avg_temp:.2f} {UNITS[current_unit][1]}")
        

class TempDataset:
    temp_dataset_value = 0
    
    def __init__(self):
        """Initialize a new TempDataset object."""
        self._data_set = []
        self._name = "Unnamed"
        TempDataset.temp_dataset_value += 1
    
    @property
    def name(self):
        """Return the current name."""
        return self._name
    
    @name.setter
    def name(self, new_name):
        """Set a name if it meets length requirements."""
        if 3 <= len(new_name) <= 20:
            self._name = new_name
        else:
            raise ValueError
    
    def process_file(self, filename):
        """Load csv file."""
        try:
            with open(filename, "r") as file:
                self._data_set = []
                for line in file:
                    try:
                        lines = line.strip().split(",")
                        lines[0] = int(lines[0])
                        lines[1] = math.floor(float(lines[1]) * 24)
                        lines[2] = int(lines[2])
                        if lines[3] != "TEMP":
                            continue
                        lines[4] = float(lines[4])
                        temp_tuple = lines[0], lines[1], lines[2], lines[4]
                        self._data_set.append(temp_tuple)
                    except ValueError:
                        continue
            return True
        except FileNotFoundError:
            return False
    
    def get_summary_statistics(self, filter_list):
        """Show Summary statistics"""
        temps = [convert_units(temp[3], current_unit) for temp in self._data_set
                 if temp[2] in filter_list]
        if not temps:
            return None
        return min(temps), max(temps), sum(temps) / len(temps)
    
    def get_avg_temperature_day_time(self, filter_list, day, time):
        """Return average temperature of day/time."""
        if not self._data_set or not filter_list or all(
            temp[2] not in filter_list for temp in self._data_set):
            return None
        
        temps = [
            temp[3] for temp in self._data_set
            if temp[2] in filter_list and temp[0] == day and temp[1] == time
        ]
        
        if not temps:
            return None
        
        return sum(temps) / len(temps)
    
    def get_num_temps(self, filter_list, lower_bound, upper_bound):
        """Return a count of temperatures."""
        return None
    
    def get_loaded_temps(self):
        """Return loaded temperatures."""
        if self._data_set:
            return len(self._data_set)
        else:
            return None
    
    @classmethod
    def get_num_objects(cls):
        """Return total number of TempDataset objects created."""
        return cls.temp_dataset_value


def main():
    """Run the STEM Center Temperature Project.

    Initializes sensors and filter list, prints the header, and displays
    the main menu. Handles user choices to load data, change units,
    edit filters, and display statistics.
    """
    sensors = {
        "4213": ("STEM Center", 0),
        "4201": ("Foundations Lab", 1),
        "4204": ("CS Lab", 2),
        "4218": ("Workshop Room", 3),
        "4205": ("Tiled Room", 4),
        "Out": ("Outside", 5),
    }
    
    sensor_list = [(key, sensors[key][0], sensors[key][1]) for key in sensors]
    filter_list = [sensor[2] for sensor in sensor_list]
    print_header()
    
    while True:
        print_menu()
        print(current_set.get_avg_temperature_day_time
              (filter_list, 5, 7)) # for testing
        
        try:
            choice = int(input("What is your choice? "))
            if choice == 1:
                new_file(current_set)
            elif choice == 2:
                choose_unit()
            elif choice == 3:
                change_filter(sensor_list, filter_list)
            elif choice == 4:
                print_summary_statistics(current_set, filter_list)
            elif choice == 5:
                print("Print Temp by Day/Time Function Called")
            elif choice == 6:
                print("Print Histogram Function Called")
            elif choice == 7:
                print("Thank you for using the STEM Center Temperature Project")
                break
            else:
                print(
                    "Invalid Choice, please enter an integer between 1 and 7.")
        except ValueError:
            print("*** Please enter a number only ***")
            

if __name__ == "__main__":
    current_set = TempDataset()
    
    main()


r"""
C:\Users\jredm\PycharmProjects\PythonProject\.venv\Scripts\python.exe C:\Users\jredm\PycharmProjects\PythonProject\Assignments\Assignment_10.py

STEM Center Temperature Project
Jaymie Redman

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 4
Please load data file and make sure at least one sensor is active

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 1
Please enter the filename of the new dataset: Temperatures_2025-11-07.csv
Loaded 11724 samples.

Please provide a 3 to 20 character name for the dataset Test Week: aaa

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 4

Summary statistics for Test Week
Minimum Temperature: 16.55 C
Maximum Temperature: 28.42 C
Average Temperature: 21.47 C

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 2

Current unit in Celsius

Choose new unit:
0 - Celsius
1 - Fahrenheit
2 - Kelvin

Which unit? 1

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 4

Summary statistics for Test Week
Minimum Temperature: 61.79 F
Maximum Temperature: 83.16 F
Average Temperature: 70.64 F

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

20.45544117647059
What is your choice? 3

4201: Foundations Lab [ACTIVE]
4204: CS Lab [ACTIVE]
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: 4201

4201: Foundations Lab
4204: CS Lab [ACTIVE]
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: 4204

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: x

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

19.910638297872342
What is your choice? 4

Summary statistics for Test Week
Minimum Temperature: 61.79 F
Maximum Temperature: 83.16 F
Average Temperature: 70.13 F

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

19.910638297872342
What is your choice? 3

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room [ACTIVE]
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: 4205

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room
4213: STEM Center [ACTIVE]
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: 4213

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room
4213: STEM Center
4218: Workshop Room [ACTIVE]
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: 4218

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room
4213: STEM Center
4218: Workshop Room
Out: Outside [ACTIVE]

Type the sensor to toggle (e.g. 4201) or x to end: Out

4201: Foundations Lab
4204: CS Lab
4205: Tiled Room
4213: STEM Center
4218: Workshop Room
Out: Outside

Type the sensor to toggle (e.g. 4201) or x to end: x

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 4
Please load data file and make sure at least one sensor is active

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

None
What is your choice? 7
Thank you for using the STEM Center Temperature Project

Process finished with exit code 0
"""
