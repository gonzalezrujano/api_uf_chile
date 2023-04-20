#!/usr/bin/env bash

latest=false
micro_service_name='mic_serv_uf_chile'

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

while getopts 'lv:' flag
do
  case "${flag}" in
    v) version=${OPTARG};;
    l) latest=true;;
  esac
done

echo Sincronizando el archivo setup.py
pipenv-setup sync

echo Creando el archivo wheel
echo
python3 setup.py bdist_wheel

if [ $? -eq 0 ]; then
  echo
  echo -e "Creaccion del archivo wheel ${GREEN}exitosa${NC}!"
  echo
else
  echo
  echo -e "Creaccion del archivo wheel ${RED}fallo!${NC} Abortando..."
  echo
  exit 1
fi

echo "Creando la imagen para la version ${version}"
if [ "$latest" = true ]; then
  echo -e "${GREEN}Asignando tambien la etiqueta de latest${NC}"

  docker build -t ${micro_service_name}:latest \
  --build-arg VERSION=${version} \
  --build-arg EXPOSE_PORT=80 .

else
  docker build \
  --build-arg VERSION=${version} \
  --build-arg EXPOSE_PORT=80 \
  -t ${micro_service_name}:latest .
fi
