def initialise():
  from aiko.common import log
  from configuration.main import parameter
  import os, sys

  for basename in os.listdir(__path__):
    pathname = "/".join([__path__, basename])
    if pathname == __file__:
      continue
    s_ifmt = os.stat(pathname)[0] & 61440
    if basename[-3:] == ".py" and s_ifmt == 32768:
      submodule = basename[:-3]
    elif s_ifmt == 16384:
      submodule = basename
    assert submodule not in locals()
    if parameter("plugin_{}_disabled".format(submodule)):
      continue
    try:
      module = ".".join([__name__, submodule])
      __import__(module, globals(), locals(), [module]).initialise()
      log("plugin: {}".format(submodule))
    except Exception as err:
      sys.print_exception(err, sys.stderr)
