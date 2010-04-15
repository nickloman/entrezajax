from django.core.cache import cache
import django.utils.simplejson as json

from Bio import Entrez
import logging
import settings

class EntrezCache:
    @classmethod
    def create_cache_key(cls, interface, **kwargs):
        keydict = {'interface':interface}
        keydict.update(kwargs)
        keys = sorted(keydict.keys())
        return "&".join(["%s=%s" % (k, keydict[k]) for k in keys])

    @classmethod
    def execute_and_cache_result(cls, fn, reg, **kwargs):
        cache_key = cls.create_cache_key(fn, **kwargs)
        result = cache.get(cache_key)
        if result:
            logging.debug("Found result in cache")
            return result
        else:
            logging.debug("Did not find result in cache")
            handle = fn(tool=reg.tool_id, email=reg.email, **kwargs)
            record = Entrez.read(handle)
            buf = json.dumps(record)
            record = json.loads(buf)
            cache.set(cache_key, record, settings.DEFAULT_CACHE_TIME)
            return record
        
    @classmethod
    def esummary(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.esummary, reg, **kwargs)
        
    @classmethod
    def espell(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.espell, reg, **kwargs)
    
    @classmethod
    def einfo(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.einfo, reg, **kwargs)
    
    @classmethod
    def esearch(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.esearch, reg, **kwargs)
    
    @classmethod
    def efetch(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.efetch, reg, **kwargs)
    
    @classmethod
    def elink(cls, reg, **kwargs):
        return cls.execute_and_cache_result(Entrez.elink, reg, **kwargs)
