"""The authority front of HV/GV expressed as Cedar policies (Section 11 addendum, 16 November 2026).

Status: [PROPOSED - EXPLORATORY - IMPLEMENTATION STUDY]. This is a policy-engine study, not a new constraint:
the policies below restate the existing constraints over a typed context that REM computes. Cedar does not read
the user's request and does not keep payment history; REM supplies both as trusted, typed context.

Cedar semantics relied on (official documentation, cedar-docs commit 4091567, "How Cedar authorization works"):
default deny; forbid overrides permit; a policy whose evaluation errors is SKIPPED, not treated as a denial.
Because of the last property, the wrapper below withholds execution whenever the authorizer reports any
error or does not answer Allow, and the policies are validated against the schema when the module is loaded.
That wrapper behaviour is an engineering choice of this study, not a property of Cedar.

Nothing here implements or claims Progent's SMT check of policy expansion: the policy set is fixed.
"""
from __future__ import annotations

import cedarpy

SCHEMA = {"": {
    "entityTypes": {"User": {}, "Account": {}},
    "actions": {t: {"appliesTo": {"principalTypes": ["User"], "resourceTypes": ["Account"], "context": {"type": "Record", "attributes": {
        "authority": {"type": "Boolean"}, "overall": {"type": "String"}, "perm_effect": {"type": "String"}, "binding": {"type": "String"},
        "condition": {"type": "String"}, "fulfilment": {"type": "String"}, "direct_value": {"type": "String"}, "predicate": {"type": "String"}}}}}
        for t in ("send_money", "schedule_transaction", "update_scheduled_transaction", "update_password", "update_user_info")}}}

POLICIES = '''
@id("permit-authorized-call")
permit (principal == User::"account_holder", action, resource)
when { context.authority && context.overall != "denied" && context.predicate == "none" && context.direct_value == "ok" };

@id("forbid-denied")
forbid (principal, action, resource) when { context.overall == "denied" };

@id("forbid-authority-not-established")
forbid (principal, action, resource) when { !context.authority };

@id("forbid-other-effect")
forbid (principal, action, resource) when { context.perm_effect == "not_requested" || context.perm_effect == "other_operation" };

@id("forbid-contradicted-binding")
forbid (principal, action, resource) when { context.binding == "contradicted" };

@id("forbid-condition-false-or-unevaluable")
forbid (principal, action, resource) when { context.condition == "false" || context.condition == "unevaluable" };

@id("forbid-repetition-of-executed-payment")
forbid (principal, action, resource) when { context.fulfilment == "duplicate" };

@id("forbid-direct-value-mismatch-or-ambiguity")
forbid (principal, action, resource) when { context.direct_value != "ok" };

@id("forbid-declared-predicate")
forbid (principal, action, resource) when { context.predicate != "none" };
'''

_validation = cedarpy.validate_policies(POLICIES, SCHEMA)
if not _validation.validation_passed:                       # fail closed: the module cannot be used with invalid policies
    raise RuntimeError(f"Cedar policies do not validate against the schema: {_validation.errors}")
_POLICY_SET = cedarpy.PolicySet.from_str(POLICIES)
_SCHEMA = cedarpy.Schema.from_json_str(__import__("json").dumps(SCHEMA)) if hasattr(cedarpy.Schema, "from_json_str") else SCHEMA
_ENTITIES = [{"uid": {"type": "User", "id": "account_holder"}, "attrs": {}, "parents": []}]


def authorize(tool: str, resource_id: str, context: dict, policies=None, schema=None):
    """Returns (allowed, decision, reasons, errors). allowed is True only for an Allow without any error."""
    try:
        res = cedarpy.is_authorized({"principal": {"type": "User", "id": "account_holder"}, "action": {"type": "Action", "id": tool},
                                     "resource": {"type": "Account", "id": resource_id or "none"}, "context": context},
                                    _POLICY_SET if policies is None else policies, _ENTITIES,
                                    schema=None if schema is False else (_SCHEMA if schema is None else schema))
    except Exception as exc:                                  # any failure of the engine or of request validation withholds
        return False, "error", [], [repr(exc)[:200]]
    errors = list(res.diagnostics.errors or [])
    allowed = (res.decision == cedarpy.Decision.Allow) and not errors
    return allowed, res.decision.value, list(res.diagnostics.reasons or []), [str(e)[:200] for e in errors]
