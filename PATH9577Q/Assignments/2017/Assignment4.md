# Assignment 4
Submit your results by modifying this Markdown and e-mailing the plain text file to my address.

1. Write a glob expression to capture the following files:
   ```shell
   ape-raw.tsv    conifer-raw.tsv    tardigrade-raw2.tsv
   ```
   but exclude the following files:
   ```shell
   ape-raw.csv    tardigrade-processed.tsv    ape-rejected.tsv
   ```
   
   ```shell
   # write your answer here
   ```

2. Modify the following Python script to be called from the command line for any input file:
   ```python
   def main(path):
       handle = open(path, 'rU')
       headers = []
       counter = 0
       outfile = None
       for line in handle:
           if line.startswith('@'):
               headers.append(line)
               continue
           if counter % 10 == 0:
               if outfile:
                   outfile.close()
               # open new file
               outfile = open('slice{}.sam'.format(counter), 'w')
               for header in headers:
                   outfile.write(header)
           outfile.write(line)
           counter += 1
       outfile.close()
           
   main('input.sam')
   ```
   Save your script to a file in the `examples` folder and run it on the `SRR5261740.trunc.sam` file.  What does this script do?  Answer in the following space
   ```
   
   
   ```
   
3. Write a Python wrapper function for [samtools](https://github.com/samtools/samtools/releases), using the `subprocess` module to call the command `samtools view -bS TEMP.sam > TEMP.bam`, where `TEMP.*` should be replaced by filenames based on a command-line argument.  Hint: to redirect the stdout stream to a file, you need to open a file in Python and pass that file handle to the `stdout` keyword argument in a `subprocess` function.  

   Work with the following template:
   ```python
   import sys
   def bam2sam(path):
       bamfile = ''  # need to set this to something based on `path` argument
       handle = open(bamfile, 'w')
       subprocess.check_call([''], stdout=handle)  # need to populate first list argument with strings
       
   
   bam2sam()  # need to pass argument here
   ```

4. [BONUS] Modify your script from question (3) to use `glob` to apply the `bam2sam` function to the outputs generated by question (2).  Paste your script here:
   ```python
   
   ```
