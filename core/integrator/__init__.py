import config
from core.integrator.nginx import Nginx

nginx = Nginx(config.settings.nginx.base_path, config.CORE_OS)
