# Working with tabular data in Python

> Note: this document is being revised

* [Binary and text files](TabularData.md#binary-and-text-files)
* [Tabular data](TabularData.md#tabular-data)
* [Functions](TabularData.md#intermission---working-with-python-functions)
* [for loops](TabularData.md#for-loops)
* [String indexing and manipulation](TabularData.md#back-to-our-file---working-with-strings)


## Binary and text files
First, let's draw a distinction between plain text and binary files.  All files correspond to a series of 1's and 0's on the hard drive or in memory.  A plain text file has a flag that tells the computer that it should apply a [character encoding](https://en.wikipedia.org/wiki/Character_encoding) that maps binary sequences (bit strings) to symbols, such as characters in an alphabet.  For example, the [ASCII](https://en.wikipedia.org/wiki/ASCII) encoding maps the bit string `1001010` to the letter `J`.  This means that when you open the file, the computer knows that it should display its contents as a collection of meaningful characters.  Obviously this is a big advantage for making a file immediately interpretable.  However, we sacrifice some efficiency to make this possible, so binary files tend to be more compact while storing the same information. 

For a plain text file, a format is a set of rules about how the characters are arranged to encode information.  Data formats are a necessary evil in bioinformatics.  Learning to parse new formats and converting between formats is a ubiquitous task that is often made more difficult by the lack of a strict standardization for popular formats such as [NEXUS](https://en.wikipedia.org/wiki/Nexus_file) or [Newick](https://en.wikipedia.org/wiki/Newick_format).  Fortunately, the pervasiveness of such tasks means that there are also plenty of resources in the public domain that make them easier to accomplish.

![](https://imgs.xkcd.com/comics/binary_heart.jpg)

## Tabular data

Tabular data formats are probably the most common format for storing conventional data types.  A table is made up of rows and columns like a [spreadsheet](https://en.wikipedia.org/wiki/Spreadsheet).  Table rows (by convention) represent independent observations/records, such as a sample of patients, and columns represent different kinds of measurements (variables) such as height and weight.  For example:

|agegp |alcgp  |tobgp    | ncases| ncontrols|
|:-----|:------|:--------|------:|---------:|
|75+   |40-79  |0-9g/day |      2|         5|
|75+   |40-79  |10-19    |      1|         3|
|35-44 |80-119 |10-19    |      0|         6|
|65-74 |80-119 |10-19    |      4|        12|
|55-64 |40-79  |30+      |      3|         6|
|45-54 |120+   |10-19    |      3|         4|
|55-64 |120+   |20-29    |      2|         3|
|25-34 |80-119 |30+      |      0|         2|
|55-64 |40-79  |20-29    |      4|        17|
|55-64 |80-119 |10-19    |      8|        15|

These data come from the `esoph` dataset in [R](https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/00Index.html). For what it's worth, to extract this subsample I used the following command in R:
```R
kable(esoph[sample(1:nrow(esoph), 10),], format='markdown', row.names=F)
```
These are aggregate data from a case-control study of esophageal cancer in France.  If you're interested about the study, you can read more about it in the source reference: [Brewlow and Day 1980](https://www.iarc.fr/en/publications/pdfs-online/stat/sp32/).  

How do we record this information in a plain text file?  Typically, we preserve the row structure of the table by placing line breaks between each row.  A [line break](https://en.wikipedia.org/wiki/Newline) is a special character encoding that tells the computer to move to a new line when displaying the content of a text file.  Different operating systems use [different control characters](https://en.wikipedia.org/wiki/Newline#Representations) in the ASCII encoding set to represent a line break: UNIX and its descendants use `LF` (line feed); Apple computers used `CR` (carriage return) until the OS became a UNIX-like system; and Microsoft Windows uses a combination of `LF` and `CR`.  This frequently causes problems when passing data files originating from different computers between programs that were developed on different platforms!  If you are trying to process a data file with a program and it isn't working, this is a possible cause.

We still have to deal with preserving the column structure of a tabular data set.  This is usually accomplished with a [delimiter](https://en.wikipedia.org/wiki/Delimiter): a character or sequence of characters that is used to separate content that belongs to different items.  The comma `,` is probably the most common delimiter, closely followed (if not surpassed) by the [tab character](https://en.wikipedia.org/wiki/Tab_key#Tab_characters), which is represented by the escape character `\t`.  To illustrate, here is how our `esoph` data would appear in a comma-separated values (CSV) file:
```
agegp,alcgp,tobgp,ncases,ncontrols
75+,40-79,0-9g/day,2,5
75+,40-79,10-19,1,3
35-44,80-119,10-19,0,6
65-74,80-119,10-19,4,12
55-64,40-79,30+,3,6
45-54,120+,10-19,3,4
55-64,120+,20-29,2,3
25-34,80-119,30+,0,2
55-64,40-79,20-29,4,17
55-64,80-119,10-19,8,15
```

and here is the same data set as a tab-separated values (TSV) file:
```
agegp	alcgp	tobgp	ncases	ncontrols
75+	40-79	0-9g/day	2	5
75+	40-79	10-19	1	3
35-44	80-119	10-19	0	6
65-74	80-119	10-19	4	12
55-64	40-79	30+	3	6
45-54	120+	10-19	3	4
55-64	120+	20-29	2	3
25-34	80-119	30+	0	2
55-64	40-79	20-29	4	17
55-64	80-119	10-19	8	15
```

An important feature of these formats is that the first line is being used to store the column labels.  This is often referred to as the *header row*.  Including the header row is optional in a CSV or TSV file, but it is important to be aware of whether it is present or absent when you are processing the file.  

A tabular data file should have the same number of items on each line.  If a line has more items than another, then the assignment of items to the various columns becomes ambiguous (especially if the data are similar types, such as a large set of numbers).  In other words, did we append an extra number to the left, or the right, or some where in the middle?  

What happens if our data includes entries that contain the delimiter?  For example, suppose that our data set includes text fields that contain a description of symptoms, such as: `muscular pain, acute`.  This creates the exact problem that we just described!  Fortunately, this format is so widely used, and this problem so common, that there is a standardized solution: we enclose the affected item in double quotes.  In other words, this row:
```
67,muscular pain, acute,Toronto
```
becomes this:
```
67,"muscular pain, acute",Toronto
```

One last thing.  There are several reasons why tabular data formats are not the most convenient choice for other types of data, or for many situations.  One of these situations is when you want to write some additional information about the content of the table in the file.  For example, suppose that we wanted to properly credit the authors of the study that these data came from.  We can't append lines to this table that contain a reference to the literature without breaking up the tabular data scheme and causing problems when we want to parse the data.  One solution to this problem is to reserve a special character to indicate that lines beginning with that character are comments and should be ignored.  There is no standard practice for commenting CSV files.  However, I have frequently seen the `#` character used for this purpose.

![](https://imgs.xkcd.com/comics/file_extensions.png)



## Working with tabular data files in Python

Okay, let's use `cd` and `ls` to navigate to the `examples` folder.  I've placed a CSV file derived from the `esoph` R data set, which I've uncreatively named `esoph.csv`:
```shell
[Elzar:~/git/courses] artpoon% pwd
/Users/artpoon/git/courses
[Elzar:~/git/courses] artpoon% cd GradPythonCourse/
[Elzar:~/git/courses/GradPythonCourse] artpoon% cd examples/
[Elzar:courses/GradPythonCourse/examples] artpoon% ls
esoph.csv
```

Use the `head` command to have a quick look at the contents of this file:
```
[Elzar:courses/GradPythonCourse/examples] artpoon% head -n5 esoph.csv 
agegp,alcgp,tobgp,ncases,ncontrols
25-34,0-39g/day,0-9g/day,0,40
25-34,0-39g/day,10-19,0,10
25-34,0-39g/day,20-29,0,6
25-34,0-39g/day,30+,0,5
```

Now let's fire up an interactive session with Python.  
```shell
[Elzar:courses/GradPythonCourse/examples] artpoon% python
Python 3.6.0b3 (default, Nov  1 2016, 16:08:38) 
[GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

The first thing we need to do is to open the file.  This is accomplished with the built-in Python function `open`:
```python
>>> handle = open('esoph.csv', 'rU')
```
Before we talk about what's happening here, we need to talk a bit about functions and variables.


### Intermission - working with Python functions
Since this may be the first time you've encountered a function call in Python (or even in any programming language!), I need to take a minute to explain some basic concepts.  A function is a set of instructions in the programming language that we've asked the computer to set aside and label with a name.  Whenever we call that name, the computer will know to run that set of instructions.  Functions become really useful if you can apply the same set of instructions to different things.  We pass those things to a function as "arguments".  There are two arguments being passed to the `open` function in this example:
1. `'esoph.csv'` is a string (sequence of characters) that corresponds to a relative path to the file.  Since we initiated our Python session in the same directory as the file, we don't need to specify any other directories.
2. `'rU'` is another string that tells Python to open the file in "read-only" mode (`r`) and to interpret the stream of ones and zeros being transmitted from the file with a Unicode encoding `U`.  
How are we supposed to know what arguments to pass to a function?  You need to use another built-in Python function called `help`:
```python
help(open)
```

This spawns another interactive shell for viewing the help documentation for the `open` function:
```shell
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
    Open file and return a stream.  Raise IOError upon failure.
```
There's actually many more lines than this!  This shell works the same way as `less` and `man`: you can scroll up and down with the arrow keys, and return to your Python session at any time by typing `q`.  The first line of the help document provides some concise information about how to use the function (to get more detailed information, keep reading!).  There are 8 different arguments that can be passed to the `open` function.  There is only 1 argument that doesn't have a default value: `file`.  That is what we use to specify an absolute or relative path to the file that we want to open a stream from. The `mode` argument is the only one that I've ever used in practice.  Note that it defaults to a read-only mode (`r`).  This is good behaviour - if it defaulted to a write mode (`w`), then you'd wiped out every file you tried to open! 

### Another intermission - Variables
Functions usually have *return values* --- they pass something back to you when they've completed their task.  You need to capture this return value by assigning it to a variable. 

When a function returns a value, you need to assign this value to a variable.  When there are multiple return values, you can provide an equal number of variables to assign them to.  Otherwise, they will be assigned to a single variable as a collection of objects such as a [tuple](https://docs.python.org/2/tutorial/datastructures.html#tuples-and-sequences).


### Back to our regular programming

Okay, let's go back to this situation:
```python
>>> handle = open('esoph.csv', 'rU')
```
Calling the `open` function caused Python to open a stream to the file named `esoph.csv`.  Since this file is in the present working directory (typically where our shell was located in the file system when we triggered an interactive Python session), we don't have to specify an absolute or relative path to the file.  

Think of a stream as a binary sequence of ones and zeros that are being read off the storage device.  The stream always starts at the beginning of the file; it can't start somewhere in the middle.  By default, Python will interpret a file stream in read mode using the Unicode encoding.  Once you've moved forward in the stream, you can't easily go back.  It's possible, but it requires calling functions that we won't cover in this course.

What are we supposed to do with this file stream object?
```python
>>> handle
<_io.TextIOWrapper name='esoph.csv' mode='rU' encoding='UTF-8'>
```
That wasn't very informative, but worth a try!  If we really want to learn about what this kind of object can do, we can use the `help` function again - however, this is going to splash a lot more information than you probably want to digest at this point.  Let's introduce another helpful function (ha ha): `dir`.
```python
>>> dir(handle)
['_CHUNK_SIZE', '__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__lt__', '__ne__', '__new__', '__next__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_checkClosed', '_checkReadable', '_checkSeekable', '_checkWritable', '_finalizing', 'buffer', 'close', 'closed', 'detach', 'encoding', 'errors', 'fileno', 'flush', 'isatty', 'line_buffering', 'mode', 'name', 'newlines', 'read', 'readable', 'readline', 'readlines', 'seek', 'seekable', 'tell', 'truncate', 'writable', 'write', 'writelines']
```
This returns a list of all the possible functions associated with the kind of object that we've labelled `handle`.  The functions that have a name surrounded by double underscores (`__`) are attributes of the object that have standardized names.  For example, `__str__` is a function that determines what text will appear if you call the base function `print` on this object:
```python
>>> handle.__str__()
"<_io.TextIOWrapper name='DataFormats.md' mode='r' encoding='UTF-8'>"
```
Well, that's exactly what was returned to us when we entered the variable name `handle` by itself to print the value associated with this variable.  Don't worry about details of this output for now; I'm just using `__str__` as a convenient example.

Here are some of the more useful methods of file objects in read mode:
* `read` : This function returns the entire file stream as one long string
* `readlines` : This function cuts up the stream wherever it encounters a line break, and returns the resulting pieces as a list (a kind of Python object that we'll talk more about later).
* `readline` : Cuts the stream at the line breaks, but returns only one piece at a time.  The first time you call this function, you'll get the first line.  The second time returns the second line, and so on.
* `close` : When you're done with the file stream, it is good programming practice to clean up after yourself and close the stream.  

We're finally ready to do a little processing with our example file:
```python
>>> handle.readline()
'agegp,alcgp,tobgp,ncases,ncontrols\n'
>>> handle.readline()
'25-34,0-39g/day,0-9g/day,0,40\n'
>>> handle.readline()
'25-34,0-39g/day,10-19,0,10\n'
```
What's this `\n` thingy?  This is how line breaks are represented in UNIX.  The backslash character (`\`) has a special meaning in UNIX - it is known as an escape character that tells the computer to interpret the *next* character differently.  In this case, we want to tell the computer that this is not the letter `n`; it is a line break.

![](https://imgs.xkcd.com/comics/backslashes.png)

Well.  That's great, we can see the contents of the file, but it's flying off into the ether because we're not assigning it to a variable so we can do something with it.  Let's fix that:
```python
>>> line = handle.readline()
>>> line
'25-34,0-39g/day,20-29,0,6\n'
```
Now we've got a variable that we've named `line` that is holding onto the content of one of the lines in our file.  This is still not terribly useful, because there are still many lines in the file and I don't want to keep assigning those lines to this same variable.  I also don't want to come up with different variable names for every line, like this:
```
>>> line2 = handle.readline()
>>> line3 = handle.readline()
>>> another_line = handle.readline()
```
This is valid Python, but it's also stupid.  No, we're going to have to learn about `for` loops.


## for loops

Loops are a fundamental concept in programming where we instruct the computer to follow the same set of instructions a specific number of times, or forever until some condition is met.  A `for` loop in Python looks like this:
```python
>>> for i in range(3):
...     print('Underpants!')
... 
Underpants!
Underpants!
Underpants!
```
(This sort of thing really is how many of us got started with programming in the 80's.)  

What's going on here?  First of all, a `for` statement has three basic parts:
1. An iterable object that we're looping over.
  In this example, `range` is a built-in function that returns a sequence of integers that starts with `0` and ends with one less than the integer argument.  In Python 3, you can't see this sequence even if you specifically ask for it.  This is because Python 3 is returning a function that will generator this sequence as numbers when you ask for them; this is more efficient than storing the entire sequence in memory.  I'm still getting used to this -- in Python 2, everything was immediately available to look at.
  ```python
  >>> range(3)
  range(0, 3)
  >>> thing = range(3)
  >>> list(thing)
  [0, 1, 2]
  ```

2. One or more variables for capturing the values being passed from the iterable object.  
  In our example, there's only one integer being passed at a time, so we only need one variable: `i`.  In our first pass through the loop, `i` has the value `0`.  On our second pass, it has the value `1`.  To illustrate:
  ```python
  >>> for i in range(3):
  ...   print(i)
  ... 
  0
  1
  2
  ```
  
3. A code block that is going to be executed every time we pass through the loop.
  This is where we have to get into another basic concept in Python.  A [code block](https://en.wikipedia.org/wiki/Block_(programming)) is a subset of instructions that we want to differentiate from the rest of the instructions.  When we write a `for` loop, for example, we usually don't want Python to execute the entire script multiple times.  A programming language needs to have some means of telling the computer which instructions are in the code block, and which ones are not.  Some languages enclose the code block in a special character.  For example, `C` uses curly brackets (`{` and `}`).  Python uses whitespace: a series of one or more spaces or tabs.  It's one of the defining (but not unique) characteristics of the language. 
  For example, deleting the spaces to the left of the `print` function in the previous example raises an error:
  ```
  >>> for i in range(3):
... print(i)
  File "<stdin>", line 2
    print(i)
        ^
IndentationError: expected an indented block
  ```
  All lines that begin with the same whitespace that come immediately after the `for` statement are included in the code block.  The next line to start with different whitespace closes the code block.  For example, this script:
  ```python
  for i in range(3):
    print(i)
  print('now stop')
  ```
  produces the following output:
  ```shell
  [Elzar:courses/GradPythonCourse/examples] artpoon% python foo.py
  0
  1
  2
  now stop
  ```
  Caveat: this example will raise a syntax error in interactive mode.  It's just [one of those quirks](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode) of the interactive mode.
  
![](https://imgs.xkcd.com/comics/ducklings.png)


## Back to our file - working with strings

Now that we know a little bit about `for` loops, let's apply it to our code:
```
>>> for line in handle.readlines():
...     print(line)
... 
25-34,40-79,20-29,0,4

25-34,40-79,30+,0,7

25-34,80-119,0-9g/day,0,2
```
and much more!  There's a couple of things to note here.  First, the lines being printed don't start at the top of our file because we've already called the `readline()` function a few times, so we've already moved through the file stream.  Second, the output is skipping every other line because each string returned by `readlines()` keeps the line break at the end.  Third, this still isn't very useful code - we could have accomplished the same thing with a `cat` statement.  No, for our script to start getting useful, we have to learn about string manipulation, and in order to do *that*, we have to learn about indexing and immutables.

### Indexing

 
### Getting back to tabular data

Hopefully you'll have noticed that some (if not all) of the string functions that we just reviewed are really useful for working with tabular data sets.  Let's open a file handle to our example plain-text file again:
```python
handle = open('esoph.csv', 'rU')  # let's use Unicode encoding
```
We know that our file contains a header line, so we need to skip it before we process the rest of the data file.  We can do this with the following line:
```python
_ = handle.nextline()  # skip header line
```
In Python 2, I used to be able to use a different function called `next`, but `nextline` pretty much serves the same role: it tells our file object to return the current line and advance to the next line in the file stream.  Since I'm not interested in doing anything with this line, I'm assigning it to a dummy variable as indicated with a single underscore (`_`) --- a totally valid and utterly uninformative variable name!  

Now it's time to iterate through the rest of the file and do something with the information contained within.  We're going to work with prior knowledge about the content of the file - namely, that each row contains the following information:
 * age group
 * alcohol consumption category
 * tobacco consumption category
 * number of cases of esophageal cancer
 * number of controls

Here is a script that will do the following things:
 1. Replace the age group notation with the lower age limit.
 2. Replace 'g' with 'mL' in alcohol consumption units.
 3. Replace the case and control counts with proportion and sample size.
 4. Print each line to the console so we can stream it into another file in a tab-separated format.
 
Here's the entire script:
```python
handle = open('esoph.csv', 'rU')
_ = handle.readline()  # skip header line

for line in handle:
    # remove the line break character and split into substrings at commas
    agegp, alcgp, tobgp, cases, controls = line.strip('\n').split(',')
    min_age = agegp.split('-')[0].strip('+')  # extract first part of XX-YY and remove trailing plus sign
    alcvol = alcgp.replace('g', 'mL')  # alcohol consumption volume
    
    # calculate sample size and case proportion
    sampsize = int(cases) + int(controls)  # convert strings to integers
    propn = float(cases) / sampsize  # a floating point number has a decimal
    
    # write out to console as a tab-separated line
    print ('\t'.join([min_age, alcvol, tobgp, str(propn), str(sampsize)]))

handle.close()  # finished with the file
```

I've cluttered this example script a bit with some documentation, because I want you to get used to the idea of always providing documentation with your code.  This is as much for your own benefit as it is for anyone else who might read your code.  Think of it as doing a big favour for your future self, who has completely forgotten why you wrote this script and how it is supposed to work!

To understand what this script is doing, I find it helpful to extract one line from the file and manually run through the commands being applied to it.  Instead of entering a `for` loop, let's grab one line with `readline`:
```python
>>> line = handle.readline()  # called a second time (after popping off the header)
>>> line
'25-34,0-39g/day,0-9g/day,0,40\n'
>>> line.strip('\n')
'25-34,0-39g/day,0-9g/day,0,40'
>>> line.strip('\n').split(',')
['25-34', '0-39g/day', '0-9g/day', '0', '40']
```
And so on.  Interactively poke and prod at every operation being performed on this line.  What happens if you don't enclose `cases` and `controls` with `int()` functions?  How about if you try to compute the proportion with `int(cases)/sampsize`?

