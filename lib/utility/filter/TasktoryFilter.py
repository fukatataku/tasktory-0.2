# -*- coding: utf-8 -*-

# from lib.utility.filter.filters import FilterFactory
from lib.log.Logger import Logger
from lib.common.common import unique

# TasktoryFilterを使っている場所
# lib/ui/journal/filter/JournalFilter.py
# lib/ui/journal/Journal.py
# lib/utility/filters/filters.py
# test_filter.py


class TasktoryFilter(Logger):

    # def __init__(self, cls_map):
        # self.flt_map = [[cls() for cls in cls_list] for cls_list in cls_map]
        # super().__init__()
        # return

    def __init__(self, *filters_list):
        self.filters_list = filters_list
        return super().__init__()

    @Logger.logging
    def select(self, tasks):
        selected_tasks_list =\
            [self.__select(tasks, filters) for filters in self.filters_list]
        return unique(sum(selected_tasks_list, []), lambda t: t.path)

    @staticmethod
    def __select(tasks, filters):
        selected_tasks = [t for t in tasks]
        for flt in filters:
            selected_tasks = flt.select(selected_tasks)
        return selected_tasks

    # @staticmethod
    # def __uniq(tasks):
    #     unique_tasks = []
    #     for task in tasks:
    #         if task not in unique_tasks:
    #             unique_tasks.append(task)
    #     return unique_tasks

    # @classmethod
    # @Logger.logging
    # def get_filter(cls, flt_config_section):
        # filters_list = []
        # for name in cls.__parse(flt_config_section['filters']):
        #     filters_list.append(cls.__parse(flt_config_section[name]))
        # return cls.__get_filter(filters_list)

    # @classmethod
    # @Logger.logging
    # def __get_filter(cls, name_map):
        # cls_map = [cls.__filter_list(name_list) for name_list in name_map]
        # return cls(cls_map)

    # @staticmethod
    # def __parse(string):
        # return [_.strip() for _ in string.split(',')]

    # @staticmethod
    # def __filter_list(name_list):
        # return [FilterFactory.get_filter(name) for name in name_list]
