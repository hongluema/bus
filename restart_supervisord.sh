#/bin/sh

pid=$(ps -ef |grep "supervisord"| grep -e "bin" |awk '{print $2}')
kill $pid
/usr/bin/python2.7 /usr/bin/supervisord -c /etc/supervisord.conf
pid=$(ps -ef |grep "supervisord"| grep -e "bin" |awk '{print $2}')
echo $pid
echo "start success"
