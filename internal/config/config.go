package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	HTTPAddr         string
	OpenAIAPIKey     string
	OpenAIModel      string
	SystemPrompt     string
	MaxHistory       int
	OtelOtlpEndpoint string
}

func Load() (Config, error) {
	cfg := Config{
		HTTPAddr:         getenv("HTTP_ADDR", ":8080"),
		OpenAIAPIKey:     os.Getenv("OPENAI_API_KEY"),
		OpenAIModel:      getenv("OPENAI_MODEL", "gpt-5.2"),
		SystemPrompt:     getenv("CHAT_SYSTEM_PROMPT", defaultSystemPrompt()),
		MaxHistory:       getenvInt("CHAT_MAX_HISTORY", 20),
		OtelOtlpEndpoint: os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT"),
	}

	if cfg.OpenAIAPIKey == "" {
		return Config{}, fmt.Errorf("OPENAI_API_KEY is required")
	}
	if cfg.MaxHistory < 0 {
		cfg.MaxHistory = 0
	}
	return cfg, nil
}

func getenv(key, def string) string {
	v := os.Getenv(key)
	if v == "" {
		return def
	}
	return v
}

func getenvInt(key string, def int) int {
	v := os.Getenv(key)
	if v == "" {
		return def
	}
	n, err := strconv.Atoi(v)
	if err != nil {
		return def
	}
	return n
}

func defaultSystemPrompt() string {
	return `You are a helpful assistant. Be concise, correct, and practical.
If the user asks for code, provide production-grade code with clear structure.`
}
