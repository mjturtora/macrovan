from utils import *

print_list_name = 'H.E!L\L*O'
print_list_name = print_list_name.translate(print_list_name.maketrans('', '', '.!*\\'))
print(print_list_name)
