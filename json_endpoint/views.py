import logging

from django.http import HttpResponse, HttpResponseForbidden
import django.utils.simplejson as json

from Bio import Entrez

from devdb.models import DeveloperRegistration
from cache import EntrezCache

Entrez.email = "n.j.loman@bham.ac.uk"

allowed_keywords = {
	'espell'   : ['db', 'term'],
	'einfo'    : ['db'],
	'esearch'  : ['db', 'term', 'field', 'reldate', 'mindate', 'maxdate', 'datetype', 'retstart', 'retmax', 'rettype', 'sort'],
	'esummary' : ['db', 'id', 'retstart', 'retmax'],
	'efetch'   : ['db', 'id', 'report', 'dispstart', 'dispmax'],
	'elink'    : ['db', 'id', 'reldate', 'mindate', 'maxdate', 'datetype', 'term', 'retmode', 'dbfrom', 'cmd', 'holding', 'version'],	
}

default_keywords = {
	'esearch'  : {'retmode' : 'xml'},
	'esummary' : {'retmode' : 'xml'},
	'elink'    : {'retmode' : 'xml'},
	'efetch'   : {'mode' : 'xml', 'rettype' : 'xml'}
}

def keywords(fn, args):
    d = {}
    for key, val in args.iteritems():
        if key in allowed_keywords[fn]:
            d[str(key)] = val

    if fn in default_keywords:
        for key, val in default_keywords[fn].iteritems():
            d[str(key)] = val
    
    logging.info(d)
    return d

def check_developer_api(fn):
    def new(*args):
        request = args[0]
        
        api_key = request.GET.get('apikey', None) 
        if not api_key:
        	return HttpResponseForbidden('No API key was supplied')
        
        reg = DeveloperRegistration.get_by_key_name(api_key)
        if not reg:
        	return HttpResponseForbidden('No API key matching the supplied value was found')
        	
        setattr(request, "entrezajax_developer_registration", reg)

        return fn(*args)
    return new
   
def paginate(request, id_list):
    start = int(request.GET.get('start', 0))
    id_list = id_list[start:]    

    max = int(request.GET.get('max', 20))
    id_list = id_list[0:max]
    
    return id_list

def dump_result(request, response, records, extradict = {}):
    result = {'entrezajax' : {'error' : False}}
    result['entrezajax'].update(extradict)
    result['result'] = records       
    
    callback = request.GET.get('callback', None)
    if callback:
        print >>response, "%s(" % (callback,),
        json.dump(result, response)
        print >>response, ")"
    else:
    	json.dump(result, response)
    
def handle_request(request, args, fn_name, fn_ptr, extradict = {}):
    response = HttpResponse(mimetype="application/json")
    records = fn_ptr(request.entrezajax_developer_registration, **args)
    dump_result(request, response, records, extradict)
    return response

# the entrez commands

@check_developer_api
def espell(request):
    return handle_request(request, keywords('espell', request.GET), 'espell', EntrezCache.espell)
   
@check_developer_api
def einfo(request):
    return handle_request(request, keywords('einfo', request.GET), 'einfo', EntrezCache.einfo)

@check_developer_api
def esearch(request):
    return handle_request(request, keywords('esearch', request.GET), 'esearch', EntrezCache.esearch)

@check_developer_api
def esummary(request):
    return handle_request(request, keywords('esummary', request.GET), 'esummary', EntrezCache.esummary)
   
@check_developer_api
def elink(request):
    return handle_request(request, keywords('elink', request.GET), 'elink', EntrezCache.elink)

@check_developer_api
def efetch(request):
    return handle_request(request, keywords('efetch', request.GET), 'efetch', EntrezCache.efetch)

# extended commands

def esearch_and_other(request, other_fn, other_ptr):
    record = EntrezCache.esearch(request.entrezajax_developer_registration, **keywords('esearch', request.GET))
    logging.info(record)
    if not record["IdList"]:
        response = HttpResponse(mimetype="application/json")
        dump_result(request, response, record)
        return response
    else:
        args = keywords('esummary', request.GET)
        id_list = paginate(request, record["IdList"])
        
        args['id'] = ",".join(id_list)
        logging.info(args)
        return handle_request(request, args, other_fn, other_ptr,
                              {
                               'count' : record["Count"],
                               'retmax' : record["RetMax"]
                              })

@check_developer_api
def esearch_and_esummary(request):
    return esearch_and_other(request, 'esummary', EntrezCache.esummary)
    
@check_developer_api
def esearch_and_efetch(request):
    return esearch_and_other(request, 'efetch', EntrezCache.efetch)

@check_developer_api
def esearch_and_elink(request):
    return esearch_and_other(request, 'elink', EntrezCache.elink)

def elink_and_other(request, other_fn, other_ptr):
    record = EntrezCache.elink(request.entrezajax_developer_registration, **keywords('elink', request.GET))
    # todo: check this is always correct

    id_list = [str(x.values()[0]) for x in record.pop()['LinkSetDb'].pop()['Link']]
    if not id_list:
        response = HttpResponse(mimetype="application/json")
        dump_result(request, response, record)
        return response
        
    id_list_len = len(id_list)
    id_list = paginate(request, id_list)
    logging.info(id_list)
               
    args = keywords(other_fn, request.GET)
    args['id'] = ",".join(id_list)
    logging.info(args)
    return handle_request(request, args, other_fn, other_ptr, {'count' : id_list_len})
    
@check_developer_api
def elink_and_esummary(request):
    return elink_and_other(request, 'esummary', EntrezCache.esummary)
    
@check_developer_api
def elink_and_efetch(request):
    return elink_and_other(request, 'efetch', EntrezCache.efetch)

