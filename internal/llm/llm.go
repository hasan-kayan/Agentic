package llm

import (
	"context"

	"github.com/hasan-kayan/Agentic/internal/domain/chat"
)

type StreamEvent struct {
	Delta string
	Done  bool
	Err   error
}

type Client interface {
	ChatOnce(ctx context.Context, model string, messages []chat.Message) (string, error)
	ChatStream(ctx context.Context, model string, messages []chat.Message) (<-chan StreamEvent, error)
}
