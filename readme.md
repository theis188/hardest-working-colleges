This is readme for the careertrend.com hardest working colleges report.

The report was generated using Python 3.5 and has dependencies on pandas and numpy.

The report uses data from NCES (included), and the Census (you will have to download).

The ACS PUMS (Census) data is over 1 GB, download here: https://www2.census.gov/programs-surveys/acs/data/pums/2015/1-Year/csv_pus.zip

You'll need to unzip the download. Then add the folder location to line 11 of hardest_working_colleges.py.

Execute hardest_working_colleges.py in its own directory. It will generate output.csv, a summary of the results. This execution may take some time, as processing the ACS data takes some time (20+ minutes). It will run most effectively on machines with at least 16GB of memory to handle the large data sets.

For any questions, contact matthew.theisen@leafgroup.com