package main

import (
	"log"

	"github.com/hasan-kayan/Agentic/internal/agents/chat"
	httpapi "github.com/hasan-kayan/Agentic/internal/api/http"
	"github.com/hasan-kayan/Agentic/internal/api/http/handlers"
	"github.com/hasan-kayan/Agentic/internal/config"
	openaiClient "github.com/hasan-kayan/Agentic/internal/llm/openai"
	memstore "github.com/hasan-kayan/Agentic/internal/store/memory"
)

func main() {
	cfg, err := config.Load()
	if err != nil {
		log.Fatal(err)
	}

	st := memstore.New()
	llm := openaiClient.New(cfg.OpenAIAPIKey)

	agent := chat.New(llm, st, cfg.SystemPrompt, cfg.OpenAIModel, cfg.MaxHistory)

	chatHandler := handlers.NewChatHandler(agent, st)

	srv := httpapi.New(cfg.HTTPAddr, httpapi.Deps{
		ChatHandler: chatHandler,
	})

	log.Printf("api listening on %s", cfg.HTTPAddr)
	log.Fatal(srv.ListenAndServe())
}
