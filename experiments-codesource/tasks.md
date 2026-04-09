# Tasks

[x] Task 1

- save resolved_config as yaml file instead of json
- keep only one model per experiment which have the best total reward

[x] Task 2

- Merge helper_plot.py and training_plots.py inside one file and remove redondance code

[x] Task 3

- Move all input variable to yaml file, such final_nb_aps (int), num_aps (int).
  on_line (bool) mode: can be different for train and evaluate phase.
  'df_shuffled_200.csv' use variable for it.

[x] Task 4

- Refacoring what the program logg
  logg Execution time (17.993168 seconds) using minutes instead of seconds.
  logg run_dir and log_file using relative path instead of absolute.

- Add evaluation results as new row inside the csv file experiments_results.csv.

[ ] Task 5

- Move variable p (parmutation) from claude_a2c_online.py to illinois_online.py inside the reset function. This update make p value update every reset environment
