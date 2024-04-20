"""Rate limit middleware"""

from slowapi import Limiter, _rate_limit_exceeded_handler  # noqa
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from fss.common.config import configs
from fss.starter.server import app

# Enable rate limiting.
if configs.enable_rate_limit:
    default_limits = configs.global_default_limits
    limiter = Limiter(key_func=get_remote_address, default_limits=[f"{default_limits}"])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)
