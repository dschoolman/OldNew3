# List the oldest and newest files in a directory tree
# 9/7/2016 Modified for python 3. Changed print statements, exceptions
# todo
# allow exclusion of directory path segment such as Chrome\User Data
# see if we can get a better exception message with more detail for I/O exception



import sys
import getopt
import time
import os

# Parameters:
# --r, --root   root of directory tree root
# --n, --num    number of oldest and newest to list
# --e, --excl   exclude suffices
# --x, --xdir  exclude directories

# todo - Improve formatting of exclusion(s) in output reporting.
# todo - Make exclusions case insensitive
# todo - check for exception if parameter is entered as -x
# todo - allow only new files or only old files
# 2013/02/20 - allow for the exclusion of specific directories.Can only use the directory name, not a path

def usage():
    print ('\nUsage: LON.py --root,--r Top of directory tree --n,--num Number of files to list\n--e, --excl Exclude suffixes  --x, --xdir Exclude directories')
    print ('     example:  LON.py  --root e:\  --num 10 --e ".lib, .exp"')

# defaults
num  = 10
root = 'default'
exclude = ()    # create an empty tuple
exdir   = ()    # create an empty tuple for directories

filelist = []           # List of all files with their date
listcount = 0           # Number of files in tree
    
# print ('Arguments:', sys.argv)

letterParams = ['r', 'n', 'e', 'x']
keywordParameters = ['root=', 'num=', 'excl=', 'xdir=']

try:
    opts, extraparams = getopt.getopt(sys.argv[1:], letterParams, keywordParameters)
#except getopt.GetoptError, e:
except getopt.GetoptError as e:
    print ('\nError in command line parameters (%s)' % (e.msg))
    usage()
    sys.exit(2)

for o,p in opts:
  if o in ['--root', '--r']:
    root = p

  if o in ['--num', '--n']:
      if p.isdigit() == False:
          print ('<', p, '> is not a valid number')
          sys.exit(4)
      num = p

  if o in ['--excl', '--e']:
      low = p.lower()
      exclude = tuple(low.split(','))

  if o in ['--xdir', '--x']:
#      low = p.lower()
#      low = p.lower()
      exdir = tuple(p.split(','))
    

if root == 'default':
    print ('No tree entered')
    usage()
    sys.exit()

if os.path.exists( root ) == 0:
    print ('Root <', root, '> does not exist')
    sys.exit(3)


      
print (' ')
print ('-' * 75)
print ("  Oldest and Newest %s Files in <%s> Directory Tree" % (num, root))
if len(exclude) > 0:
        print ("  Excluding files with suffices", exclude)

if len(exdir) > 0:
        print ("  Excluding directories", exdir)
   
for rootfolder, dirs, files in os.walk(root, topdown=True):  

    temp_list = []                
    for dir in dirs:
#        if dir == 'AVG2013':
#           (print 'found dir AVG2013 in:', dirs, '  rootfolder:', rootfolder)
#        if dir == 'AVG Secure Search':
#           (print 'found dir AVG Secure Search in:', dirs, '  rootfolder:', rootfolder)
           
        if dir in exdir:
           # this may mess up the dirs. So I will just store the dir and delete after 
           # dirs.remove(dir)
           temp_list.append(dir)
#           print ('Saving dir: ', dir, ' from rootfolder:', rootfolder, ' dirs:', dirs)

    for d in temp_list:
#        print ('Removing dir: ', d, ' from rootfolder:', rootfolder, ' dirs:', dirs)
        dirs.remove(d)

    for filename in files:

        if (len(exclude) == 0) or (len(exclude) > 0 and filename.lower().endswith(exclude) == False):

                
                fullpath = os.path.join( rootfolder, filename)

                # retrieves the stats for the current file as a tuple
                # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)  
                # the tuple element mtime at index 8 is the last-modified-date
                #2/24/2010 - Added exception handler. Got WindowsError 206 on very long path name
                try:
                    stats = os.stat(fullpath)
                #except IOError as (errno, strerror):
                except IOError:
                    print ("I/O error - path %s"  % (fullpath))
                except WindowsError:
                    print ("Windows error - path %s" % (fullpath))

                # create tuple (year yyyy, month(1-12), day(1-31), hour(0-23), minute(0-59), second(0-59),
                # weekday(0-6, 0 is monday), Julian day(1-366), daylight flag(-1,0 or 1)) from seconds since epoch
                # note: this tuple can be sorted properly by date and time
                lastmod_date = time.localtime(stats[8])

                # create list of tuples ready for sorting by date
                date_file_tuple = lastmod_date, fullpath
                filelist.append(date_file_tuple)
                listcount = listcount + 1

if listcount == 0:
    print ('No files in tree')
    sys.exit(5)    

filelist.sort()
outcount = 0

# determine the length of the longest filename
longest = 0
for f in filelist:
    outcount = outcount +1
    if outcount <= int(num):
        if len(f[1]) > longest:
            longest = len(f[1])      

outcount = 0
print ("-" * 75)
print ("-" * 75)
print ("                       Oldest files")
print ("%s %s" % ("Filename".ljust(longest), "Last Modified"))
print ("-" * (longest + 18))
print ("-" * (longest + 18))
for fileentry in filelist:
    outcount = outcount +1
    if outcount <= int(num):
        #
        # convert date tuple to MM/DD/YYYY HH:MM:SS format
        #
        file_date = time.strftime("%m/%d/%y %H:%M:%S", fileentry[0])
        print ("%s %s" % (fileentry[1].ljust(longest), file_date))

print ("-" * (longest + 18))
print ("-" * (longest + 18))

filelist.reverse()
outcount = 0

# determine the length of the longest file
longest = 0
for f in filelist:
    outcount = outcount +1
    if outcount <= int(num):
        if len(f[1]) > longest:
            longest = len(f[1])      

outcount = 0

print ("                       Newest files")
print ("%s %s" % ("Filename".ljust(longest), "Last Modified"))
print ("-" * (longest + 18))
for fileentry in filelist:
    outcount = outcount +1
    if outcount <= int(num):
        #
        # convert date tuple to MM/DD/YYYY HH:MM:SS format
        #
        file_date = time.strftime("%m/%d/%y %H:%M:%S", fileentry[0])
        print ("%s %s" % (fileentry[1].ljust(longest), file_date))
