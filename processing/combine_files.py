import os
import re

## list directory, pair similar files to combine
source_dir = '/home/spencer/Documents/welch-bible-lessons'
target_dir = './data/lessons'
files = [(re.sub('-\d\.txt', '', x),x) for x in os.listdir(source_dir) if '.txt' in x]

file_groups = {}
for group, file in files:
    if not file_groups.get(group):
        file_groups[group] = []
    
    file_groups[group] += [file]

# combine files
for k, v in file_groups.items():

    grouped_file_path = os.path.join(target_dir, f'{k}.txt')
    grouped_file = open(grouped_file_path, 'w')
    
    v.sort()
    for f in v:
        file_path = os.path.join(source_dir, f)
        with open(file_path, 'r') as p:
            grouped_file.write(p.read())

    grouped_file.close()
