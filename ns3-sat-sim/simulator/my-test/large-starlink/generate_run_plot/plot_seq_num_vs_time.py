import pandas as pd
import matplotlib.pyplot as plt
import sys

def read_udp_burst_from_csv(logs_ns3_dir, udp_burst_id):
    incoming_burst_csv_path = "{}/udp_burst_{}_incoming.csv".format(logs_ns3_dir, udp_burst_id)
    outgoing_burst_csv_path = "{}/udp_burst_{}_outgoing.csv".format(logs_ns3_dir, udp_burst_id)

    # retrieve the data and return the panda object with the appropriate headers
    udp_burst_headers = ["udp_schedule_id", "seq_num", "timestamp"]
    df_incoming = pd.read_csv(incoming_burst_csv_path, names=udp_burst_headers)
    df_outgoing = pd.read_csv(outgoing_burst_csv_path, names=udp_burst_headers)

    return df_incoming, df_outgoing

def plot_sequence_num_vs_time(df_incoming, df_outgoing, plot_output_dir):
    # parse input data
    incoming_x = df_incoming["timestamp"]
    incoming_y = df_incoming["seq_num"]

    outgoing_x = df_outgoing["timestamp"]
    outgoing_y = df_outgoing["seq_num"]

    # fix scale
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(outgoing_x, outgoing_y, label="outgoing")
    ax.plot(incoming_x, incoming_y, label="incoming")

    # adjust scale
    
    # show legend and labels
    plt.legend()
    plt.ylabel("Seq Num")
    plt.xlabel("Timestamp")

    plt.title("Seq vs Timestamp")
    plt.savefig('temp.png')
    return

def plot_udp_burst_seqeunce_num_vs_time(
    logs_ns3_dir, 
    plot_output_dir, 
    udp_burst_id
):

    return

def main():
    args = sys.argv[1:]
    if len(args) != 3:
        print("Must supply exactly four arguments")
        print("Usage: python plot_udp_burst.py [logs_ns3_dir] [plot_output_dir] [udp_burst_id]")
        exit(1)
    else:
        df_incoming, df_outgoing = read_udp_burst_from_csv(args[0], args[2])
        plot_sequence_num_vs_time(df_incoming, df_outgoing)


if __name__ == "__main__":
    main()
