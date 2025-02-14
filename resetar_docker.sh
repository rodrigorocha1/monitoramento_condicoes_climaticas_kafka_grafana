#!/bin/bash
docker volume rm $(docker volume ls -q)
docker image rm $(docker image ls -q)
