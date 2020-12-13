# Reimplement, because CPython3.3 impl is rather bloated

import os

# https://github.com/python/cpython/blob/master/Lib/stat.py
#
# Indices for stat struct members in the tuple returned by os.stat()
ST_MODE  = 0
#   ST_INO   = 1
#   ST_DEV   = 2
#   ST_NLINK = 3
#   ST_UID   = 4
#   ST_GID   = 5
#   ST_SIZE  = 6
#   ST_ATIME = 7
#   ST_MTIME = 8
#   ST_CTIME = 9
#
# Constants used as S_IFMT() for various file types
S_IFDIR  = 0o040000  # directory
#   S_IFCHR  = 0o020000  # character device
#   S_IFBLK  = 0o060000  # block device
#   S_IFREG  = 0o100000  # regular file
#   S_IFIFO  = 0o010000  # fifo (named pipe)
#   S_IFLNK  = 0o120000  # symbolic link
#   S_IFSOCK = 0o140000  # socket file

def S_IFMT(mode):
  return mode & 0o170000

def S_ISDIR(mode):
  return S_IFMT(mode) == S_IFDIR

def file_copy(pathname_old, pathname_new):
  with open(pathname_new, "w") as file_new:
    with open(pathname_old, "r") as file_old:
      for line in file_old.readlines():
        file_new.write(line)

def isdir(pathname):
  try:
    mode = os.stat(pathname)[ST_MODE]
    return S_ISDIR(mode)
  except OSError:
    return False

def make_directories(pathname):
  directories = pathname.split('/')[:-1]
  if directories:
    for index in range(len(directories)):
      parent = '/'.join(directories[:index + 1])
      try:
        os.mkdir(parent)
      except OSError:
        pass

def path_list(pathname="."):
  path_traverse(pathname, print, print)

def path_remove(pathname):
  path_traverse(pathname, os.rmdir, os.remove)

def path_traverse(pathname, directory_handler=None, file_handler=None):
  try:
    if isdir(pathname):
      for file in os.listdir(pathname):
        filename = pathname + "/" + file
        path_traverse(filename, directory_handler, file_handler)
      if directory_handler:
        directory_handler(pathname)
    else:
      if file_handler:
        file_handler(pathname)
  except Exception:
    pass
