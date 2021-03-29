# Project Name: Identical
## This project was an assignment of CMPE 230 course @ Boğaziçi University (Spring 2020 semester).
The project consists of a single Python program that detects and lists files and directories that are identical with respect to name and/or content.

### Execution on Command Line
```identic [-f | -d ] [-c] [-n] [-s] [< dir > ...]```

### Output
Full paths of identical files/directories are printed in blocks.

### Description of the arguments
| Argument | Description |
|:------:|:-----:|
|[`-f` \| `-d` ]|These arguments are mutually exclusive. If `-f` is given, the program looks for identical files and if `-d` is given, the program looks for identical directories.|
|`-c`|If `-c` is given, the program looks for identical files with respect to the content.<sup>*</sup>|
|`-n`|If `-n` is given, the program looks for identical files with respect to the name.|
|`-s`|If `-s` is given, the program prints the sizes of each duplicate along with their paths. This argument is ignored if `-n` is given.|
| < dir > |This argument stands for the directories to traverse. Traversing progresses in depth-first fashion, i.e. if a directory is being traversed, all of its subdirectories must have already been traversed. As seen above, there can be multiple directories given as argument and if none given, current directory is the default.|

<sup>*</sup>: If `-d` is given with `-c`, in order for two directories to be identical, the contents of all of the subdirectories of these directories must also be identical.
