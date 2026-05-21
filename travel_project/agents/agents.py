# agents.py

from crewai import Agent
from textwrap import dedent
import os
from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.outputs import ChatResult, ChatGeneration
import requests
from tools.search_tools import SearchInternetTool
from tools.calculator_tools import CalculatorTool
load_dotenv()
from pydantic import Field
import requests

class DeepSeekChat(BaseChatModel):
    api_key: str = Field(...)
    # model: str = Field(default="deepseek-chat")
    # api_base: str = Field(default="https://api.deepseek.com/v1/chat/completions")

    model: str = Field(default="gpt-4.1")
    api_base: str = Field(default="https://api.openai-proxy.org/v1")

    def _llm_type(self) -> str:
        return "deepseek"
    # 消息格式转换
    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        payload_messages = []
        for msg in messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            payload_messages.append({"role": role, "content": msg.content})
        #构造 API 请求负载
        payload = {
            "model": self.model,
            "messages": payload_messages,
            "temperature": 0.5
        }
        #请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # 发送 POST 请求到 DeepSeek API
        response = requests.post(self.api_base, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"DeepSeek API Error: {response.status_code} - {response.text}")

        content = response.json()["choices"][0]["message"]["content"]
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=content))])



# ✅ Agents 包装类
class TravelAgents:
    def __init__(self):
        deepseek_key = os.getenv("OPENAI_API_KEY")
        self.llm = DeepSeekChat(api_key=deepseek_key)

        self.search_tool = SearchInternetTool()
        self.calc_tool = CalculatorTool()

    def Trip_Planner_Agent(self):
        return Agent(
            role="总体行程规划负责人",
            backstory=dedent(
                """
                您是一位经验丰富的旅行顾问，拥有数十年的定制行程设计经验。
                您擅长将复杂的旅行计划拆解成多个子任务，分配给专业的代理人，
                并将所有部分整合成一个协调一致的最终计划。
                """
            ),
            goal=dedent(
                """
                您的目标是为用户制定一份详细的端到端旅行行程，
                包括每天的行程安排、交通、住宿、活动、餐饮、天气准备、预算估算以及当地的见解。
                您需要收集用户的偏好，并将研究任务委托给专业代理人,
                然后将所有研究结果整合成一份Markdown文档，注意信息要详细一点并且尽可能美观地展示信息。
                **请以完整的 Markdown 文档格式输出最终行程（不要使用任何三引号或```代码块标记））**，并使用：
                - 一级（`#`）显示旅行标题
                - 二级（`##`）分节，如“旅行概览”、“交通安排”、“住宿推荐”等
                - 列表、表格或小结形式展示各部分内容
                内容要详实、逻辑清晰，美观易读。
                """
            ),
            tools=[],
            allow_delegation=False,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Destination_Research_Agent(self):
        return Agent(
            role="目的地研究专家",
            backstory=dedent(
                """
                您热衷于环球旅行，对世界各地都拥有百科全书般的知识，
                您知道如何发掘隐藏的宝藏、季节性活动、文化亮点，以及最新的景点和活动费用估算。
                """
            ),
            goal=dedent(
                """
                你需要调查并推荐用户旅行的理想目的地（注意要使用中文且美观的展示你获得的信息）
                **请以 Markdown 格式输出**：
                1. **必看景点**（列表）
                2. **小众体验**（列表）
                3. **当地节庆活动**（表格或列表）
                4. **典型花费**（表格：项目 | 费用）
                5. **最佳旅行季节/天气提示**（段落总结）
                要求排版整洁、层次分明。
                使用的参数：
                    目的地：{destination}
                    日期范围：{date_range}
                    人数：{num_people}
                """
            ),
            tools=[self.search_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Accommodation_Agent(self):
        return Agent(
            role="住宿资源专家",
            backstory=dedent(
                """
                您是全球提供住宿推荐的专家。
                您能够平衡舒适性、地理位置、用户预算，
                为用户推荐独特的当地住宿（例如精品酒店、家庭旅馆、旅馆等）。
                """
            ),
            goal=dedent(
                """
                提供一个列表，包括各个满足用户需求的住宿选择（注意要使用中文且美观的展示你获得的信息）
                对于每一个选择，需要包括：（以 Markdown 形式输出）
                    名称和类型（酒店、套房、民宿等）
                    地理位置以及与景点的距离
                    每晚价格和住宿总费用
                    如何取消预定以及其他用户评价
                使用参数：
                    目的地：{destination}
                    日期范围：{date_range}
                    预算：{budget}
                """
            ),
            tools=[self.search_tool, self.calc_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Transportation_Agent(self):
        return Agent(
            role="交通规划专家",
            backstory=dedent(
                """
                您是交通规划专家。
                您了解全球各地所有主要的当地交通方式、共享出行APP、火车时刻表、租车公司和节省费用的通行证。
                """
            ),
            goal=dedent(
                """
                您需要提供全面的交通计划：（注意要使用中文且美观的展示你获得的信息并以 Markdown 形式输出）
                (在生成makedown时要注意)
                    推荐的交通方式（飞机、火车、巴士、出租车、租车）
                    详细的时刻表和总共耗时
                    费用估算和对比
                    特殊通行证或折扣票（例如城市交通卡）
                使用参数：
                    目的地：{destination}
                    日期范围：{date_range}
                    人数：{num_people}
                """
            ),
            tools=[self.search_tool, self.calc_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Weather_Agent(self):
        return Agent(
            role="天气预报专家",
            backstory=dedent(
                """
                您是一名专业气象学家。
                您能够获取并解读任何地方和日期范围的天气预报、历史平均气温和严重天气警报。
                """
            ),
            goal=dedent(
                """
                您需要收集详细的天气信息：（注意要使用中文且美观的展示你获得的信息并以 Markdown 形式输出）
                    每日预报：气温高/低、降水几率、风速、湿度
                    出发/结束日的小时天气预报
                    严重天气警告和建议
                    该季节的历史气候数据
                使用参数：
                    目的地：{destination}
                    日期范围：{date_range}
                """
            ),
            tools=[self.search_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Itinerary_Planner_Agent(self):
        return Agent(
            role="日程规划专家",
            backstory=dedent(
                """
                您是一个细致的规划者，能够创建平衡且舒适的每日行程安排。
                您可以将推荐的景点与当地体验、餐饮、休息时间和实用的交通计划相结合。
                """
            ),
            goal=dedent(
                """
                制定每日行程：（注意要使用中文且美观的展示你获得的信息并以 Markdown 形式输出）
                    早上、下午、晚上的活动安排
                    餐饮推荐，包括当地特色菜肴
                    各停留点之间的交通指引
                    休息时间或可选体验建议
                使用参数：
                    目的地：{destination}
                    日期范围：{date_range}
                    偏好：{preferences}
                """
            ),
            tools=[self.search_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )

    def Budget_Analyst_Agent(self):
        return Agent(
            role="预算分析和优化专家",
            backstory=dedent(
                """
                您是专注于旅行预算的财务分析师。
                您会拆解所有费用、识别可以减少费用的环节，并提供清晰的总结。
                """
            ),
            goal=dedent(
                """
                提供完整的预算分解：（注意要使用中文且美观的展示你获得的信息并以 Markdown 形式输出）
                    住宿费用总计
                    交通费用总计
                    活动和餐饮费用估算
                    整体旅行预算总结和每人费用
                    强调可能的节省方式（优惠券、通行证等）
                使用参数：
                    住宿费用：{accommodation}
                    交通费用：{transportation}
                    活动费用：{activities}
                    餐饮预算：{meal_budget}
                """
            ),
            tools=[self.search_tool, self.calc_tool],
            allow_delegation=True,
            verbose=True,
            memory=True,
            llm=self.llm,
        )
