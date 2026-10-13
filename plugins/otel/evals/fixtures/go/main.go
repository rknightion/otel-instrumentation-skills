package main
import (
 "context"
 "net/http"
 "go.opentelemetry.io/otel"
 "go.opentelemetry.io/otel/attribute"
 "go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
)
// Deliberately flawed review fixture; initialization and flushing are missing.
func handler(w http.ResponseWriter, r *http.Request) {
 ctx, span := otel.Tracer("checkout").Start(context.Background(), "GET " + r.URL.Path)
 defer span.End()
 uid := r.Header.Get("X-User-ID")
 span.SetAttributes(attribute.String("app.user_id", uid))
 counter, _ := otel.Meter("checkout").Int64Counter("requests")
 _ = counter
 _ = ctx // async/outbound calls below would lose this context
 w.WriteHeader(200)
}
func main() { http.ListenAndServe(":8080", otelhttp.NewHandler(http.HandlerFunc(handler), "checkout")) }
