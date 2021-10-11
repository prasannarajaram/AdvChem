import itertools, sys
spinner = itertools.cycle(['-', '/', '|', '\\'])
while True:
    sys.stdout.write(next(spinner))   # write the next character
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')            # erase the last written char
