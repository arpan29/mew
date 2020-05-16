import sys
from pylint import lint

THRESHOLD = 9

args = []
args.append("--output-format=colorized")
args.append("--load-plugins=pylint_django")
args.append(sys.argv[1])
run = lint.Run(args, do_exit=True)
score = run.linter.stats['global_note']

if score < THRESHOLD:
    print("The code score is below the threshold. Please fix the issues and re-build.")
    sys.exit(1)
