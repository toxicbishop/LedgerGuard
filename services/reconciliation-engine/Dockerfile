FROM golang:1.22-alpine AS build
WORKDIR /src
COPY go.mod .
COPY . .
RUN go build -o /out/reconciler ./cmd/reconciler
FROM alpine:3.20
COPY --from=build /out/reconciler /usr/local/bin/reconciler
ENTRYPOINT ["/usr/local/bin/reconciler"]
