import sys

if len(sys.argv) >= 2:
    arg = int(sys.argv[1])
    print('Argument ' + str(sys.argv[1]) + ' was provided.')
else:
    print('No arguments given.')
