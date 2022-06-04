# subscanner
A python script that I wrote to extract a subtitle image for a given set of input. It requires opencv and numpy to operate. It operates mainly by utilizing fourier transformation to detect certain traits of a subtitle inserted into an image. 

# how to use
To do a test run, open command shell with working directory set to the main subscanner directory, and type,


python src/subscanner.py "samples" "out" -clean


This will execute the subtitle scanner for every files contained within the samples directory and place the output in the out directory. -clean option will ensure that the destination will be first cleaned.

More generally, the command should take the following form


;script execution; ;source; ;destination; ;option;
  

;script execution; would be self-explanatory. Call the script however you see fit.

;source; should contain the path to the source file(s). It can point to either a file, or a set of files using star asterik(*), or a directory. If it is pointing to a directory or a set of files, then ;destination; must be a directory. If it is pointing to a directory, then every file within it will be processed.

;destination; should contain the path to the destination file(s). It can point to either a file, or a directory. If it is pointing to a directory, then 

;source; must be either a directory or a set of files. If it is a directory, then the outputs will be placed within it while retaining the same name as its corresponding source.

;option; is optional, and can be skipped. Currently, there is only one option, -clean , which cleans the destination directory before outputs are placed within it.

# caveats
If a source image does not contain any subtitles, then some messages will be printed onto stdout and its modified spectrum will be outputted instead.
