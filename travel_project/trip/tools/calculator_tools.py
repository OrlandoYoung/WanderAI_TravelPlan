# tools/calculator_tools.py

from crewai.tools import BaseTool

class CalculatorTool(BaseTool):
    name: str = "calculate"
    description: str = "执行各种预算、定价和费用计算"

    def _run(self, expression: str) -> str:
        """
        接受一个数学表达式字符串，返回计算结果。
        """
        try:
            result = eval(expression, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"计算时出错：{e}"

    async def _arun(self, expression: str) -> str:
        # 如果不需要异步，可以直接复用同步逻辑
        return self._run(expression)