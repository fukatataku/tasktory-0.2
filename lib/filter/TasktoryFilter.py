# -*- coding: utf-8 -*-

from lib.filter.filters import FilterFactory


class TasktoryFilter:

    def __init__(self, cls_map):
        self.flt_map = [[cls() for cls in cls_list] for cls_list in cls_map]
        return

    def select(self, task_list):
        task_map =\
            [self.__select(task_list, flt_list) for flt_list in self.flt_map]
        task_list = sum(task_map, [])
        return self.__uniq(task_list)

    @staticmethod
    def __select(task_list, flt_list):
        selected_task_list = [t for t in task_list]
        for flt in flt_list:
            selected_task_list = flt.select(selected_task_list)
        return selected_task_list

    @staticmethod
    def __uniq(task_list):
        unique_task_list = []
        for task in task_list:
            if task not in unique_task_list:
                unique_task_list.append(task)
        return unique_task_list

    @classmethod
    def get_filter(cls, name_map):
        cls_map = [cls.get_filter_list(name_list) for name_list in name_map]
        return cls(cls_map)

    @staticmethod
    def get_filter_list(name_list):
        return [FilterFactory.get_filter(name) for name in name_list]
