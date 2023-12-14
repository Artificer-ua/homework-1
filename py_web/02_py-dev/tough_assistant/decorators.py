

def input_error(func):

    def wrapper(*args, **kwargs):
        
        try:
            return func(*args, **kwargs)

        except TypeError as e:
            return e
                    
        except KeyError as e:
            return e
        
        except ValueError as e:
            return e
        
    return wrapper


if __name__ == "__main__":
    print("Module Decorators")
