import os

def send_nudge(message: str) -> dict[str, object]:
    if os.getenv('DRY_RUN', 'true').lower() == 'true':
        return {'sent': False, 'mode': 'dry-run', 'message': message}
    # Wire Telegram Bot API here; keep credentials outside source control.
    return {'sent': True, 'mode': 'telegram', 'message': message}
