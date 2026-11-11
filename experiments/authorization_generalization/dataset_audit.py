"""Pre-evaluation checks: version filtering, label shortcuts and group leakage."""
import collections

def audit_labels(data):
 return {'n':len(data.steps),'positives':int(data.y.sum()),
  'positive_without_x_act1':sum(s.label==1 and not s.features['x_act1'] for s in data.steps),
  'positive_without_x_act1_by_task':dict(collections.Counter(s.user_task_id for s in data.steps if s.label==1 and not s.features['x_act1'])),
  'attacker_value_unlabelled':sum(s.attacker_key_match and not s.label for s in data.steps),
  'label_warning':'Reference action attempt labels are not independently adjudicated authorization labels.'}

def ensure_disjoint(train,test,key):
 overlap={key(x) for x in train}&{key(x) for x in test}
 if overlap:raise ValueError(f'group leakage: {sorted(overlap)}')
