import json, time, urllib.request, urllib.parse
UA = "Mozilla/5.0 (Linux; Android 14) Chrome/130 Mobile"
def get(url, data=None, t=40):
    s = time.time()
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, "Origin": "https://sharanuvl1-png.github.io", "Accept": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=t); b = r.read()
        return r.status, time.time() - s, b, r.headers.get("access-control-allow-origin")
    except Exception as e:
        return str(e), time.time() - s, b"", None
def sparql(q):
    return get("https://query.wikidata.org/sparql?" + urllib.parse.urlencode({"query": q, "format": "json"}))
TYPES = "Q34038 Q35509 Q57821 Q1785071 Q109607 Q40080 Q23397 Q839954 Q23413 Q8502 Q54050 Q23442 Q43742 Q6017969 Q2298569 Q44539 Q842402 Q32815 Q16970 Q33506 Q22698 Q4989906 Q570116 Q179700 Q1107656 Q8514 Q473972 Q46169 Q162875 Q381885 Q12518 Q5003624 Q16560 Q207694 Q860861 Q1129985 Q1371051 Q2049994 Q37654 Q330284 Q132510 Q1076486 Q194195 Q1144661 Q811979 Q174782 Q2977 Q15911738 Q105731 Q1440300 Q3947 Q47521 Q15324 Q131681 Q39816 Q34627 Q160742 Q44613 Q271669 Q1500350 Q12323"
c, t, b, a = sparql("SELECT ?t ?tLabel WHERE { VALUES ?t { %s } SERVICE wikibase:label { bd:serviceParam wikibase:language \"en\". } }" % " ".join("wd:" + x for x in TYPES.split()))
print("labels", c, round(t, 2), a)
for r in json.loads(b)["results"]["bindings"]: print(r["t"]["value"].split("/")[-1], r["tLabel"]["value"])
PLACES = [("Dubai", 25.2048, 55.2708, 25, 12), ("Hampi", 15.335, 76.46, 15, 10), ("Manali", 32.2432, 77.1892, 20, 12), ("Udaipur", 24.5854, 73.7125, 15, 10)]
for name, lat, lon, R, RS in PLACES:
    pt = 'bd:serviceParam wikibase:center "Point(%s %s)"^^geo:wktLiteral' % (lon, lat)
    qs = """SELECT ?i ?iLabel ?iDescription ?t ?loc ?sl ?img ?art WHERE {
 SERVICE wikibase:around { ?i wdt:P625 ?loc . %s . bd:serviceParam wikibase:radius "%d" . }
 ?i wdt:P31 ?t . VALUES ?t { %s }
 ?i wikibase:sitelinks ?sl .
 OPTIONAL { ?i wdt:P18 ?img }
 OPTIONAL { ?art schema:about ?i ; schema:isPartOf <https://en.wikipedia.org/> }
 SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} LIMIT 400""" % (pt, R, " ".join("wd:" + x for x in TYPES.split()))
    c, t, b, a = sparql(qs)
    rows = json.loads(b)["results"]["bindings"] if c == 200 else []
    print("==", name, "sights", c, round(t, 2), a, len(rows))
    for r in rows[:25]: print("  ", r["iLabel"]["value"], "|", r["t"]["value"].split("/")[-1], "| sl", r["sl"]["value"], "| desc", r.get("iDescription", {}).get("value", ""), "| art" if "art" in r else "")
    qh = """SELECT ?h ?hLabel ?loc ?sl ?img ?web ?art WHERE {
 SERVICE wikibase:around { ?h wdt:P625 ?loc . %s . bd:serviceParam wikibase:radius "%d" . }
 ?h wdt:P31/wdt:P279* wd:Q27686 .
 ?h wikibase:sitelinks ?sl .
 OPTIONAL { ?h wdt:P18 ?img } OPTIONAL { ?h wdt:P856 ?web }
 OPTIONAL { ?art schema:about ?h ; schema:isPartOf <https://en.wikipedia.org/> }
 SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} LIMIT 300""" % (pt, RS)
    c, t, b, a = sparql(qh)
    rows = json.loads(b)["results"]["bindings"] if c == 200 else []
    print("==", name, "hotels", c, round(t, 2), len(rows), [r["hLabel"]["value"] for r in rows[:12]])
    qL = '[out:json][timeout:25];(nwr(around:%d,%s,%s)["tourism"="viewpoint"]["name"];nwr(around:%d,%s,%s)["natural"~"^(waterfall|cave_entrance|hot_spring|beach|peak|arch)$"]["name"];nwr(around:%d,%s,%s)["historic"~"^(ruins|fort|archaeological_site|castle|city_gate)$"]["name"];);out center 200;' % ((R*800, lat, lon) * 3)
    for ep in ["https://maps.mail.ru/osm/tools/overpass/api/interpreter", "https://overpass-api.de/api/interpreter"]:
        c, t, b, a = get(ep, ("data=" + urllib.parse.quote(qL)).encode(), 30)
        print("==", name, "osm-sights", ep.split("/")[2], c, round(t, 2), a, b.count(b'"type"'))
    # wikipedia geosearch
    c, t, b, a = get("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({"action": "query", "generator": "geosearch", "ggscoord": f"{lat}|{lon}", "ggsradius": 10000, "ggslimit": 50, "prop": "description", "format": "json", "formatversion": 2}))
    pages = json.loads(b)["query"]["pages"] if c == 200 else []
    print("==", name, "wiki geo", len(pages), [(p["title"], p.get("description", "")) for p in pages[:30]])
