#!/bin/sh
pg_dump --file "/mnt/e/Documents/wines.backup" --host "127.0.0.1" --port "5432" --username "postgres" --verbose --format=c --blobs "wines"