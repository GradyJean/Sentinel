from core.integrator.nginx import Nginx
import config

nginx = Nginx(config.settings.nginx.base_path, config.CORE_OS)
