""""""
def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("---This parrot wouldn't", action, end=' ')
    print("if you put", voltage,"volts through it")
    print("---Lovely plumage, the", type)
    print("---It's", state, "!")


parrot(1000)
parrot(voltage=1000)
# parrot(voltage=1000, action='VOOOOM')
# parrot(action='VOOOOM', voltage=1000000000)
# parrot('a million', 'bereft of life', 'jump')
# parrot('a thousand', state='pushing up the daisies')


#invalid calls
parrot(voltage=5.0, 'dead')
parrot(110, voltage=220)
parrot(actor='John')
