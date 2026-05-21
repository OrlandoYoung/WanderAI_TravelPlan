# main.py

import os

import logging
import time
import random
import uuid
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

from crewai import Crew, Process
from agents import TravelAgents
from tasks.tasks import TravelTasks
from tools.file_io import save_markdown

from trip.models import (
    Trip, TripWeather, TripTransport, TripHotel,
    TripFood, TripItinerary, TripBudget, TripSummary
)

logging.basicConfig(level=logging.INFO)
load_dotenv()

class TripCrew:
    def __init__(self, origin, destination, date_range, interests, person, trip_id=None, max_workers=5):
        self.origin      = origin
        self.destination = destination
        self.date_range  = date_range
        self.interests   = interests
        self.person      = person
        self.trip_id     = trip_id or uuid.uuid4().hex
        self.max_workers = max_workers

    def run(self):
        agents  = TravelAgents()
        tasks_d = TravelTasks()

        tp = agents.Trip_Planner_Agent()
        dr = agents.Destination_Research_Agent()
        ac = agents.Accommodation_Agent()
        tr = agents.Transportation_Agent()
        we = agents.Weather_Agent()
        it = agents.Itinerary_Planner_Agent()
        ba = agents.Budget_Analyst_Agent()

        shared_inputs = {
            "destination":     self.destination,
            "date_range":      self.date_range,
            "num_people":      self.person,
            "budget":          None,
            "preferences":     self.interests,
            "accommodation":   "",
            "transportation":  "",
            "activities":      "",
            "meal_budget":     ""
        }

        task_mapping = {
            "Weather_Forecasts":                tasks_d.Weather_Forecasts(we,  self.destination, self.date_range),
            "Transportation_Between_Destinations": tasks_d.Transportation_Between_Destinations(
                                                  tr, self.origin, self.destination, self.date_range, self.person),
            "Plan_Local_Transportation":        tasks_d.Plan_Local_Transportation(tr, self.destination, self.date_range, self.person),
            "Info_Transportation_Passes":       tasks_d.Info_Transportation_Passes(tr, self.destination, self.date_range, self.person),
            "Find_Your_Perfect_Stay":           tasks_d.Find_Your_Perfect_Stay(ac, self.destination, self.date_range, self.person),
            "Discover_Local_Cuisine":           tasks_d.Discover_Local_Cuisine(dr, self.destination, self.date_range, self.person),
            "Daily_Itineraries":                tasks_d.Daily_Itineraries(it, self.destination, self.date_range, self.interests, self.person),
            "Budget_Plan":                      tasks_d.Budget_Plan(ba, self.destination, self.date_range, self.person),
        }

        results = {}

        def run_with_retry(task, tries=3, base_delay=0.5):
            last_exc = None
            for attempt in range(1, tries+1):
                try:
                    return Crew(
                        agents=[task.agent],
                        tasks=[task],
                        process=Process.sequential,
                        verbose=False
                    ).kickoff(shared_inputs)
                except Exception as e:
                    last_exc = e
                    if attempt < tries:
                        delay = base_delay * (2 ** (attempt-1)) + random.uniform(0, 0.2)
                        logging.warning(f"[{task.agent.role}] 尝试 {attempt} 失败，{delay:.1f}s 后重试")
                        time.sleep(delay)
                    else:
                        logging.error(f"[{task.agent.role}] 重试 {tries} 次后仍失败")
            raise last_exc

        # 并发执行各子任务
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_name = {
                executor.submit(run_with_retry, task): name
                for name, task in task_mapping.items()
            }
            for future in as_completed(future_to_name):
                name = future_to_name[future]
                out = future.result()
                # 转为字符串存储
                results[name] = str(out)
                logging.info(f"✅ {name} 完成")

        # 主表
        trip, _ = Trip.objects.get_or_create(trip_id=self.trip_id)

        # 存储各部分 Markdown
        TripWeather.objects.update_or_create(
            trip=trip, defaults={'markdown_content': results.get("Weather_Forecasts", "")}
        )
        transport_md = "\n\n".join([
            results.get("Transportation_Between_Destinations", ""),
            results.get("Plan_Local_Transportation", ""),
            results.get("Info_Transportation_Passes", ""),
        ])
        TripTransport.objects.update_or_create(
            trip=trip, defaults={'markdown_content': transport_md}
        )
        TripHotel.objects.update_or_create(
            trip=trip, defaults={'markdown_content': results.get("Find_Your_Perfect_Stay", "")}
        )
        TripFood.objects.update_or_create(
            trip=trip, defaults={'markdown_content': results.get("Discover_Local_Cuisine", "")}
        )
        TripItinerary.objects.update_or_create(
            trip=trip, defaults={'markdown_content': results.get("Daily_Itineraries", "")}
        )
        TripBudget.objects.update_or_create(
            trip=trip, defaults={'markdown_content': results.get("Budget_Plan", "")}
        )

        # 最终汇总
        final_task = tasks_d.Final_Trip_Plan(
            tp, list(task_mapping.values()),
            self.origin, self.destination, self.date_range, self.interests, self.person,
            save_markdown
        )
        summary_out = Crew(
            agents=[tp],
            tasks=[final_task],
            process=Process.sequential,
            verbose=True
        ).kickoff(shared_inputs)

        summary_md = str(summary_out)
        TripSummary.objects.update_or_create(
            trip=trip, defaults={'markdown_content': summary_md}
        )

        # 更新状态
        trip.status = Trip.COMPLETED
        trip.save()

        return {
            "trip_id":    self.trip_id,
            "summary_md": summary_md
        }


if __name__ == "__main__":
    # 本地测试脚本
    origin      = "上海"
    destination = "西安"
    date_range  = "2025年8月1日至2025年8月5日"
    interests   = "好吃的, 好玩的, 适合拍照打卡"
    person      = 3

    crew = TripCrew(origin, destination, date_range, interests, person)
    result = crew.run()
    md_path = save_markdown(result["summary_md"])
    print(f"\nTrip ID: {result['trip_id']}")
    print(f"已保存 Markdown：{md_path}")
