"""Engineering evidence binding, inspired by CaMeL policies and PROVISO §3.1.
A raw source digest is an identity/integrity check, NOT proof of authorization.
Only a trusted contract may pin the digest and explicitly delegate a field.
"""
import hashlib
import json
from .authorization import ExternalField, canonical, validate

class EvidenceStore:
    def __init__(self): self._artifacts = {}
    def ingest(self, text: str, *, executed: bool):
        if not executed: return
        digest = hashlib.sha256(text.encode()).hexdigest()
        try: value = json.loads(text)
        except (ValueError, TypeError): return
        if isinstance(value,dict): self._artifacts[digest] = value
    def resolve(self, grant, *, enabled=True):
        args = {}
        for k,v in grant.args.items():
            if isinstance(v,ExternalField):
                if not enabled or v.sha256 not in self._artifacts: return None
                obj = self._artifacts[v.sha256]
                if v.field not in obj: return None
                v = obj[v.field]
            args[k] = v
        try: validate(grant.tool,args)
        except (ValueError,TypeError): return None
        return args
