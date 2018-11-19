cd ../src
pm2 stop main.py --update-env --merge-logs --log-date-format="YYYY-MM-DD HH:mm Z"