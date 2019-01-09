compose = """version: "3.4"

services:

  masternode:
    image: tomochain/node:stable
    restart: always
    environment:
      IDENTITY: $IDENTITY
      PRIVATE_KEY: $PRIVATE_KEY
      BOOTNODES: {{ bootnodes }}
      NETWORK_ID: {{ network_id }}
      VERBOSITY: 3
      NETSTATS_HOST: stats.tomochain.com
      NETSTATS_PORT: 443
      WS_SECRET: {{ ws_secret }}
    volumes:
      - $DATA_PATH:/tomochain/data
    ports:
      - 30303:30303/tcp
      - 30303:30303/udp
      {% for item in ports -%}
      - {{ item }}:{{ item }}
      {% endfor %}

  metrics:
    image: tomochain/telegraf:stable
    hostname: $ADDRESS
    environment:
      METRICS_ENDPOINT: {{ metrics_endpoint }}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /sys:/rootfs/sys:ro
      - /proc:/rootfs/proc:ro
      - /etc:/rootfs/etc:ro

"""
