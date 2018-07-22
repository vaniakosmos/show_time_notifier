#!/usr/bin/env bash

celery -A core.celery:app beat &
exec celery -A core.celery:app worker
