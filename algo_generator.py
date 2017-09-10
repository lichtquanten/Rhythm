from shutil import copyfile
import pickle
import sys

def generate_algorithm(algos):
    copyfile('pristine_algorithm.py', 'temp.py')
    sys.stdout = open('temp.py', 'a')

    print("algos = ", end='')
    print(algos)
    sys.stdout.close()
    f = open('temp.py', 'r')
    lines= f.readlines()
    lines.insert(13, lines[-1])
    lines = lines[:-1]
    thefile = open('algorithm.py', 'w')
    for line in lines:
        thefile.write("%s" % line)

if __name__ == "__main__":
    algos = [
        {
            'action': {
                'ticker': 'AMZN',
                'amount': 2,
                'amount_unit': 'shares',
                'position': 'long'
            },
            'condition': {
                'type': 'stocky',
                'logic': [
                    {'ticker': 'AMZN', 'field': 'close_price', 'threshold': 0.02, 'threshold_type': 'percentage'},
                    'or',
                    {'ticker': 'AMZN', 'field': 'open', 'threshold': 500, 'threshold_type': 'dollars'}
                ]
            }
        }]
    generate_algorithm(algos)
