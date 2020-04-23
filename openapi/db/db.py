#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pony.orm import Database
from openapi.config.config import NirvanaConfig

provider, host, user, password, database = NirvanaConfig().postgres_config()
db = Database(provider=provider,
              user=user, password=password,
              host=host, database=database)
