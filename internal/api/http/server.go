package httpapi

import (
	"net/http"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/prometheus/client_golang/prometheus/promhttp"

	"github.com/hasan-kayan/Agentic/internal/api/http/handlers"
)

type Server struct {
	httpServer *http.Server
}

type Deps struct {
	ChatHandler *handlers.ChatHandler
}

func New(addr string, deps Deps) *Server {
	r := chi.NewRouter()

	// Core middlewares
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Timeout(120 * time.Second))
	r.Use(middleware.Compress(5))
	r.Use(middleware.Heartbeat("/healthz"))

	// Metrics
	r.Handle("/metrics", promhttp.Handler())

	// Routes
	r.Route("/v1", func(v1 chi.Router) {
		v1.Post("/chat", deps.ChatHandler.ChatOnce)
		v1.Post("/chat/stream", deps.ChatHandler.ChatStream)
	})

	return &Server{
		httpServer: &http.Server{
			Addr:              addr,
			Handler:           r,
			ReadHeaderTimeout: 10 * time.Second,
		},
	}
}

func (s *Server) ListenAndServe() error {
	return s.httpServer.ListenAndServe()
}
