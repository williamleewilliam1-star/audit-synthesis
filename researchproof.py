#!/usr/bin/env python3
import argparse, datetime as dt, hashlib, html, json, pathlib, urllib.parse, urllib.request

OPENALEX = 'https://api.openalex.org/works'
USER_AGENT = 'ResearchProof/0.1 (+https://github.com/williamleewilliam1-star/researchproof)'

def canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def sha(obj):
    return hashlib.sha256(canon(obj)).hexdigest()

def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()

def fetch_openalex(query, limit=8, opener=urllib.request.urlopen):
    params = urllib.parse.urlencode({'search': query, 'per-page': str(limit)})
    url = OPENALEX + '?' + params
    req = urllib.request.Request(url, headers={'Accept':'application/json','User-Agent':USER_AGENT})
    with opener(req, timeout=20) as r:
        payload = json.load(r)
    return url, payload

def normalize_work(w):
    loc = w.get('primary_location') or {}
    source = loc.get('source') or {}
    oa = w.get('open_access') or {}
    authors=[]
    for a in (w.get('authorships') or [])[:4]:
        author=(a.get('author') or {}).get('display_name')
        if author: authors.append(author)
    doi=w.get('doi')
    return {
      'openalex_id': w.get('id'), 'title': w.get('display_name'),
      'year': w.get('publication_year'), 'doi': doi,
      'cited_by_count': int(w.get('cited_by_count') or 0),
      'is_retracted': bool(w.get('is_retracted')),
      'is_open_access': bool(oa.get('is_oa')),
      'source': source.get('display_name'), 'authors': authors,
      'flags': (['RETRACTED'] if w.get('is_retracted') else []) + ([] if doi else ['MISSING_DOI'])
    }

def run_workflow(query, raw_payload):
    audit=[]
    def event(step, inp, out, note=''):
        audit.append({'at':now(),'step':step,'input_sha256':sha(inp),'output_sha256':sha(out),'note':note})

    plan={'question':query.strip(),'policy':{'exclude_retracted':True,'human_approval_required':True,'scientific_claims_without_source_support':'forbidden'}}
    event('PLAN', {'query':query}, plan, 'Bound the question and trust policy before retrieval.')

    raw_results=list(raw_payload.get('results') or [])
    event('DISCOVER', {'query':query}, {'result_count':len(raw_results)}, 'Retrieve candidate works from OpenAlex.')

    normalized=[normalize_work(w) for w in raw_results]
    event('NORMALIZE', {'raw_count':len(raw_results)}, normalized, 'Normalize metadata into an auditable evidence schema.')

    accepted=[w for w in normalized if not w['is_retracted']]
    excluded=[w for w in normalized if w['is_retracted']]
    flags=[]
    for w in accepted:
        for f in w['flags']:
            flags.append({'work':w['openalex_id'],'flag':f})
    if not accepted: flags.append({'work':None,'flag':'NO_ACCEPTED_EVIDENCE'})
    validation={'accepted_count':len(accepted),'excluded_count':len(excluded),'flags':flags}
    event('VALIDATE', normalized, validation, 'Retracted works are excluded; metadata gaps remain visible.')

    years=[w['year'] for w in accepted if isinstance(w['year'],int)]
    oa=sum(1 for w in accepted if w['is_open_access'])
    summary={
      'retrieval_statement': (
        ('Retrieved %d non-retracted works%s; %d are marked open access.' % (len(accepted), (' spanning %d-%d' % (min(years),max(years))) if years else '', oa))
        if accepted else 'No non-retracted works were accepted.'
      ),
      'scientific_conclusion':'WITHHELD',
      'reason':'ResearchProof v0.1 does not infer a scientific conclusion from metadata alone.',
      'human_approval_required':True
    }
    event('SYNTHESIZE', validation, summary, 'Generate only claims supported by retrieved metadata; withhold scientific inference.')

    decision={'status':'READY_FOR_HUMAN_REVIEW' if accepted else 'ESCALATE_NO_EVIDENCE','approved':False,'reviewer':None}
    event('REVIEW_GATE', summary, decision, 'A person must review sources and explicitly approve downstream use.')

    return {'schema':'researchproof.audit.v1','generated_at':now(),'question':query,'plan':plan,'evidence':accepted,'excluded':excluded,'validation':validation,'summary':summary,'decision':decision,'audit':audit}

def render_html(report):
    rows=''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
      html.escape(str(w.get('year') or '—')), html.escape(w.get('title') or 'Untitled'),
      html.escape(w.get('source') or '—'), html.escape(w.get('doi') or '—'),
      html.escape(', '.join(w.get('flags') or []) or 'OK')) for w in report['evidence'])
    events=''.join('<li><strong>%s</strong> — %s<br><code>%s → %s</code></li>' % (
      html.escape(a['step']), html.escape(a['note']), a['input_sha256'][:12], a['output_sha256'][:12]) for a in report['audit'])
    data=html.escape(json.dumps(report,ensure_ascii=False,indent=2))
    return '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ResearchProof audit demo</title><link rel="stylesheet" href="styles.css"></head><body><main><p class="eyebrow">AUDITABLE RESEARCH AGENT · V0.1</p><h1>ResearchProof</h1><p class="lede">Evidence synthesis that shows its work and stops before unsupported scientific conclusions.</p><section><h2>Question</h2><p>%s</p><p class="statement">%s</p><p><strong>Scientific conclusion:</strong> %s — %s</p></section><section><h2>Evidence matrix</h2><div class="scroll"><table><thead><tr><th>Year</th><th>Title</th><th>Source</th><th>DOI</th><th>Flags</th></tr></thead><tbody>%s</tbody></table></div></section><section><h2>Agent audit trail</h2><ol>%s</ol><p class="gate">Human gate: %s · approved=false</p></section><details><summary>Machine-readable report</summary><pre>%s</pre></details><footer>Prototype for Digital Science Catalyst Grant 2026. Public metadata only. No scientific conclusion is generated without human review.</footer></main></body></html>''' % (html.escape(report['question']),html.escape(report['summary']['retrieval_statement']),html.escape(report['summary']['scientific_conclusion']),html.escape(report['summary']['reason']),rows,events,html.escape(report['decision']['status']),data)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('query')
    ap.add_argument('--out',default='demo_data.json')
    ap.add_argument('--html',default='demo.html')
    ap.add_argument('--fixture')
    args=ap.parse_args()
    if args.fixture:
        raw=json.loads(pathlib.Path(args.fixture).read_text())
        source='fixture:'+args.fixture
    else:
        source,raw=fetch_openalex(args.query)
    report=run_workflow(args.query,raw)
    report['retrieval_source']=source
    pathlib.Path(args.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    pathlib.Path(args.html).write_text(render_html(report))
    print(json.dumps({'status':report['decision']['status'],'accepted':len(report['evidence']),'excluded':len(report['excluded']),'flags':len(report['validation']['flags']),'audit_steps':len(report['audit']),'out':args.out,'html':args.html},indent=2))

if __name__=='__main__': main()
