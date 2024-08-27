#/bin/bash
(cd vue; pnpm run dev --host 0.0.0.0 --port 5173) & python django/manage.py migrate && python django/manage.py runserver_plus --insecure 0.0.0.0:8080
