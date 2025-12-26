package store

import (
	"context"

	"github.com/hasan-kayan/Agentic/internal/domain/chat"
)

type ConversationStore interface {
	Get(ctx context.Context, conversationID string) ([]chat.Message, bool, error)
	Put(ctx context.Context, conversationID string, messages []chat.Message) error
}
