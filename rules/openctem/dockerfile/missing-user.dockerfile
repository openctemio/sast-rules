FROM alpine:3.20 AS build
RUN apk add curl
# ruleid: openctem.dockerfile.missing-user
CMD ["curl", "--version"]

FROM alpine:3.20
USER 1001
# ok: openctem.dockerfile.missing-user
CMD ["id"]
