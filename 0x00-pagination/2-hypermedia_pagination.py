#!/usr/bin/env python3
""" Simple pagination"""

import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """ Return a tuple of size two containing a start index and an end index"""
    return ((page - 1) * page_size, page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Return page with pagination"""
        return self.get_dataset(page, page_size)

    def get_dataset(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ Return dataset with pagination"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0
        self.__dataset = []
        with open(self.DATA_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            start, end = index_range(page, page_size)
            for i, row in enumerate(reader):
                if i in range(start, end):
                    self.__dataset.append(row)
                if i >= end:
                    break
        return self.__dataset

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """ Return a dictionary"""
        data = self.get_dataset(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if page < total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
