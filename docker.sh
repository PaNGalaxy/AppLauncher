docker build -f dockerfiles/Dockerfile -t code.ornl.gov:4567/ndip/trame-apps/trame-app-launcher .



docker run -e TRAME_ROUTER_HISTORY_MODE=html5 -e TRAME_UCAMS_CLIENT_SECRET=secret -e TRAME_XCAMS_CLIENT_SECRET=secret -e OAUTHLIB_INSECURE_TRANSPORT=1 -e TRAME_UCAMS_REDIRECT_URL=http://localhost/redirect -it -p 8080:80 code.ornl.gov:4567/ndip/trame-apps/trame-app-launcher