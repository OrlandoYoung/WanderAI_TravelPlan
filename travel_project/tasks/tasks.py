from crewai import Task
from textwrap import dedent

class TravelTasks:
    def __tip_section(self):
        return "如果你可以完美的执行我的需求，我将给你一万美金作为奖励!"
    # 最终行程计划任务（Final_Trip_Plan）
    def Final_Trip_Plan(self, agent, context, origin, destination,travel_dates, interests, person, callback_function):
        return Task(
            description=dedent(
                f"""
            **任务**: 汇总最终旅行计划并创建详细文档（不要使用任何三引号或```代码块标记）。
            **描述**: 
            - 总体行程规划负责人(Trip_Planner_Agent)充当项目经理，将来自不同专门团队成员的输出汇总为一个完整的旅行行程文档。
            - 该文档将以用户友好的段落形式呈现。
            - 生成的文档将采用Markdown格式，包含所有必要的细节和格式化，其中必须要有如下六个部分：交通方式、住宿信息、每日行程、美食推荐、天气、预算规划（注意分别用这六个词作为标题）。
 
            **参数**: 
            - 出发地：{origin}
            - 旅行目的地：{destination}
            - 旅行日期范围：{travel_dates}
            - 旅行者兴趣：{interests}
            - 旅行人数：{person}

            **注意事项**: {self.__tip_section()}
        """
            ),
            agent=agent,
            context=context,
            callback=callback_function,
            expected_output = 
            """
            {
  "旅行总结": "🌏 旅行的详细信息和总体概述，涵盖行程亮点、交通安排、住宿推荐、美食体验、天气状况和预算规划。",

  "旅行亮点": [
    {"名称": "🌟 亮点1", "描述": "简要描述，介绍此次旅行的特别之处。"},
    // ...更多亮点...
  ],

  "交通方式": {
    "到达方式": "🚗 一个列表，包括从出发地到目的地的所有交通选项。",
    "选项": [
      {
        "交通方式": "✈️ 飞机",
        "旅行时间": "3小时",
        "出发时间": "08:00",
        "到达时间": "11:00",
        "费用": "$150-$250",
        "详情": "直飞航班，舒适快捷。"
      },
      {
        "交通方式": "🚆 火车",
        "旅行时间": "6小时",
        "出发时间": "07:00",
        "到达时间": "13:00",
        "费用": "$70-$120",
        "详情": "风景优美，环保经济。"
      }
      // ... 更多交通方式和选项 ...
    ],
    "最佳选项": "✈️ 根据旅行时间和费用综合考虑，推荐飞机作为最佳选择。",
    "出行方式": "🚇 列出所有本地交通选项的详细信息。",
    "本地交通": [
      {"交通方式": "地铁 🚇", "详情": "快速便捷，覆盖主要景点。", "价格": "$2/次"},
      {"交通方式": "公交 🚌", "详情": "经济实惠，线路丰富。", "价格": "$1.5/次"},
      {"交通方式": "出租车 🚕", "详情": "灵活方便，适合短途。", "价格": "$10起步"}
      // ...更多交通方式...
    ],
    "通行证": "🎫 列出所有可用的通行证和详细信息。",
    "通行证信息": [
      {"名称": "城市通行证", "费用": "$30", "福利": "交通+景点免费入场", "适用条件": "3天内有效"},
      {"名称": "公共交通月票", "费用": "$50", "福利": "无限次乘坐公交地铁", "适用条件": "全月有效"}
      // ...更多通行证信息...
    ]
  },

  "住宿信息": [
    {
      "名称": "🏨 星级酒店A",
      "地址": "中心街123号",
      "联系方式": "+86 123 4567 8901",
      "类型": "酒店",
      "价格范围": "$100-$150/晚",
      "设施": ["免费WiFi", "早餐", "游泳池", "健身房"],
      "无障碍设施": "有",
      "可持续性": "绿色认证",
      "评价": "4.5/5 好评如潮",
      "预订": "https://hotel-a-booking.com"
    }
    // ...更多住宿选择...
  ],

  "每日行程": [
    {
      "日期": "2025-07-15",
      "计划": "上午参观博物馆，下午城市徒步，晚上品尝当地美食。",
      "活动": ["博物馆参观 🖼️", "城市徒步 🚶‍♂️", "美食体验 🍲"],
      "交通": ["步行 🚶", "地铁 🚇"],
      "用餐": ["午餐：当地特色餐厅", "晚餐：海鲜大排档"],
      "天气": "晴，25°C，微风",
      "建议": "早晨防晒，带水壶补水"
    }
    // ...更多天数...
  ],

  "美食推荐": [
    {
      "美食": "担担面 🍜",
      "餐厅": [
        {"名称": "小吃街A", "价格": "$5-$8"}
      ]
    },
    {
      "美食": "烤鸭 🦆",
      "餐厅": [
        {"名称": "餐厅B", "价格": "$20-$30"}
      ]
    }
    // ...更多美食...
  ],

  "天气": {
    "每日": [
      {"日期": "2025-07-15", "预报": "🌞 晴朗，最高25°C，最低18°C"}
    ],
    "每小时": [
      {"时间": "08:00", "预报": "🌤️ 多云"},
      {"时间": "12:00", "预报": "☀️ 晴朗"}
    ],
    "警报": ["⚠️ 暴雨预警", "⚠️ 高温警报"],
    "实时": "当前晴朗，温度23°C",
    "历史数据": "过去一周平均气温24°C"
  },

  "预算规划": {
    "分类": {
      "住宿": "$500",
      "交通": "$300",
      "餐饮": "$200"
      // ...更多类别...
    },
    "总计": "$1000"
  },

  "成本节约建议": [
    "✅ 优先选择公共交通，节约出租车费用",
    "✅ 提前预订住宿享受折扣",
    "✅ 使用优惠券和团购活动"
  ],

  "附加建议": [
    "🧳 携带轻便行李",
    "📱 下载当地地图APP，离线使用",
    "🔋 携带充电宝，保证手机电量"
  ]
}

            """,
        )
    
    def Research_Destination_Highlights(self, agent, origin, destination,travel_dates, interests, person):  # Destination_Research_Agent
        return Task(
            description=dedent(
                f"""
            **任务**：研究目的地的景点和评价（不要使用任何三引号或```代码块标记）。
            **描述**：根据用户兴趣、旅行日期、可持续性、无障碍性、预算、家庭友好性和独特体验等因素，深入了解目的地的主要景点、历史遗址、当地习俗、特殊活动、日常活动推荐和本地体验。

            **参数**:
            - 出发地：{origin}
            - 旅行目的地：{destination}
            - 旅行日期范围：{travel_dates}
            - 旅行者兴趣：{interests}
            - 旅行人数：{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
使用 **Markdown 格式** 输出以下内容（不要使用任何三引号或```代码块标记）：

- 按类别分组（地标、文化体验、本地活动等）
- 每个项目包括：
  - 📌 名称与简要介绍
  - 🕐 建议时间/时长
  - 📍 地点或区域
  - 🧭 实用信息（门票、时间等）
- 使用列表、表格和 emoji 美化
- 提供丰富的排版（如列表、层次结构、加粗）
""")

        )
        
    def Discover_Local_Cuisine(self, agent, destination,travel_dates, person):  # Destination_Research_Agent
        return Task(
            description=dedent(
                f"""
            **任务**：研究当地美食和餐饮选择（不要使用任何三引号或```代码块标记）。
            **描述**：研究目的地的著名菜肴以及推荐的餐饮场所，包含价格信息。

            **参数**:
            - 旅行目的地：{destination}
            - 旅行日期范围：{travel_dates}
            - 旅行人数：{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
使用 Markdown 格式展示（不要使用任何三引号或```代码块标记）：

- 🍱 推荐美食清单，每项包含：
  - 名称与简要介绍
  - 推荐餐厅（名称 + 💰价格 + 📍位置）
- 使用表格列出多个餐厅对比
- 添加 emoji 点缀 + 分点展示
""")
        )
    
    def Find_Your_Perfect_Stay(self, agent, destination,travel_dates, person):  # Accommodation_Agent
        return Task(
            description=dedent(
                f"""
            **任务**：搜索住宿选项（不要使用任何三引号或```代码块标记）。
            **描述**：根据位置、旅行人数、旅行日期、设施、无障碍性、可持续性评分、客户评价等，探索酒店、度假租赁或其他住宿类型。

            **参数**:
            - 旅行目的地：{destination}
            - 旅行日期范围：{travel_dates}
            - 旅行人数：{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
           expected_output = dedent("""
使用 **Markdown 格式** 美观地展示住宿选项（不要使用任何三引号或```代码块标记），每项包括：

- 🏨 名称、📍地址、📞联系方式
- 💰 价格范围
- 🛏️ 类型与设施（使用项目符号列出）
- 🌱 可持续性认证
- ⭐ 客户评价和评分
- 🔗 预订链接（如有）

可使用表格或分块展示，注意使用 emoji 和层次结构。
"""),
        )
    
    def Transportation_Between_Destinations(self, agent, origin, destination,travel_dates, person):  # Transportation_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 规划目的地之间的交通（不要使用任何三引号或```代码块标记）。
            **描述**: 探索在出发地和目的地之间的交通选择（航班、火车、巴士等），考虑以下因素：出发和到达时间、费用（预算友好）、总时间、舒适性和便利性、可持续性、无障碍性。
            **参数**: 
            - 出发地 : {origin}
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}
            - 旅行人数 :{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
使用 Markdown 格式输出（不要使用任何三引号或```代码块标记）：

- 🚄 各交通方式表格（包含出发时间、到达时间、费用、时长等）
- ✈️ 🚌 🚆 等 emoji 区分交通工具
- ✅ 推荐最佳选项并说明理由
- 美观排版、强调关键信息
"""),
        )
    
    def Plan_Local_Transportation(self, agent, destination,travel_dates, person):  # Transportation_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 规划当地交通（不要使用任何三引号或```代码块标记）。
            **描述**: 调查目的地的当地交通选项（公共交通、出租车、租车等），以便在目的地周围移动，记住使用中文。
            
            **参数**: 
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}
            - 旅行人数 :{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
使用 Markdown 格式展示（不要使用任何三引号或```代码块标记）：

- 各交通方式的清单（🚌 公交、🚕 出租车、🚲 自行车等）
- 每种方式的价格 💰、便利性、适用范围
- 可使用表格或项目符号，添加 emoji 提升可读性
"""),
        )
    
    def Info_Transportation_Passes (self, agent, destination,travel_dates, person):  # Transportation_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 提供交通通行证或票务信息（不要使用任何三引号或```代码块标记）。 
            **描述**: 研究并推荐可以节省费用和时间的交通通行证或票务，记住使用中文。
            考虑以下选项：
                • 城市通行证：结合交通和景点门票。
                • 公共交通通行证：适用于公交车、火车和地铁的日票、周票或月票。
                • 机场接送：共享或私人交通选项。
                • 租车优惠：折扣、保险套餐和附加驾驶员费用。         
                            
            **参数**: 
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}
            - 旅行人数 :{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
用 Markdown 展示所有可用通行证（不要使用任何三引号或```代码块标记）：

- 每种通行证：
  - 🎫 名称
  - 💰 费用
  - ✅ 福利
  - 📌 适用条件

- 使用表格汇总并添加 emoji 点缀
"""),
        )

    def Weather_Forecasts (self, agent, destination,travel_dates):  # Weather_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 获取天气预报（不要使用任何三引号或```代码块标记）。
            **描述**: 获取目的地在指定旅行日期期间的全面天气信息，记住使用中文。
            包括:
                • 每日预报：每日的温度、降水、风速和湿度。
                • 每小时预报：一天中特定时间的详细天气情况。
                • 天气警报：极端天气条件的预警（暴风雨、飓风等）。
                • 实时更新：当前天气状况和预报。
                • 历史数据：目的地的平均天气模式。

            **参数**: 
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
用 Markdown 格式展示天气（不要使用任何三引号或```代码块标记）：

- 📅 每日天气表格（温度、降雨、风速）
- 🕒 每小时预报（可选）
- ⚠️ 天气警报（列表形式）
- 🌡️ 实时天气描述
- 📈 历史气候图或总结（简要）

使用清晰排版，适合在前端卡片式组件显示。
"""),
        )
        
    def Daily_Itineraries(self, agent, destination,travel_dates, interests, person):  # Itinerary_Planner_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 创建每日行程（不要使用任何三引号或```代码块标记）。
            **描述**: 根据用户的特定偏好、时间限制和精力水平，制定一个全面且灵活的每日行程，记住使用中文。
            包括：
                • 计划：详细的每日计划。
                • 活动：当天所有活动的详细信息。
                • 交通：高效且经济的交通选项。
                • 餐饮：本地食品和餐饮推荐。
                • 住宿：相关住宿信息。
                • 天气：根据天气情况为户外活动和衣物建议提供建议。
                • 其他建议：根据行程和天气情况提供的其他建议（如必要的衣物、鞋类、配件）。

            **参数**: 
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}
            - 旅行兴趣: {interests}
            - 旅行人数 :{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
用 Markdown 格式展示每日行程（不要使用任何三引号或```代码块标记）：

- 📆 日期标题（如 `### Day 1 - 2025-07-14`）
- 🗺️ 行程安排（用时间轴或列表）
- 🍽️ 餐饮推荐
- 🚕 交通方式
- 🌤️ 天气预报摘要
- 🔍 活动亮点
- ✅ 衣物建议或其他注意事项

结构清晰、层级分明，适合前端展示。
"""),
        )
        
    def Budget_Plan (self, agent, destination,travel_dates, person):  # Budget_Analyst_Agent
        return Task(
            description=dedent(
                f"""
            **任务**: 制定预算计划（不要使用任何三引号或```代码块标记）。
            **描述**: 分析住宿、交通、活动和餐饮的费用，根据旅行日期范围和人数制定详细的预算计划，记住使用中文。
            包括：
                • 费用细分：各类别的逐项费用。
                • 总预算：旅行的总体估算费用。
                • 费用比较：分析每个类别中的不同选择（例如，比较酒店价格、交通票价、活动费用）。
                • 节省费用建议：建议如何在不影响旅行体验的前提下减少开支（例如，选择预算友好的住宿、选择公共交通、探索免费的活动）。
                • 灵活的预算安排：提供适应不同预算水平和优先事项的选项。
            **参数**: 
            - 旅游目的地: {destination}
            - 旅行日期范围: {travel_dates}
            - 旅行人数 :{person}

            **注意**: {self.__tip_section()}
        """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
用 Markdown 格式输出预算（不要使用任何三引号或```代码块标记）：

- 💸 分类预算（表格或项目符号）
- 📊 总预算金额
- 🔍 各项费用对比分析（图表或文本）
- 💡 成本节约建议（项目符号形式）
- 🎯 适合不同预算级别的选项推荐

使用 emoji 和排版提升可读性。
"""),
        )
    def Revise_Plan(self, agent, previous_plan: str, user_feedback: str):
        return Task(
            description=dedent(
                f"""
            **任务**: 根据用户反馈修订已有的旅行计划。
            **描述**: 接收上一次生成的完整旅行计划（Markdown 文档），
            以及用户的修改意见，对用户的意见进行分析，将任务分配给不同专门团队成员，然后根据返回的信息对原计划进行修改和完善，输出一份新的、
            满足反馈要求的旅行计划（仍然输出为 Markdown 文档且不含任何代码块标记），记住使用中文。

            **参数**:
            - 上一次行程计划:
            ```
            {previous_plan}
            ```
            - 用户反馈:
            ```
            {user_feedback}
            ```

            **注意**: 保留原计划中的所有合理内容，并根据反馈进行增删或调整。
            """
            ),
            agent=agent,
            async_execution=True,
            expected_output = dedent("""
用 Markdown 格式输出修订后的完整计划（不要使用任何三引号或```代码块标记））：

- 在原有基础上保留合理内容
- 用标题、表格、列表等排版清晰展示变更部分
- 使用 emoji 标注变更点（如 ✏️ 修订、➕ 新增、❌ 删除）
""")
,
        )