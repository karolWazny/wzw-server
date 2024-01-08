# Server for E-Xsultate Songbook Generator Service
# Copyright (C) 2022  Karol Ważny

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import defaults
import logging
from redishandler.jobs import JobManager
from . import service
import quart_cors

from . import controller


redis_host = os.getenv('REDIS_HOST', defaults.REDIS_HOST)
redis_port = os.getenv('REDIS_PORT', defaults.REDIS_PORT)

jobs_manager = JobManager(redis_host, redis_port)
controller.async_generator_service = service.Service(jobs_manager)

level = os.getenv("LOGGING_LEVEL", defaults.LOGGING_LEVEL)
level = logging.getLevelName(level)

logging.basicConfig(level=level,
                    format='%(asctime)s %(levelname)s %(message)s')

allowed_origin = os.getenv("ALLOWED_ORIGIN", defaults.ALLOWED_ORIGIN)


application = controller.application
application = quart_cors.cors(application, allow_origin="*")
