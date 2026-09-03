import os

def escalate(message: str) -> dict[str, object]:
    if os.getenv('DRY_RUN', 'true').lower() == 'true':
        return {'sent': False, 'mode': 'dry-run', 'message': message}
    # Wire the configured Slack webhook here.
    return {'sent': True, 'mode': 'slack', 'message': message}
