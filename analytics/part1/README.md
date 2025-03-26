# Part 1: Analytics Implementation

## Overview

Part 1 focuses on implementing an analytics metric called **Levels Full**, which is used to understand how members move between membership levels in a credit union. Each member is assigned a level (A through F) based on a computed score based on their financial activity. These levels are defined using predefined score ranges. The task involves analyzing members' current scores, historical scores, and their product accounts to track metrics such as movement between levels, member count in the level, average product count, and member count history.

## Design Choices and Assumptions

### Using Pandas Over Dataclasses
Though the assessment provides a set of Python dataclasses (e.g., `Level`, `MemberLevelScore`, `MemberProductAccount`), I chose to use **pandas DataFrames** and **pandas operations** for the following reasons:

1. **Data Manipulation**: Pandas operations like filtering, grouping, merging, and cutting are more concise and efficeint compared to iterating over and manually transforming lists of dataclass objects
   - Using **IntervalIndex** to create score ranges for each level and **pd.cut()** to assign members to a level based on their current score had a major advantage over operating on dataclasses
   - Brought the runtime from an average of **1 minute** to loop through each dataclass object for level assignment to **> 1 second**
   - Similarly, this method was used to assign levels to each user's historical scores at each point in the timeline, improving the runtime from **2 minutes to 7 seconds**.

3. **Data Loading and Exploration**  
   Since all of the data files were .csv files, using `pd.read_csv()` allowed for direct ingestion into a form of data that was ready to access and manipulate. Parsing through megabytes of data and organizing them into dataclasses took significantly longer, **upwards for 3 minutes**, compared to using `pd.read_csv()`, which took about **4 seconds**.

**Trade-Offs**
- Because I was not using the dataclasses, I had to manually implement the data rules and checks to remain consistent with the structure and definitions of the data models
- However, by taking that extra step, I was able to retain the data's consistency and accuracy that the dataclasses offer, while also gaining the efficiency and flexibility from leveraging pandas Dataframes and operations

Dataclasses are still valuable for type safety, consistency, and structured use cases (e.g., APIs or model building). But for the analytical focus of Part 1, Pandas provides the best balance of power, simplicity, and readability.

### Handling Missing Historical Scores
A section of this part that required an assumption was in the case of a member's historical data entry missing the score attribute. In the context of this project, this means that we do not have data to check what the member's previous level was at a specific period in the timeline. To account for this, I made the assumption that the entry must either be dropped or we must replace the missing score with the member's current score. In either method of handling the missing data, the growth and churn rate would not be affected. I found this to be the safest way to handle null scores.

## Project Structure

`levels_full.py`
- This file simply builds the LevelsFull object and uses pprint for improved visualization of the data.
- The script also writes the output to the file `levels_full.txt` for even better viewing of the data.

`levels_full_debug.ipynb`
- This notebook file was used while debugging and testing runtimes for each portion of the script.
- Breaking the long LevelsFull building function into cells allowed me to fix errors within the function as well as improve upon the data manipulation methods to decrease runtime as much as possible.
- At first, data processing and manipulation was taking minutes, but breaking it down into cells helped me engineer the script to run in seconds.

## How to Run
```bash
cd analytics\part1
python levels_full.py
```
