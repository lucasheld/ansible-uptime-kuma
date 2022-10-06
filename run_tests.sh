#!/bin/sh

collection_path="$HOME/.ansible/collections/ansible_collections/lucasheld/uptime_kuma"
version="$1"

if [ ! -d "$collection_path" ]
then
  ansible-galaxy collection install git+https://github.com/lucasheld/ansible-uptime-kuma.git
fi
cp -r ./{plugins,tests} "$collection_path"
cd "$collection_path"

if [ $version ]
then
  versions="$version"
else
  versions="1.18.2 1.17.1"
fi

for version in $versions
do
  docker rm -f uptimekuma > /dev/null 2>&1

  echo "Starting uptime kuma $version..."
  docker run -d -it --rm -p 3001:3001 --name uptimekuma "louislam/uptime-kuma:$version" > /dev/null || exit 1

  while [[ "$(curl -s -L -o /dev/null -w ''%{http_code}'' 127.0.0.1:3001)" != "200" ]]
  do
    sleep 0.5
  done

  echo "Running tests..."
  ansible-test units --target-python default --num-workers 1

  echo "Stopping uptime kuma..."
  docker stop uptimekuma > /dev/null

  echo ''
done
