```pytho
class typing.Generator(Iterator[T_co], Generic[T_co, T_contra, V_co])
Generator[YieldType, SendType, ReturnType]
def echo_round() -> Generator[int, float, str]:
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return 'Done'
    
l = [x for x in range(10)] # []生成的是列表
g = (x for x in range(10)) # ()生成的是生成器
```

