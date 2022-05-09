# TO DO:
# Change RELATIVE_PATH_TO_SATGEN
# Change RELATIVE_PATH_TO_SATELLITE_STATE
# Change OUTPUT_DIR - directory to output the data

# Change SRC_NODE - source of the node
# Change DST_NODE - destination of the node

import exputil
import time

local_shell = exputil.LocalShell()
max_num_processes = 6

RELATIVE_PATH_TO_SATGEN = "../../../../satgenpy"
RELATIVE_PATH_FROM_SATGEN_TO_MY_TEST = "../ns3-sat-sim/simulator/my-test"

RELATIVE_PATH_FROM_SATGEN_TO_SATELLITE_STATE = RELATIVE_PATH_FROM_SATGEN_TO_MY_TEST + (
"/large-starlink/satellite_network_state/gen_data"
"/starlink_550_isls_gs_top_100_algorithm_free_gs_one_sat_many_only_over_isls"
)

RELATIVE_PATH_FROM_SATGEN_TO_OUTPUT_DIR = RELATIVE_PATH_FROM_SATGEN_TO_MY_TEST + (
"/satgen_analysis/data/"
)

RELATIVE_PATH_FROM_SATGETN_TO_COMMAND_LOGS = RELATIVE_PATH_FROM_SATGEN_TO_MY_TEST + (
    "/satgen_analysis/data/command_logs"
)
# Check that no screen is running
if local_shell.count_screens() != 0:
    print("There is a screen already running. "
          "Please kill all screens before running this analysis script (killall screen).")
    exit(1)

# Re-create data directory
local_shell.remove_force_recursive("data")
local_shell.make_full_dir("data")
local_shell.make_full_dir("data/command_logs")

# Where to store all commands
commands_to_run = []

# Manual
print("Generating commands for manually selected endpoints pair (printing of routes and RTT over time)...")


# Beijin(1593) to New York(1590) starlink 
commands_to_run.append(
    "cd {satgen_location};".format(satgen_location=RELATIVE_PATH_TO_SATGEN)+
    " python -m satgen.post_analysis.main_print_routes_and_rtt " +
    "{output_dir} {satellite_state_dir} {dynamic_update_interval_ms} {end_time_s} {src_num} {dst_num} ".format(
        output_dir=RELATIVE_PATH_FROM_SATGEN_TO_OUTPUT_DIR, 
        satellite_state_dir=RELATIVE_PATH_FROM_SATGEN_TO_SATELLITE_STATE,
        dynamic_update_interval_ms=100, end_time_s=500, src_num=1593, dst_num=1590
    )+
    "> {command_log_dir}/manual_starlink_isls_{src_num}_to_{dst_num}.log 2>&1".format(
        command_log_dir=RELATIVE_PATH_FROM_SATGETN_TO_COMMAND_LOGS, src_num=1593, dst_num=1590)
)

commands_to_run.append(
    "cd {satgen_location};".format(satgen_location=RELATIVE_PATH_TO_SATGEN)+
    " python -m satgen.post_analysis.main_print_graphical_routes_and_rtt " +
    "{output_dir} {satellite_state_dir} {dynamic_update_interval_ms} {end_time_s} {src_num} {dst_num} ".format(
        output_dir=RELATIVE_PATH_FROM_SATGEN_TO_OUTPUT_DIR, 
        satellite_state_dir=RELATIVE_PATH_FROM_SATGEN_TO_SATELLITE_STATE,
        dynamic_update_interval_ms=100, end_time_s=500, src_num=1593, dst_num=1590
    )+
    "> {command_log_dir}/manual_graphical_starlink_isls_{src_num}_to_{dst_num}.log 2>&1".format(
        command_log_dir=RELATIVE_PATH_FROM_SATGETN_TO_COMMAND_LOGS, src_num=1593, dst_num=1590)
)

print(RELATIVE_PATH_FROM_SATGETN_TO_COMMAND_LOGS)
print("Running commands (at most %d in parallel)..." % max_num_processes)
for i in range(len(commands_to_run)):
    print("Starting command %d out of %d: %s" % (i + 1, len(commands_to_run), commands_to_run[i]))
    local_shell.detached_exec(commands_to_run[i])
    while local_shell.count_screens() >= max_num_processes:
        time.sleep(2)


# Awaiting final completion before exiting
print("Waiting completion of the last %d..." % max_num_processes)
while local_shell.count_screens() > 0:
    time.sleep(2)
print("Finished.")