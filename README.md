# subscanner
subscanner is a python script for extracting a subtitle image from a given set of inputs. It requires opencv and numpy to operate. It operates mainly by utilizing fourier transformation to detect certain traits of a subtitle inserted into an image. 

# how to use
To do a test run, open command shell with working directory set to the main subscanner directory, and type,


python src/subscanner.py "samples" "out" --clean --test


This will execute the subtitle scanner for every files contained within the samples directory and place the output in the out directory. -clean option will ensure that the destination will be first cleaned.

More generally, the command should take the following form


;script execution; ;source; ;destination; ;options;
  

;script execution; would be self-explanatory. Call the script however you see fit.

;source; should contain the path to the source file(s). It can point to either a file, or a set of files using star asterik(*), or a directory. If it is pointing to a directory or a set of files, then ;destination; must be a directory. If it is pointing to a directory, then every file within it will be processed.

;destination; should contain the path to the destination file(s). It can point to either a file, or a directory. If it is pointing to a directory, then 

;source; must be either a directory or a set of files. If it is a directory, then the outputs will be placed within it while retaining the same name as its corresponding source.

;options; is optional, and can be skipped. You can enable any combination of options that you'd like. Currently, list of possible options is as follows.

| option | explanation |
| --- | --- |
| --clean | Cleans the destination directory before outputs are placed within it. Does nothing if destination is not a directory. |
| --test | Print intermediate datas that are generated while subscanner is being run. Currently, the following outputs will be printed.  |

| output | explanation |
| --- | --- |
| _1r1original | Original source image. |
| _1r2spectrum | Initial spectrum image that was converted from source. Row-wise. |
| _1r3processed | Spectrum image that has gone through multiple processing operations. Row-wise. |
| _1r4binary | Binary image that was processed through Otsu's method from _1r3processed. Row-wise. |
| _2c1original | A section in source image. |
| _2c2spectrum | Spectrum image that was converted from a section in source. Column-wise. |
| _2c3processed | Spectrum image that has gone through multiple processing operations. Column-wise. |
| _2c4binary | Binary image that was processed through Otsu's method from _2c2processed. Column-wise. |
| _3out | Output image. |  

# caveats
If a source image does not contain any subtitles, then no further operations will be made.
