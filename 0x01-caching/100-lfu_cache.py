#!/usr/bin/env python3
""" LFU Caching """

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.queue = []
        self.freq = {}

    def put(self, key, item):
        """ Add an item in the cache """
        if key and item:
            if key in self.cache_data.keys():
                self.queue.remove(key)
                self.freq[key] += 1
            elif len(self.cache_data.keys()) >= self.MAX_ITEMS:
                discard = self.queue.pop(0)
                del self.cache_data[discard]
                del self.freq[discard]
                print("DISCARD: {}".format(discard))
            self.queue.append(key)
            self.cache_data[key] = item
            self.freq[key] = 1

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data.keys():
            return None
        self.queue.remove(key)
        self.queue.append(key)
        self.freq[key] += 1
        return self.cache_data[key]
