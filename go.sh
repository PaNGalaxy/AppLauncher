#/bin/bash
(cd vue; pnpm run dev --host 0.0.0.0 --port 5173) & python ./manage.py runserver_plus --insecure 0.0.0.0:8080
