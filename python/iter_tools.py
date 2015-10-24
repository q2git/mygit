from random import Random
import time
import itertools

chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    
def random_str(randomlength=8):
    str = ''
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
    
#itertools.combinations
#itertools.combinations_with_replacement
for i in itertools.combinations(chars,6):
    time.sleep(0.3)
    print ''.join(i)