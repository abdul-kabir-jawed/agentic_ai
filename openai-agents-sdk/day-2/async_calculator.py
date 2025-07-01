import asyncio

class AsyncCalculator():
    def __init__(self,name: str):
        self.name=name

    async def addition(self, a:int, b:int )->int:
        """Add two numbers."""
        await asyncio.sleep(5)
        return a+b

    async def subtract(self, a:int, b:int )->int:
        """Subtract two numbers."""
        await asyncio.sleep(5)
        return a-b

    async def divide(self, a:int, b:int )->float:
        """Divivde two numbers."""
        await asyncio.sleep(6)
        return a/b

    async def multiply(self, a:int, b:int )->int:
        """Multiply two numbers."""
        await asyncio.sleep(7)
        return a*b
    
    async def reverse_string(self, text:str )->str:
        """Reverse a string."""
        await asyncio.sleep(8)
        return text[::-1]
    

async def main():
    calc=AsyncCalculator("calc")
    divide_num= calc.divide(25,6)
    reverse= calc.reverse_string("hello")
    divide_num,reverse=await asyncio.gather(divide_num,reverse)
    print(divide_num, reverse)


async def waiting():
    task=asyncio.create_task(main())
    done,pending=await asyncio.wait({task},timeout=10)
    for p in pending:
        print("some task not complete in time")
        p.cancel()

    
asyncio.run(waiting())
