#Змінювати кожен ел-т результату ориг. ф-ї
def change_each(change):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            for i in f(*args, **kwargs):
                yield change(i)
        return wrapped
    return wrapper

@change_each(lambda x:x*x*x)
def myrange(n):
    return range(1, n+1)

print(list(myrange(10)))