# Identifying Twitter popular topics consistent in time
Project for the Data Mining course @ UNITN

The purpose of this project is to identify topics in tweets that 
become popular in different periods of time.
The analysis and the description of the solution can be found in the 
file doc/Report.pdf

# Requirements
Developed and tested with Python version 3.8.5

Libraries:
- Pandas
- NLTK
- Regex
- HTML

The libraries can be installed by running the command

```[shell]
pip install -r src/requirements.txt
```

# Folder strucure

The root folder has four subfolders:
- **bin/** contains the results obtained by the algorithm
- **data/** contains the original dataset and the pre-processed one
- **doc/** contains the report of the project
- **src/** contains the code of the solution proposed, along with the code used to preprocess the data

# Running

The executable to run is **src/main.py**, so by running
```[bash]
python3 src/main.py --help
```
you will get the following output:
```
usage: Program to find consistent popular topics in tweets.
     [-h] [--input INPUT] [--output_dir OUTPUT_DIR] [--s S] [--r R] [--a A]
                                                                 [--start START] [--end END] [--basic]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         path to the file in input (csv format with two columns 'time' and 'tokens') (default:
                        data/cleaned_covid19_tweets.csv)
  --output_dir OUTPUT_DIR
                        path to the output directory (default: bin/results/)
  --s S                 minimum support to consider a topic frequent in a period of time (default: 0.01)
  --r R                 minimum support to consider a topic consistent among the periods of time (default: 0.1)
  --a A                 amplitude of each period of time in seconds (default: 86400)
  --start START         start timestamp of the first period to consider. If not set, it will be set the midnight
                        of the day of the oldest tweet in the dataset. (default: None)
  --end END             end timestamp of the last period to consider. If not set, it will be set the timestamp of 
                        the most recent tweet in the dataset. (default: None)
  --basic               use the basic apriori implementation (default: False)
```

So the algorithm can be run with default parameters with the command

```[bash]
python src/main.py
```

The parameters can be customized by using command line options, for instance
```
python src/main.py --s 0.01 --r 0.1 --a 86400
```

The output will be stored in *bin/results* and the name of the output file is 
in the format `<s>#<r>#<a>#<current_timestamp>`