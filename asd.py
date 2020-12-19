2020-12-19T11:06:14.071038+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/app/wsgiapp.py", line 49, in load
2020-12-19T11:06:14.071039+00:00 app[web.1]: return self.load_wsgiapp()
2020-12-19T11:06:14.071039+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/app/wsgiapp.py", line 39, in load_wsgiapp
2020-12-19T11:06:14.071040+00:00 app[web.1]: return util.import_app(self.app_uri)
2020-12-19T11:06:14.071040+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/util.py", line 358, in import_app
2020-12-19T11:06:14.071040+00:00 app[web.1]: mod = importlib.import_module(module)
2020-12-19T11:06:14.071041+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/importlib/__init__.py", line 127, in import_module
2020-12-19T11:06:14.071042+00:00 app[web.1]: return _bootstrap._gcd_import(name[level:], package, level)
2020-12-19T11:06:14.071042+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
2020-12-19T11:06:14.071043+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 991, in _find_and_load
2020-12-19T11:06:14.071043+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
2020-12-19T11:06:14.071044+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
2020-12-19T11:06:14.071044+00:00 app[web.1]: File "<frozen importlib._bootstrap_external>", line 783, in exec_module
2020-12-19T11:06:14.071044+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
2020-12-19T11:06:14.071045+00:00 app[web.1]: File "/app/remind_me/wsgi.py", line 16, in <module>
2020-12-19T11:06:14.071045+00:00 app[web.1]: application = get_wsgi_application()
2020-12-19T11:06:14.071045+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/core/wsgi.py", line 12, in get_wsgi_application
2020-12-19T11:06:14.071046+00:00 app[web.1]: django.setup(set_prefix=False)
2020-12-19T11:06:14.071046+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/__init__.py", line 19, in setup
2020-12-19T11:06:14.071047+00:00 app[web.1]: configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
2020-12-19T11:06:14.071047+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 83, in __getattr__
2020-12-19T11:06:14.071048+00:00 app[web.1]: self._setup(name)
2020-12-19T11:06:14.071048+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 70, in _setup
2020-12-19T11:06:14.071048+00:00 app[web.1]: self._wrapped = Settings(settings_module)
2020-12-19T11:06:14.071049+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 177, in __init__
2020-12-19T11:06:14.071049+00:00 app[web.1]: mod = importlib.import_module(self.SETTINGS_MODULE)
2020-12-19T11:06:14.071049+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/importlib/__init__.py", line 127, in import_module
2020-12-19T11:06:14.071050+00:00 app[web.1]: return _bootstrap._gcd_import(name[level:], package, level)
2020-12-19T11:06:14.071050+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
2020-12-19T11:06:14.071050+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 991, in _find_and_load
2020-12-19T11:06:14.071051+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
2020-12-19T11:06:14.071051+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
2020-12-19T11:06:14.071051+00:00 app[web.1]: File "<frozen importlib._bootstrap_external>", line 783, in exec_module
2020-12-19T11:06:14.071052+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
2020-12-19T11:06:14.071052+00:00 app[web.1]: File "/app/remind_me/settings.py", line 13, in <module>
2020-12-19T11:06:14.071052+00:00 app[web.1]: import environ
2020-12-19T11:06:14.071053+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/environ.py", line 114
2020-12-19T11:06:14.071053+00:00 app[web.1]: raise ValueError, "No frame marked with %s." % fname
2020-12-19T11:06:14.071054+00:00 app[web.1]: ^
2020-12-19T11:06:14.071054+00:00 app[web.1]: SyntaxError: invalid syntax
2020-12-19T11:06:14.071538+00:00 app[web.1]: [2020-12-19 11:06:14 +0000] [8] [INFO] Worker exiting (pid: 8)
2020-12-19T11:06:14.089357+00:00 app[web.1]: [2020-12-19 11:06:14 +0000] [9] [ERROR] Exception in worker process
2020-12-19T11:06:14.089359+00:00 app[web.1]: Traceback (most recent call last):
2020-12-19T11:06:14.089360+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/arbiter.py", line 583, in spawn_worker
2020-12-19T11:06:14.089360+00:00 app[web.1]: worker.init_process()
2020-12-19T11:06:14.089361+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/workers/base.py", line 119, in init_process
2020-12-19T11:06:14.089361+00:00 app[web.1]: self.load_wsgi()
2020-12-19T11:06:14.089361+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/workers/base.py", line 144, in load_wsgi
2020-12-19T11:06:14.089362+00:00 app[web.1]: self.wsgi = self.app.wsgi()
2020-12-19T11:06:14.089363+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/app/base.py", line 67, in wsgi
2020-12-19T11:06:14.089363+00:00 app[web.1]: self.callable = self.load()
2020-12-19T11:06:14.089363+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/app/wsgiapp.py", line 49, in load
2020-12-19T11:06:14.089364+00:00 app[web.1]: return self.load_wsgiapp()
2020-12-19T11:06:14.089370+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/app/wsgiapp.py", line 39, in load_wsgiapp
2020-12-19T11:06:14.089370+00:00 app[web.1]: return util.import_app(self.app_uri)
2020-12-19T11:06:14.089370+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/gunicorn/util.py", line 358, in import_app
2020-12-19T11:06:14.089371+00:00 app[web.1]: mod = importlib.import_module(module)
2020-12-19T11:06:14.089371+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/importlib/__init__.py", line 127, in import_module
2020-12-19T11:06:14.089372+00:00 app[web.1]: return _bootstrap._gcd_import(name[level:], package, level)
2020-12-19T11:06:14.089372+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
2020-12-19T11:06:14.089372+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 991, in _find_and_load
2020-12-19T11:06:14.089373+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
2020-12-19T11:06:14.089373+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
2020-12-19T11:06:14.089374+00:00 app[web.1]: File "<frozen importlib._bootstrap_external>", line 783, in exec_module
2020-12-19T11:06:14.089374+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
2020-12-19T11:06:14.089374+00:00 app[web.1]: File "/app/remind_me/wsgi.py", line 16, in <module>
2020-12-19T11:06:14.089375+00:00 app[web.1]: application = get_wsgi_application()
2020-12-19T11:06:14.089376+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/core/wsgi.py", line 12, in get_wsgi_application
2020-12-19T11:06:14.089376+00:00 app[web.1]: django.setup(set_prefix=False)
2020-12-19T11:06:14.089377+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/__init__.py", line 19, in setup
2020-12-19T11:06:14.089377+00:00 app[web.1]: configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
2020-12-19T11:06:14.089377+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 83, in __getattr__
2020-12-19T11:06:14.089378+00:00 app[web.1]: self._setup(name)
2020-12-19T11:06:14.089378+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 70, in _setup
2020-12-19T11:06:14.089378+00:00 app[web.1]: self._wrapped = Settings(settings_module)
2020-12-19T11:06:14.089379+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/django/conf/__init__.py", line 177, in __init__
2020-12-19T11:06:14.089402+00:00 app[web.1]: mod = importlib.import_module(self.SETTINGS_MODULE)
2020-12-19T11:06:14.089402+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/importlib/__init__.py", line 127, in import_module
2020-12-19T11:06:14.089403+00:00 app[web.1]: return _bootstrap._gcd_import(name[level:], package, level)
2020-12-19T11:06:14.089403+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 1014, in _gcd_import
2020-12-19T11:06:14.089403+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 991, in _find_and_load
2020-12-19T11:06:14.089404+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 975, in _find_and_load_unlocked
2020-12-19T11:06:14.089404+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 671, in _load_unlocked
2020-12-19T11:06:14.089404+00:00 app[web.1]: File "<frozen importlib._bootstrap_external>", line 783, in exec_module
2020-12-19T11:06:14.089405+00:00 app[web.1]: File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
2020-12-19T11:06:14.089405+00:00 app[web.1]: File "/app/remind_me/settings.py", line 13, in <module>
2020-12-19T11:06:14.089405+00:00 app[web.1]: import environ
2020-12-19T11:06:14.089406+00:00 app[web.1]: File "/app/.heroku/python/lib/python3.8/site-packages/environ.py", line 114
2020-12-19T11:06:14.089406+00:00 app[web.1]: raise ValueError, "No frame marked with %s." % fname
2020-12-19T11:06:14.089406+00:00 app[web.1]: ^
2020-12-19T11:06:14.089407+00:00 app[web.1]: SyntaxError: invalid syntax
2020-12-19T11:06:14.089755+00:00 app[web.1]: [2020-12-19 11:06:14 +0000] [9] [INFO] Worker exiting (pid: 9)
2020-12-19T11:06:14.267955+00:00 app[web.1]: [2020-12-19 11:06:14 +0000] [4] [INFO] Shutting down: Master
2020-12-19T11:06:14.268384+00:00 app[web.1]: [2020-12-19 11:06:14 +0000] [4] [INFO] Reason: Worker failed to boot.
2020-12-19T11:06:14.494218+00:00 heroku[web.1]: Process exited with status 3
2020-12-19T11:06:14.537403+00:00 heroku[web.1]: State changed from up to crashed
2020-12-19T11:06:15.417900+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/" host=remind-me-django-backend.herokuapp.com request_id=d9925af8-0b33-4960-a4d4-236230234ac4 fwd="111.125.106.112" dyno=web.1 connect=1ms service= status=503 bytes= protocol=https
2020-12-19T11:06:15.925745+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/favicon.ico" host=remind-me-django-backend.herokuapp.com request_id=47cf34f4-3773-4203-afe5-91afe93b63f4 fwd="111.125.106.112" dyno= connect= service= status=503 bytes= protocol=https
2020-12-19T11:06:36.376812+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/" host=remind-me-django-backend.herokuapp.com request_id=69f1eb13-dff9-42dd-b2a7-08d8280b0da6 fwd="111.125.106.112" dyno= connect= service= status=503 bytes= protocol=https
2020-12-19T11:06:36.934828+00:00 heroku[router]: at=error code=H10 desc="App crashed" method=GET path="/favicon.ico" host=remind-me-django-backend.herokuapp.com request_id=198c6ccc-efa5-441f-903a-db39fb7d52c2 fwd="111.125.106.112" dyno= connect= service= status=503 bytes= protocol=https