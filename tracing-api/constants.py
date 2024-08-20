POLICY_MODE_ENFORCING   = "Enforcing"       # deny access if there is no allowing policy
POLICY_MODE_PERMISSIVE  = "Permissive"      # allow access if there is no policy associated
POLICY_MODE_DISABLED    = "Disabled"        # disable policy enforcement

DECISION_STRATEGY_UNANIMOUS     = "Unanimous"          # allow access only if every policy is allowing
DECISION_STRATEGY_AFFIRMATIVE   = "Affirmative"        # allow access if there is at least one allowing policy

API_PREFIX = "/v1"
