import urllib
import urllib2
import logging

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        logging.debug(headers)
        return headers

def hmmer(endpoint, args1, args2):
    opener = urllib2.build_opener(SmartRedirectHandler())
    urllib2.install_opener(opener);

    params = urllib.urlencode(args1)
    try:
        req = urllib2.Request(endpoint,
                              data = params,
                              headers={"Accept" : "application/json"})
        v = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        raise Exception("HTTP Error 400: %s" % e.read())

    results_url = v['location']

    enc_res_params = urllib.urlencode(args2)
    modified_res_url = results_url + '?' + enc_res_params

    results_request = urllib2.Request(modified_res_url)
    f = urllib2.urlopen(results_request)
    return f

def phmmer(**kwargs):
    logging.debug(kwargs)
    args = {'seq' : kwargs.get('seq'),
            'seqdb' : kwargs.get('seqdb')}
    args2 = {'output' : 'json', 'range' : kwargs.get('range')}
    return hmmer("http://hmmer.janelia.org/search/phmmer", args, args2)

def hmmscan(**kwargs):
    logging.debug(kwargs)
    args = {'seq' : kwargs.get('seq'),
            'hmmdb' : kwargs.get('hmmdb')}
    args2 = {'output' : 'json'}
    range = kwargs.get('range', None)
    if range:    
    	args2['range'] = range
    	
    return hmmer("http://hmmer.janelia.org/search/hmmscan", args, args2)

def test():
    seq = """>lcl||YPD4_1219|ftsK|128205128 putative cell division protein
MSQEYTEDKEVTLKKLSNGRRLLEAVLIVVTILAAYLMVALVSFNPSDPSWSQTAWHEPI
HNLGGSIGAWMADTLFSTFGVLAYAIPPIMVIFCWTAFRQRDASEYLDYFALSLRLIGTL
ALILTSCGLAALNIDDLYYFASGGVIGSLFSNAMLPWFNGVGATLTLLCIWVVGLTLFTG
WSWLVIAEKIGAAVLGSLTFITNRSRREERYDDEDSYHDDDHADGRDITGQEKGVVSNKG
VVSNNAVVGAGVAASSALAHGDDDVLFSAPSVTDSIVEHGSVVATGTETTDTKATDTNDE
YDPLLSPLRATDYSVQDATSSPIADVAVEPVLNHDAAAIYGTTPVMTNTATPPLYSFELP
EESLPIQTHAAPTERPEPKLGAWDMSPTPVSHSPFDFSAIQRPVGQLESRQPGSNQSGSH
QIHSAQSSHISVGNTPYMNPGLDAQIDGLSTTSLTNKPVLASGTVAAATAAAAFMPAFTA
TSDSSSQIKQGIGPELPRPNPVRIPTRRELASFGIKLPSQRMAEQELRERDGDETQNPQM
AASSYGTEITSDEDAALQQAILRKAFADQQSERYALSTLAEQSSITERSPAAEMPTTPSQ
VSDLEDEQALQEAELRQAFAAQQQHRYGATGDTDNAVDNIRSVDTSTAFTFSPIADLVDD
SPREPLFTLSPYVDETDVDEPVQLEGKEESLLQDYPEQVPTYQPPVQQAHLGQSAPTQPS
HTQSTYGQSTYGQSTYGQSTPAPVSQPVVTSASAISTSVTPTSIASLNTAPVSAAPVAPS
PQPPAFSQPTAAMDSLIHPFLMRNDQPLQKPTTPLPTLDLLSSPPAEEEPVDMFALEQTA
RLVEARLGDYRVKAEVVGISPGPVITRFELDLAPGVKASRISNLSRDLARSLSAIAVRVV
EVIPGKPYVGLELPNKHRQTVYLREVLDCAKFRENPSPLAIVLGKDIAGQPVVADLAKMP
HLLVAGTTGSGKSVGVNAMILSILYKATPDDVRFIMIDPKMLELSVYEGIPHLLTGVVTD
MKDAANALRWCVGEMERRYKLMSALGVRNLAGYNERVAQAEAMGRPIPDPFWKPSDSMDI
SPPMLVKLPYIVVMVDEFADLMMTVGKKVEELIARLAQKARAAGIHLVLATQRPSVDVIT
GLIKANIPTRIAFTVSSKIDSRTILDQGGAESLLGMGDMLYMAPNSSIPVRVHGAFVRDQ
EVHAVVNDWKARGRPQYIDSILSGGEEGEGGGLGLDSDEELDPLFDQAVNFVLEKRRASI
SGVQRQFRIGYNRAARIIEQMEAQQIVSTPGHNGNREVLAPPPHE"""
    handle = hmmscan(hmmdb = 'pfam', seq = seq)
    import json
    j = json.loads(handle.read())
    print json.dumps(j, sort_keys=True, indent=4)

# test()

