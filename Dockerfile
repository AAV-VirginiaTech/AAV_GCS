FROM auvsisuas/interop-client:latest

RUN rm -rf /interop/client/tools/mavlink_proxy.py
COPY mavlink_proxy.py /interop/client/tools/mavlink_proxy.py