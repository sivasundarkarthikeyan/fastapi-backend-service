#!/usr/bin/env bash

# Show env vars
grep -v '^#' postgres.env

# Export env vars
export $(grep -v '^#' postgres.env | xargs)

