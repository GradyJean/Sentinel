import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import Dict

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import tasks
from models.scheduler import TaskScheduler
from service import task_scheduler_service


class SchedulerTask(ABC):
    """
    任务抽象类
    """
    task_id: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "task_id") or cls.task_id is None:
            raise TypeError(f"{cls.__name__} task_id")

    @abstractmethod
    async def run(self):
        pass


class SchedulerManager:
    def __init__(self):
        self.config: Dict[TaskScheduler] = self.__load_config()
        self.scheduler = AsyncIOScheduler()
        self.__auto_import_tasks()
        self.__register_tasks()

    def start(self):
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()

    @staticmethod
    def __load_config() -> Dict[TaskScheduler]:
        """
        加载配置
        :return:
        """
        config: Dict[TaskScheduler] = {}
        records = task_scheduler_service.get_all()
        if records:
            for record in records:
                config[record.task_id] = record
        return config

    @staticmethod
    def __auto_import_tasks():
        """
        自动导入任务
        :return:
        """
        for module_info in pkgutil.walk_packages(tasks.__path__, tasks.__name__ + "."):
            importlib.import_module(module_info.name)

    @staticmethod
    def __all_task_classes():
        """
        获取所有任务类
        :return:
        """
        subclasses = set()
        queue = [SchedulerTask]
        while queue:
            parent = queue.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child)
                    queue.append(child)
        return subclasses

    def __register_tasks(self):
        """
        注册任务
        :return:
        """
        for cls in self.__all_task_classes():
            task_id = cls.task_id
            if task_id not in self.config:
                continue
            task_config: TaskScheduler = self.config[task_id]
            task = cls()
            self.scheduler.add_job(
                func=task.run,
                trigger=CronTrigger.from_crontab(task_config.cron),
                id=task_id,
                replace_existing=True
            )
