from bbfreeze import Freezer
f = Freezer("Commons Graph")
f.addScript("commonsgraph.py")
f.addScript("tktest.py")
f()    # starts the freezing process
