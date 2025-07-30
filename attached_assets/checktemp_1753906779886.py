from netmiko import ConnectHandler
import pandas as pd
import datetime
import time

ts = time.time()

# Specify the path to your Excel file
excel_file_path = 'switchFile.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

 # Convert the DataFrame to a list of dictionaries
# 'records' orientation creates a list where each element is a dictionary
# representing a row, with column headers as keys.
list_of_switches = df.to_dict(orient='records')

# Print the resulting list of dictionaries
#print(list_of_switches)

# Commands to execute
commands = [
    'show env temp'
]

time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
outputsVar ='Start Script at Time: ' + time + '\n'
#loop through all switches in the given excel spreadsheet
for switch in list_of_switches:
    try:
        # Establish SSH connection
        net_connect = ConnectHandler(**switch)

        # If enable mode is required
        # net_connect.enable()

        for command in commands:
            print(f"Executing '{command}' on {switch['host']}...")
            output = net_connect.send_command(command)
            hostname = net_connect.send_command('sh run | i host').split()[1]
            outputsVar += '\n --- Output of '+ command +' on ' + hostname + ' \n' + output + '\n\n'

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Disconnect from the switch
        if 'net_connect' in locals() and net_connect.is_alive():
            net_connect.disconnect()

# Output file name
output_file = 'device_output3' + time + '.txt'
# Open file to write output after going through all switches
with open(output_file, 'w') as f:
    f.write(outputsVar)