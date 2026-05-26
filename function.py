# def log(message: str):
#     print(message)

# def log_error(message: str):
#     print('eror: ', message)

# def log_warning(message: str):
#     print('warning: ', message)

# log('Hello, world')
# log_error('Something went wrong')
# log_warning('This is a warning')

def wrapper_error(func):
    def wrapper(meeage: str):
        print('error!')
        func(meeage)
    return wrapper

# new_log_error = wrapper_error(log)

# new_log_error('Hello, world')
@wrapper_error
def new_log_error(message: str):
    print(message)


new_log_error('Hello, world')