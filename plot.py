import glob
import matplotlib.pyplot as plt

def plot_logs(log_folder):
    data1_list = []
    data2_list = []
    data3_list = []
    data4_list = []
    log_files = glob.glob(log_folder + '/*')  # Find all files in the folder
    for log_file in log_files:
        if not log_file.endswith('.out'):  # Skip files that don't end with ".out"
            continue
        with open(log_file, 'r') as f:
            last_data = None
            for line in f:
                fields = line.strip().split()
                last_data = fields[-4:]  # Keep the last 4 numeric values in the line
            if last_data is not None:
                # Extract the last 4 numeric values from the line
                data1, data2, data3, data4 = [float(x) for x in last_data]
                data1_list.append(data1)
                data2_list.append(data2)
                data3_list.append(data3)
                data4_list.append(data4)
    plt.scatter(data1_list, data2_list, label='data 1 vs. data 2')
    plt.scatter(data3_list, data4_list, label='data 3 vs. data 4')
    plt.legend()
    plt.show()
