FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod go.sum ./
COPY . .
RUN go build -o /out/reconciler ./cmd/reconciler
FROM alpine:3.20
COPY --from=build /out/reconciler /usr/local/bin/reconciler
ENTRYPOINT ["/usr/local/bin/reconciler"]
