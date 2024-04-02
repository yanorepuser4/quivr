from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID
from models.settings import get_supabase_client
from modules.analytics.entity.analytics import BrainsUsages, Usage
from modules.brain.service.brain_user_service import BrainUserService

brain_user_service = BrainUserService()

class Analytics:
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_brains_usages(self, user_id: UUID, brain_id: Optional[UUID] = None) -> BrainsUsages:
        user_brains = brain_user_service.get_user_brains(user_id)
        if brain_id is not None:
            user_brains = [brain for brain in user_brains if brain.id == brain_id]

        usages = []

        for brain in user_brains:
            chat_history = (
                self.db.from_("chat_history")
                .select("*")
                .filter("brain_id", "eq", str(brain.id))
                .execute()
            ).data

            usage_per_day = defaultdict(int)
            for chat in chat_history:
                message_time = datetime.strptime(chat['message_time'], "%Y-%m-%dT%H:%M:%S.%f")
                usage_per_day[message_time.date()] += 1

            # Generate all dates in the last 7 days
            start_date = datetime.now().date() - timedelta(days=6)
            all_dates = [start_date + timedelta(days=i) for i in range(6)]
            for date in all_dates:
                usage_per_day[date] += 0

            brain_usages = sorted(
                [Usage(date=date, usage_count=count) for date, count in usage_per_day.items() if start_date <= date <= datetime.now().date()],
                key=lambda usage: usage.date
            )
            usages.extend(brain_usages)

        return BrainsUsages(usages=usages)